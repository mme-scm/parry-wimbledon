# Koszul homology of a pair of 2-forms and the map f₂

Λ = Λ\*(Zⁿ) with generators e1, …, en; η₁, η₂ ∈ Λ². For a ring R the objects are taken in Λ\*(Rⁿ):

- H₁ᵏ = {(a₁, a₂) ∈ (Λᵏ)² : a₁η₂ − a₂η₁ = 0} / {(bη₁, bη₂) : b ∈ Λᵏ⁻²}
- H₀ᵈ = Λᵈ / (η₁Λᵈ⁻² + η₂Λᵈ⁻²)
- f₂ : H₁ᵏ → H₀ᵏ⁺⁴, f₂(a₁, a₂) = a₁γ₂(η₂) − a₂γ₂(η₁)

Here γ₂ is the second divided power. Over Z it is determined by 2γ₂(η) = η², because Λ_Z is torsion-free. Equivalently, γ₂(Σ cₛmₛ) = Σ_{s<t} cₛcₜ mₛmₜ over the distinct monomials of η. Over another ring it is the base change. f₂ is well defined: it sends a boundary (bη₁, bη₂) to b(η₁γ₂(η₂) − η₂γ₂(η₁)), which lies in the ideal.

The forms are in `forms.json` (the default is the pair below). `run.py` computes everything and writes `results/report.md`, which contains every number quoted here.

```
η₁ = e1e4 + e2e3 + e5e8 + e6e7 + e9e12 + e10e11
η₂ = e1e3 + e2e3 + e2e4 + e5e7 + e6e7 + e6e8 + e9e11 + e10e11 + e10e12
```

## Result for these forms

**f₂ ≠ 0 over Z.** Its only nonzero component is f₂ : H₁³ ≅ Z²⁸ → H₀⁷ ≅ (Z/2)²⁸. Its image is (Z/2)¹⁶. f₂ = 0 on H₁ᵏ for every k ≠ 3.

Over GF(2), f₂ also has rank 16, again only for k = 3. Here H₁³(GF(2)) = H₁³ ⊗ F₂ ⊕ Tor(H₀⁵, F₂) has dimension 28 + 12. The integral image (Z/2)¹⁶ injects into H₀⁷ ⊗ F₂, so the GF(2) image is already the image of the integral classes; the Tor classes add nothing.

| d | H₀ᵈ over Z | H₁ᵈ over Z |
|---|---|---|
| 0 | Z | 0 |
| 1 | Z¹² | 0 |
| 2 | Z⁶⁴ | 0 |
| 3 | Z¹⁹⁶ | Z²⁸ |
| 4 | Z³⁶⁴ ⊕ (Z/2)² | Z¹⁹⁶ |
| 5 | Z³⁹² ⊕ (Z/2)¹² | Z⁵⁷² |
| 6 | Z¹⁹⁶ ⊕ (Z/2)²⁸ | Z⁸⁵⁸ ⊕ Z/2 |
| 7 | (Z/2)²⁸ | Z⁵⁷² ⊕ (Z/2)²⁸ |
| 8 | Z/2 | Z¹⁹⁶ ⊕ (Z/2)²⁸ |
| 9 | 0 | Z²⁸ ⊕ (Z/2)¹² |
| 10 | 0 | (Z/2)² |
| 11, 12 | 0 | 0 |

The only torsion is 2-torsion, all of exponent 2. In particular there is no 5-torsion, even though the discriminant of the pencil is 5.

### f₂ in the given basis

Every map preserves the grading by δ = (δ₁, δ₂, δ₃), where δ_b counts the indices of a monomial in {e_{4b−3}, e_{4b−2}} minus those in {e_{4b−1}, e_{4b}}. In degree 3 → 7 the groups split into 14 weight blocks, each with H₁³ ≅ Z² and H₀⁷ ≅ (Z/2)²:

- **δ ∈ {±1}³ (8 blocks):** the block of Λ³ is spanned by monomials with exactly one index in each 4-block, and the sign of δ_b fixes which pair it comes from. Here f₂ mod 2 is an isomorphism Z²/2 → (Z/2)².
- **δ = ±ε_b (6 blocks):** f₂ = 0.

So ker(f₂ mod 2) has dimension 12 and coker f₂ ≅ (Z/2)¹². `results/report.md` lists, for every block:
- a Z-basis z₁, z₂ of H₁ as explicit integral cycles (a₁, a₂);
- monomials [m₁], [m₂] whose classes form a basis of H₀;
- the class f₂(zⱼ) in that basis;
- the functionals λᵢ giving the coordinates.

For example, in block (+1, +1, +1):

```
H₀⁷ basis: [e1e2e3e5e6e7e9], [e1e2e3e5e6e7e10]
z₁: a₁ = −e1e5e9 − e1e6e10 − e2e5e10 − e2e6e9 − e2e6e10
    a₂ = −e1e5e9 + e1e5e10 + e1e6e9 + e2e5e9 + e2e6e10        f₂(z₁) ≡ [e1e2e3e5e6e7e9] + [e1e2e3e5e6e7e10]
z₂: a₁ = e1e5e9 − e1e5e10 − e1e6e9 − e2e5e9 − e2e6e10
    a₂ = 2e1e5e9 − e1e5e10 − e1e6e9 + e1e6e10 − e2e5e9 + e2e5e10 + e2e6e9    f₂(z₂) ≡ [e1e2e3e5e6e7e10]
```

The substitution e1→e4, e2→e3, e3→−e2, e4→−e1 on any one 4-block fixes η₁ and η₂ and flips δ_b. Together with permutations of the blocks, this is why all 8 blocks of the first kind behave alike, and all 6 of the second kind.

## Proof

**Certificate (rigorous, small).** `results/certificate.json` lists 16 integral cycles z_j ∈ (Λ³)² and 16 functionals λᵢ : Λ⁷ → Z/2. `verify_certificate.py` shares no code with the rest of the package. It checks three things:

1. a₁η₂ = a₂η₁ over Z for each z_j.
2. λᵢ(uη₁) ≡ λᵢ(uη₂) ≡ 0 for all 792 monomials u ∈ Λ⁵, so each λᵢ factors through H₀⁷(Z).
3. The 16×16 matrix λᵢ(f₂(z_j)) mod 2 is invertible.

Hence f₂ ≠ 0 over Z and rank(im f₂) ≥ 16.

The identity 2f₂ = 0 holds for any pair of 2-forms: using a₁η₂ = a₂η₁, 2f₂(a) = a₁η₂² − a₂η₁² = a₂η₁(η₂ − η₁) ∈ (η₁). So im f₂ is an elementary abelian 2-group. The upper bound 16 comes from the full computation.

**Why it holds (hand derivation, which predicted the table before the code ran).** Write x₁, x₂, y₁, y₂ for e_{4b−3}, e_{4b−2}, e_{4b}, e_{4b−1} in block b. Then η₁ = Σ xᵢyᵢ, and η₂ = Σ Bᵢⱼxᵢyⱼ with B = [[0,1],[1,1]] in each block; B has characteristic polynomial t² − t − 1. Let O = Z₂[φ] with φ² = φ + 1, the unramified quadratic extension of Z₂ (residue field F₄, since t² + t + 1 is irreducible mod 2). Over O, B is diagonalizable with eigenvalues φ and φ̄ = 1 − φ, and φ − φ̄ = √5 is a unit. So after a change of basis in GL₁₂(O), which commutes with γ₂ and hence with f₂, Λ = Λ(V) ⊗ Λ(V̄) with V, V̄ symplectic of rank 6, and

  η₁ = ω + ω̄,  η₂ = φω + φ̄ω̄.

- O is flat over Z, so H(O) = H(Z) ⊗ O and f₂(O) = f₂(Z) ⊗ O. Because 2f₂ = 0, the F₂-rank of im f₂(Z) equals the F₄-rank of im f₂(O).
- For a rank-6 symplectic lattice, Λ/(ω) is O, O⁶, O¹⁴, O¹⁴, O/2·[γ₂ω], 0, 0. This is a unit test in `tests/`. By hand, with pᵢ = xᵢyᵢ: ω maps span{pᵢ} → span{pᵢpⱼ} with determinant ±2, and maps the remaining monomials of Λ² bijectively, up to sign, onto the remaining monomials of Λ⁴. Λ³ → Λ⁵ and Λ⁴ → Λ⁶ are onto. Künneth over O gives every entry of the table above.
- Put c = φa₁ − a₂ and c̄ = φ̄a₁ − a₂, so that cω + c̄ω̄ = 0. Expand γ₂(η₁) and γ₂(η₂) and use φ² − φ = φ̄² − φ̄ = 1:

  f₂(a) ≡ (a₁ + c)·γ₂(ω) + (a₁ + c̄)·γ₂(ω̄)  mod (ω, ω̄).

- k = 3: H₁³ is spanned by cycles with c̄ = 0 and c ∈ ker ω ∩ Λ³V, and their mirror images. Then a₁ = c/√5 ≡ c mod 2 and a₁ + c = 2φc/√5. So f₂ ≡ [c] ⊗ [γ₂ω̄] ∈ H₀³(ω) ⊗ O/2. This is nonzero exactly when c ∉ ωΛ¹ + 2Λ³. Mod 2, ω·Λ¹ (dimension 6) lies in ker ω (dimension 14), so the rank is 14 − 6 = 8 per side, 16 in total.
- k = 4: the only target is H₀⁸ = H₀⁴(ω) ⊗ H₀⁴(ω̄) = O/2. The candidates are [c] ⊗ [γ₂ω̄] with c ∈ ker ω ∩ Λ⁴, which is 0 in H₀⁴(ω) because the class map Σ a_{ij}pᵢpⱼ ↦ Σ a_{ij} mod 2 vanishes on ker ω. The terms in H₀³ ⊗ H₀⁵ vanish because H₀⁵ = 0.
- k ≤ 2: H₁ᵏ = 0. k ≥ 5: H₀ᵏ⁺⁴ = 0.

The derivation shows what the result depends on. For any split pencil η₁ = ω + ω̄, η₂ = λω + μω̄ with λ − μ a 2-adic unit, the same computation gives f₂ ≡ ((λ² − λ)a₁ + c)γ₂(ω) + ((μ² − μ)a₁ + c̄)γ₂(ω̄). If λ and μ reduce into F₂, then λ² − λ and μ² − μ are even and the degree-3 classes map to 0. For pencils of this kind, nonvanishing in degree 3 therefore needs eigenvalues in F₄ ∖ F₂ mod 2, as with t² − t − 1.

The same term explains a caveat about the definition. Replace (η₁, η₂) by (η₁, η₂ + tη₁). Under the induced isomorphism of H₁, f₂ changes by (t² − t)·a₁γ₂(η₁) modulo the ideal; rescaling η₁ by a unit u changes it by (u − u²)·a₂γ₂(η₁). For t ∈ Z and u = ±1 these changes lie in the ideal, so over Z and over F₂, f₂ depends only on the pencil up to GL₂. Over O it does not (φ² − φ = 1). This is why the derivation keeps the original pair rather than passing to (ω, ω̄). For the integral split pair (e1e2 + e3e4 + e5e6, e7e8 + e9e10 + e11e12), H₀ and H₁ are the same abelian groups as above, but f₂ = 0 in every degree (a unit test).

The prime 5 is not covered by this argument, because √5 is not a unit there. That H has no 5-torsion is shown only by the computation: the ungraded F₅ dimensions equal the rational ranks.

## Method

1. **Grading.** `koszul.weight_lattice` computes a Z-basis of the characters χ: Zⁿ → Z that are constant on the monomials of η₁ and η₂. Every matrix in the problem is block diagonal for the induced weight grading. `Pair.mult` raises an error if a product leaves its block. For these forms the lattice has rank 4 (over Q it is spanned by the degree and δ₁, δ₂, δ₃), and the largest block of Λᵏ has 88 monomials.
2. **Exact integer linear algebra** (`zlinalg.py`, pure Python ints). Every Smith form U A V = S comes with U⁻¹ and V⁻¹ and is checked exactly: UAV = S, UU⁻¹ = I, VV⁻¹ = I, and the divisibility chain holds.
3. **H₁ per block.** Take the Smith form of D: (a₁, a₂) ↦ a₁η₂ − a₂η₁. The last columns of V give a saturated Z-basis K of ker D. Express im E, E: b ↦ (bη₁, bη₂), in K-coordinates and take its Smith form. Generators of H₁ are the columns of K·U_X⁻¹, with orders s_i.
4. **H₀ per block.** coker M with M = [η₁ | η₂]; the coordinates of a class are U_M x reduced mod sᵢ.
5. **f₂.** Apply F = [γ₂(η₂) | −γ₂(η₁)] to each H₁ generator and reduce in H₀. The image structure comes from the relation lattice ker[Y | diag(s)]. The code asserts that f₂ kills every boundary and that 2f₂ = 0 on every generator.

## Independent checks (all run by `run.py`; about 20 s)

- **Ungraded F_p** for p = 2, 3, 5, 7, 11, using numpy ranks on the full matrices, with no blocks and no Smith forms. The dimensions of H₀(F_p) and H₁(F_p) agree with the universal-coefficient prediction from the integral answer: H₁(F_p)ᵏ = H₁ᵏ ⊗ F_p ⊕ Tor(H₀ᵏ⁺², F_p).
- **f₂ over F₂, ungraded:** rank f₂ = rank[M | F·ker D] − rank M. This gives 16 for k = 3 and 0 otherwise.
- **FLINT** (`python-flint`), per block:
  - invariant factors of H₀ and H₁; torsion of H₁ = torsion of coker E, since Z₁ is saturated. There are 0 mismatches.
  - |im f₂| = |coker M| / |coker [M | F·K]|, with K from the HNF of [Dᵀ | I]. This gives 2¹⁶ for k = 3 and 1 for k = 4.
- **Tests** (`python -m unittest discover -s tests`):
  - signs against permutation parity, associativity, graded commutativity;
  - Smith forms against FLINT on random matrices;
  - the rank-6 symplectic case;
  - one 4-block, where the ranks are predicted by splitting over Q(√5);
  - random pairs on Z⁷ with nontrivial 2-, 3- and 6-torsion, checked against UCT and FLINT;
  - the δ-flip symmetry;
  - the certificate verifier rejects three tampered certificates.

## Use

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python run.py                 # writes results/{report.md, results.json, certificate.json}
python3 verify_certificate.py           # stdlib only
.venv/bin/python -m unittest discover -s tests
```

To try other forms, edit `forms.json`:
- `n`, `eta1`, `eta2`: the forms, written like `e^1 e^4 + 2 e5e8`.
- `display_characters` (optional): weight vectors used only to label blocks.
- `primes`: the primes for the F_p checks.

The core (`exterior.py`, `zlinalg.py`, `koszul.py`) needs only the standard library. numpy is used for the F_p checks; python-flint is optional, for the cross-checks and for LLL-shortened cycle representatives.

Limits: the pure-Python Smith form is meant for blocks of up to a few hundred rows. Generic forms have no weight grading beyond degree, so n = 12 is feasible only because of the grading. The explicit per-block presentation in the report is produced only for target blocks ≅ (Z/2)^r. The image structure in the summary tables is computed for all blocks.
