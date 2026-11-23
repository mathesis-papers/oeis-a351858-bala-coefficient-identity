import json
from math import comb
from pathlib import Path


def multiply(left, right, degree):
    product = [0] * (degree + 1)
    for left_index, left_value in enumerate(left[:degree + 1]):
        for right_index, right_value in enumerate(right[:degree + 1 - left_index]):
            product[left_index + right_index] += left_value * right_value
    return product


def power(base, exponent, degree):
    assert exponent >= 0
    result = [1] + [0] * degree
    factor = base[:degree + 1]
    while exponent:
        if exponent % 2:
            result = multiply(result, factor, degree)
        exponent //= 2
        if exponent:
            factor = multiply(factor, factor, degree)
    return result


def coefficient_quotient(numerator, denominator, degree):
    assert denominator[0] == 1
    quotient = [0] * (degree + 1)
    for index in range(degree + 1):
        value = numerator[index] if index < len(numerator) else 0
        quotient[index] = value - sum(
            denominator[shift] * quotient[index - shift]
            for shift in range(1, min(index, len(denominator) - 1) + 1)
        )
    return quotient[degree]


def original_coefficient(exponent, degree):
    numerator = power([1, 1, 1], exponent, degree)
    if degree >= exponent:
        return multiply(numerator, power([1, 1], degree - exponent, degree), degree)[degree]
    denominator = power([1, 1], exponent - degree, degree)
    return coefficient_quotient(numerator, denominator, degree)


def finite_sum(exponent, degree):
    return sum(comb(exponent, index) * comb(degree - index, index)
               for index in range(min(exponent, degree // 2) + 1))


def family_original(parameter, degree):
    numerator = power([1] * (parameter + 1), (parameter + 1) * degree, degree)
    denominator = power([1] * parameter, parameter * degree, degree)
    return coefficient_quotient(numerator, denominator, degree)


def family_positive(parameter, degree):
    return sum(
        comb((parameter + 1) * degree, index)
        * power([1] * parameter, degree - index, degree - parameter * index)[degree - parameter * index]
        for index in range(degree // parameter + 1)
    )


def binomial(upper, lower):
    return comb(upper, lower) if 0 <= lower <= upper else 0


def alternating_double(degree):
    if degree == 0:
        return 1
    return sum(
        (-1) ** (degree - first - second) * comb(degree, first)
        * comb(3 * degree, second)
        * comb(4 * degree - 2 * second - first - 1, degree - first - second)
        for first in range(degree + 1)
        for second in range(degree - first + 1)
    )


def alternating_triple(degree):
    if degree == 0:
        return 1
    return sum(
        (-1) ** second * binomial(4 * degree, degree - 2 * first - second - third)
        * comb(4 * degree, first) * comb(3 * degree + second - 1, second)
        * comb(second, third)
        for first in range(degree + 1)
        for second in range(degree + 1)
        for third in range(second + 1)
    )


def quotient_series(numerator, denominator, degree):
    assert denominator[0] == 1
    result = [0] * (degree + 1)
    for index in range(degree + 1):
        result[index] = (numerator[index] if index < len(numerator) else 0) - sum(
            denominator[shift] * result[index - shift]
            for shift in range(1, min(index, len(denominator) - 1) + 1)
        )
    return result


def rational_power(parameter, exponent, degree):
    numerator = [1] * (parameter + 1)
    denominator = [1] * parameter
    if exponent < 0:
        numerator, denominator = denominator, numerator
        numerator_exponent = parameter * -exponent
        denominator_exponent = (parameter + 1) * -exponent
    else:
        numerator_exponent = (parameter + 1) * exponent
        denominator_exponent = parameter * exponent
    return quotient_series(power(numerator, numerator_exponent, degree),
                           power(denominator, denominator_exponent, degree), degree)


def compose_zero(series, argument, degree):
    assert argument[0] == 0
    result = [0] * (degree + 1)
    factor = [1] + [0] * degree
    for index, value in enumerate(series[:degree + 1]):
        for position in range(degree + 1):
            result[position] += value * factor[position]
        factor = multiply(factor, argument, degree)
    return result


def reversion_check(parameter, degree):
    function = rational_power(parameter, 1, degree)
    inverse = [0] * (degree + 2)
    for index in range(1, degree + 2):
        inverse[index] = compose_zero(function, inverse, index - 1)[index - 1]
    reduced = inverse[1:]
    derivative = [(index + 1) * reduced[index + 1] for index in range(degree)]
    logarithmic_derivative = quotient_series(derivative, reduced, degree - 1)
    actual = [1] + logarithmic_derivative
    expected = [family_original(parameter, index) for index in range(degree + 1)]
    assert actual == expected
    lower = compose_zero([1] * parameter, inverse, degree)
    upper = compose_zero([1] * (parameter + 1), inverse, degree)
    assert multiply(reduced, power(lower, parameter, degree), degree) == power(
        upper, parameter + 1, degree)
    return degree + 1


def is_prime(value):
    return value >= 2 and all(value % divisor for divisor in range(2, int(value ** 0.5) + 1))


def main():
    parameter_cases = 0
    for exponent in range(41):
        for degree in range(41):
            assert original_coefficient(exponent, degree) == finite_sum(exponent, degree)
            parameter_cases += 1
    target_values = []
    for degree in range(101):
        exact = original_coefficient(3 * degree, degree)
        assert exact == finite_sum(3 * degree, degree)
        target_values.append(exact)
    family_cases = 0
    for parameter in range(1, 9):
        for degree in range(26):
            assert family_original(parameter, degree) == family_positive(parameter, degree)
            family_cases += 1
    assert target_values[:6] == [1, 1, 7, 19, 103, 376]
    assert [family_original(3, degree) for degree in range(6)] == [1, 1, 3, 19, 67, 251]
    references = json.loads(Path(__file__).with_name('reference-values.json').read_text())
    reference_counts = {}
    for sequence, parameter in [('A351858', 2), ('A351859', 3)]:
        for degree, expected in enumerate(references[sequence]['values']):
            assert family_original(parameter, degree) == int(expected, 16)
        reference_counts[sequence] = len(references[sequence]['values'])
    witnesses = []
    for parameter, expected in [(4, 201), (5, 151)]:
        first = family_original(parameter, 1)
        fifth = family_original(parameter, 5)
        assert first == 1 and fifth == expected
        assert (fifth - first) % 25 == 0 and (fifth - first) % 125 != 0
        witnesses.append({'k': parameter, 'u_k_1': first, 'u_k_5': fifth,
                          'difference': fifth - first, 'residue_mod_125': (fifth - first) % 125})
    for degree in range(31):
        assert alternating_double(degree) == family_original(2, degree)
        assert alternating_triple(degree) == family_original(3, degree)
    reversion_cases = sum(reversion_check(parameter, 12) for parameter in range(1, 9))
    gauss_cases = 0
    for parameter in range(1, 7):
        for slope in range(1, 4):
            for multiplier in [-2, -1, 0, 1, 2]:
                for prime in [2, 3, 5, 7]:
                    for level in [1, 2]:
                        upper = prime ** level
                        lower = prime ** (level - 1)
                        upper_value = rational_power(parameter, multiplier * upper, slope * upper)[slope * upper]
                        lower_value = rational_power(parameter, multiplier * lower, slope * lower)[slope * lower]
                        assert (upper_value - lower_value) % upper == 0
                        gauss_cases += 1
    prime_witnesses = []
    for prime in range(5, 98):
        if not is_prime(prime):
            continue
        base = comb(2 * prime - 1, prime)
        for parameter, value in [(prime - 1, base + prime ** 2 * (prime - 2)),
                                 (prime, base + prime ** 2)]:
            assert family_original(parameter, prime) == value
            assert (value - 1) % prime ** 2 == 0 and (value - 1) % prime ** 3 != 0
        prime_witnesses.append(prime)
    result = {
        'status': 'pass',
        'arithmetic': 'exact Python integers; formal series truncated at the extracted degree',
        'two_parameter_identity': {'m_inclusive': [0, 40], 'n_inclusive': [0, 40], 'cases': parameter_cases},
        'A351858_identity': {'n_inclusive': [0, 100], 'cases': len(target_values), 'first_six': target_values[:6]},
        'positive_family_formula': {'k_inclusive': [1, 8], 'n_inclusive': [0, 25], 'cases': family_cases},
        'OEIS_reference_terms_matched': reference_counts,
        'family_counterexamples': witnesses,
        'alternating_sums': {'n_inclusive': [0, 30], 'cases_per_sequence': 31},
        'reversion_and_algebraic_equation': {'k_inclusive': [1, 8], 'degree_inclusive': [0, 12], 'cases': reversion_cases},
        'ordinary_Gauss_congruences': {'k_inclusive': [1, 6], 'coefficient_slopes': [1, 2, 3],
                                     'power_multipliers': [-2, -1, 0, 1, 2], 'primes': [2, 3, 5, 7],
                                     'levels': [1, 2], 'n': 1, 'cases': gauss_cases},
        'infinite_obstruction_formulas': {'primes_checked': prime_witnesses,
                                         'parameters': ['k=p-1', 'k=p'], 'cases': 2 * len(prime_witnesses)},
        'scope': 'Finite coefficient comparisons and exact counterexamples; universal identities have written proofs in note.tex.'
    }
    Path(__file__).with_name('verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
