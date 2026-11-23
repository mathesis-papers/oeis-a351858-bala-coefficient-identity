# Bala's trinomial coefficient conjecture and its companion formulas

The note proves, for all integers `m,n >= 0`,

`[x^n](1+x+x^2)^m (1+x)^(n-m) = sum_{j=0..floor(n/2)} binom(m,j) binom(n-j,j)`.

Setting `m=3n` proves Peter Bala's conjecture in the FORMULA field of
[OEIS A351858](https://oeis.org/A351858), originally added in revision 2
on 27 February 2022 and retained in revision 31 of 28 October 2025.
The same expansion gives positive finite formulas for the rational-function
family `u_k`, including [A351859](https://oeis.org/A351859).

The note also proves the entries' alternating sums, diagonal and series-reversion
formulas, algebraicity, ordinary Gauss congruences, and the integral-coefficient
criterion stated in A351858. The general coefficient-slope Gauss congruences
allow every positive coefficient slope and every integral power multiplier.

The two infinite obstruction families `k=p-1,p` reprove results of Ravi Bajaj
and Alexander Burns in [their initial mathematical account, Sections 2–3](https://github.com/rbajaj5/a183068-supercongruence/blob/524c02ec2a8da45b9fc7078e7de6f3a044360e82/related-results/A351858CyclotomicFamilyBoundary.md).
Their [subsequent version, Sections 5–7](https://github.com/rbajaj5/a183068-supercongruence/blob/dd9762d8cdf9718ecc09637dc470e87100677886/related-results/A351858CyclotomicFamilyBoundary.md)
gives the separate fixed-`k=2` cubic-congruence argument.
The fixed-`k=3` cubic congruences are outside the proofs here.
The OEIS coefficient-slope sentences say “may satisfy”; they do not assert
a universal theorem. A universal all-`k` interpretation fails at `k=4,5`,
`c=s=1`, `p=5`.

## Files and rebuild

- `note.tex`: complete mathematical arguments and embedded bibliography.
- `verify.py`: exact-integer comparisons, using Python's standard library.
- `verification.json`: deterministic results and finite parameter ranges.
- `reference-values.json`: finite coefficient values from the two OEIS tables,
  encoded as exact hexadecimal integer strings.
- `metadata.json`: title, abstract, creators, license and problem identifier.
- `source-manifest.json`: file sizes and SHA-256 digests.

With Tectonic 0.17.0:

```sh
tectonic note.tex
python3 verify.py
```

Alternatively, with a standard LaTeX distribution:

```sh
pdflatex -halt-on-error note.tex
pdflatex -halt-on-error note.tex
python3 verify.py
```

The bibliography is embedded; BibTeX is unnecessary. The checker requires
Python 3.9 or later and no third-party packages. It compares formal quotient
coefficients with positive sums, alternating sums and reversion identities.
It also compares the two infinite obstruction formulas at every prime from
5 through 97, and ordinary Gauss congruences at the finite ranges listed in
`verification.json`. All arithmetic is integral and exact; there is no rounding.
These finite comparisons supplement the universal written proofs.

## Scope of the formal statement

The declaration `D5.S1.Recurrence.BalaTrinomialCoefficientIdentity.result` in
[the pinned Lean file](https://github.com/the-omega-institute/trureturing/blob/4a7117cee792c7d5598d7f4770577d557fb45137/D5/S1/Recurrence/BalaTrinomialCoefficientIdentity.lean)
states exactly the `m=3n` identity over rational formal power series for every
natural `n`, including zero. Its `source` is the rational quotient, independent
of the finite sum. It does not have the free parameter `m` of the general
theorem. The family, generating-function, Gauss-criterion and obstruction
results have complete written proofs in the note.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Creative Commons Attribution 4.0 International: CC BY 4.0 (`cc-by-4.0`).
