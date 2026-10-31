"""Transcribed review cards and paired, original practice. Run to rebuild decks.json."""
import json
from pathlib import Path

cards = []

def add(ref, topic, page, question, answer, practice, solution):
    cards.append(dict(id=ref, topic=topic, page=page, question=question, answer=answer,
                      practice_question=practice, practice_answer=solution))

add('1a', 'Logic', 2,
    'Using a truth table, are (p → q) ∧ (q → r) and (p → r) logically equivalent?',
    'No.\np q r | (p→q)∧(q→r) | p→r\nT T T | T | T\nT T F | F | F\nT F T | F | T\nT F F | F | F\nF T T | T | T\nF T F | F | T\nF F T | T | T\nF F F | T | T\nThe columns differ, for example at (T,F,T).',
    'Are p → q and ¬q → ¬p equivalent? Give a truth table.',
    'Yes (contraposition). For (p,q) = TT, TF, FT, FF, both columns are T,F,T,T.')
add('1b', 'Logic', 3,
    'Using Boolean equivalences only, classify (p ∧ (q ∧ ¬q)) → ¬(p → ¬q).',
    'Tautology. q ∧ ¬q ≡ F, so the premise is F. F → B ≡ ¬F ∨ B ≡ T for any B.',
    'Classify (p ∨ ¬p) ∧ (q ∧ ¬q) using Boolean equivalences.',
    'Contradiction: T ∧ F ≡ F.')
add('1c.i', 'Logic', 4,
    'Translate: There is no integer x such that x² − x = −1. Specify the domain.',
    'Domain Z. ¬∃x∈Z (x² − x = −1), equivalently ∀x∈Z (x² − x ≠ −1).',
    'Translate: No real x has x² = −4.',
    '¬∃x∈R (x² = −4), equivalently ∀x∈R (x² ≠ −4).')
add('1c.ii', 'Logic', 4,
    'Translate: For every real x, there is a real y such that xy = 1.',
    '∀x∈R ∃y∈R (xy = 1). Translation preserves the claim; the claim is false at x = 0.',
    'Translate: Every nonzero real x has a real reciprocal.',
    '∀x∈R (x ≠ 0 → ∃y∈R (xy = 1)). This is true: choose y = 1/x.')
add('1d', 'Logic', 5,
    'Prove or disprove: ∀m∈Z ∃n∈Z such that m < n².',
    'True. If m ≥ 0, choose n = m+1: n²−m = m²+m+1 > 0. If m < 0, choose n = 1: m < 0 < 1 = n².',
    'Prove or disprove: ∀m∈Z ∃n∈Z such that n > m².',
    'True. Choose n = m²+1, an integer strictly greater than m².')
for ref, q, a, pq, pa in [
    ('a', '∀x∈R, x² ≠ 2', 'False: x = √2 gives x² = 2.', '∀x∈Q, x² ≠ 2', 'True. If (a/b)²=2 in lowest terms, a²=2b² makes a even, then b even, a contradiction.'),
    ('b', '∃x∈R, x² = x', 'True: x = 0 or x = 1.', '∃x∈R, x² = −1', 'False: real squares are nonnegative.'),
    ('c', '∀x,y∈R ∃z∈R, z = x/y', 'False: take x=1, y=0. Division by zero is undefined.', '∀x∈R ∀y∈R minus {0} ∃z∈R, z = x/y', 'True: choose z=x/y; y is nonzero.'),
    ('d', '∀x∈Z ∃y∈Z, y² − x < 200', 'False: x=−200 gives y²+200 ≥ 200 for every integer y.', '∀x∈Z ∃y∈Z, y² − x ≥ 200', 'True. Choose y=|x|+200; then y²−x ≥ (|x|+200)²−|x| ≥ 40000.'),
    ('e', '∀x∈Z ∀y∈Z, x² ≠ y³', 'False: x=y=0 (also x=8, y=4 gives 64).', '∃x,y∈Z with x²=y³ and x,y both nonzero', 'True: x=y=1, or x=8,y=4.')]:
    add('1e.'+ref, 'Logic', 6, 'True or false? Justify.\n'+q, a, 'True or false? Justify.\n'+pq, pa)
add('1f', 'Logic', 7,
    'For real x,y, let P(x,y) mean (x+1)^(y+1) ∈ Q. Prove or disprove:\n∀x∀y ((x∈Q ∧ y∈Q) → P(x,y)).',
    'False. Choose x=1, y=1/2. Both are rational, but (1+1)^(1/2+1) = 2^(3/2) = 2√2 is irrational.',
    'Must a positive rational raised to a rational power be rational?',
    'No: 2^(1/2)=√2 is irrational, although 2 and 1/2 are rational.')
add('2a', 'Proofs', 8,
    'Show: if integers m,n have even product mn, then m is even or n is even.',
    'Contrapositive: assume both odd, m=2k+1 and n=2j+1. Then mn=2(2kj+k+j)+1 is odd. Hence an even product requires an even factor.',
    'Show: if n² is odd for integer n, then n is odd.',
    'Contrapositive: if n=2k is even, n²=4k²=2(2k²) is even. Thus odd n² implies odd n.')
add('2b', 'Proofs', 9,
    'Show that at least four of any 37 chosen days fall in the same month.',
    'Pigeonhole principle: 12 months holding at most 3 chosen days each accommodate at most 36. Since 37>36, some month has at least 4.',
    'Among 25 people, prove at least three share a birth month.',
    'If each of 12 months had at most 2 people, there would be at most 24. Thus some month has at least 3.')
add('2c', 'Proofs', 10,
    'For integer n ≥ 10, prove n⁴ − 2n² > 3n³.',
    'n⁴−3n³−2n² = n²[n(n−3)−2]. For n≥10, n²>0 and n(n−3)−2 ≥ 10·7−2 = 68 > 0. Therefore the difference is positive.',
    'For integer n ≥ 5, prove n³ > 4n².',
    'n³−4n² = n²(n−4)>0 because n²>0 and n−4≥1.')
add('2d', 'Proofs', 11,
    'Prove these are equivalent for real x: (i) x irrational; (ii) x/3 irrational; (iii) 2x−3 irrational.',
    'Use contrapositives around a cycle.\n(i)→(ii): if x/3=p/q, then x=3p/q is rational.\n(ii)→(iii): if 2x−3=p/q, then x/3=(p+3q)/(6q) is rational.\n(iii)→(i): if x=a/b, then 2x−3=(2a−3b)/b is rational.\nAll numerators and denominators are integers and denominators are nonzero.',
    'Show x is irrational iff 5x+2 is irrational.',
    'If x=a/b is rational, 5x+2=(5a+2b)/b is rational. If 5x+2=p/q is rational, x=(p−2q)/(5q) is rational. Taking contrapositives gives both directions.')
add('2e', 'Proofs', 13,
    'Show the product of three consecutive integers is divisible by 6.',
    'Among n,n+1,n+2, at least one is even and one is divisible by 3 (the residues modulo 3 cover 0,1,2). The product is divisible by 2 and 3, hence by 6 since gcd(2,3)=1.',
    'Show n(n+1) is even for every integer n.',
    'One of two consecutive integers is even, so their product has a factor of 2.')
add('2f', 'Proofs', 14,
    'Prove ∛(2x−1) ≤ ∛(x²) for every real x.',
    'The real cube-root function is increasing, so it suffices to show 2x−1 ≤ x². This is equivalent to (x−1)²≥0, true for all real x.',
    'Prove ∛(6x−9) ≤ ∛(x²) for every real x.',
    'Monotonicity reduces it to 6x−9≤x², equivalent to (x−3)²≥0.')
add('2g', 'Proofs', 15,
    'Prove every odd integer k has a unique pair (n,n+1) with (n+1)²−n²=k.',
    '(n+1)²−n²=2n+1, so necessarily n=(k−1)/2. Since k is odd this is an integer, establishing existence. This equation fixes n uniquely, so the pair is ((k−1)/2,(k+1)/2).',
    'Find and justify the unique consecutive pair whose larger square minus smaller square is 17.',
    '2n+1=17 gives n=8, so the pair is (8,9), with 81−64=17. Solving the linear equation establishes uniqueness.')
add('2h', 'Proofs', 16,
    'Prove x⁴−3y⁴=11 has no integer solutions.',
    'Modulo 3 the equation requires x⁴≡2. But x≡0,1,2 gives x⁴≡0,1,1 respectively. Contradiction.',
    'Prove x²−3y²=2 has no integer solutions.',
    'Modulo 3 this requires x²≡2, but squares modulo 3 are only 0 and 1.')
add('2i', 'Proofs', 17,
    'Find the error: a=b implies a²=ab, hence (a−b)(a+b)=b(a−b). Cancel (a−b), get a+b=b, so a=0.',
    'Since a=b, a−b=0. Cancelling this factor divides by zero. The factored equality is merely 0=0 and does not imply a+b=b.',
    'Find the error: x²=x, so dividing by x gives x=1, the only solution.',
    'Division by x excludes x=0 without justification. Factor x(x−1)=0 to obtain both x=0 and x=1.')
add('3a', 'Sets', 18,
    'For sets A,B,C, prove A ∩ (B ∩ C)ᶜ ⊆ (A ∩ Bᶜ) ∪ (A ∩ Cᶜ).',
    'In fact equality holds: A∩(B∩C)ᶜ = A∩(Bᶜ∪Cᶜ) by De Morgan, then = (A∩Bᶜ)∪(A∩Cᶜ) by distribution. Equality implies inclusion.',
    'Simplify A ∩ (B ∪ C)ᶜ using De Morgan.',
    'A∩(B∪C)ᶜ = A∩Bᶜ∩Cᶜ. An element must be in A and in neither B nor C.')
add('3b', 'Sets', 19,
    'Prove (A ∩ B) ∪ (A ∩ Bᶜ) = A using Boolean algebra.',
    '(A∩B)∪(A∩Bᶜ) = A∩(B∪Bᶜ) = A∩U = A, by distribution, complement, and identity.',
    'Simplify (A ∪ B) ∩ (A ∪ Bᶜ).',
    'By distribution, = A∪(B∩Bᶜ) = A∪∅ = A.')
for ref,q,a,pq,pa in [
    ('i','The set of all primes','Countably infinite: list the primes in increasing order, giving a bijection with positive integers.','The set of even integers','Countably infinite: k↦2k is a bijection Z→2Z.'),
    ('ii','All 3-element subsets of {1,...,100}','Finite: C(100,3)=161700.','All 2-element subsets of {1,...,20}','Finite: C(20,2)=190.'),
    ('iii','The real numbers between 0 and 0.01','Uncountable: x↦0.01x is a bijection (0,1)→(0,0.01).','The real numbers between 2 and 3','Uncountable: x↦x+2 is a bijection (0,1)→(2,3).'),
    ('iv','The power set P(Z)','Uncountable: by Cantor’s theorem |P(Z)|>|Z|; Z is countably infinite.','The power set P(N)','Uncountable by Cantor’s theorem.'),
    ('v','All functions from {0,1} to N','Countably infinite: f↦(f(0),f(1)) is a bijection with N×N, which is countable.','All functions from N to {0,1}','Uncountable: these correspond to subsets of N through indicator functions; P(N) is uncountable.')]:
    add('3c.'+ref,'Sets',20 if ref!='v' else 21,'Classify as finite, countably infinite, or uncountable. Justify:\n'+q,a,'Classify and justify:\n'+pq,pa)
for ref,q,a,pq,pa in [
    ('a','one-to-one but not onto','f(x)=4x+1. Odd inputs give odd outputs. Equality of outputs forces equal inputs; 1 has no odd preimage (it requires x=0).','Give an injective but not surjective map Z→Z.','f(x)=2x. It is injective; odd integers have no preimage.'),
    ('b','onto but not one-to-one','f(x)=x if x>0, and x+2 if x<0. f(1)=f(−1)=1, so not injective. For odd y>0 choose x=y; for odd y<0 choose x=y−2. Thus onto.','Give a surjective but not injective map Z→Z.','f(x)=floor(x/2). Each integer y has preimages 2y and 2y+1, so onto and not injective.'),
    ('c','both onto and one-to-one, different from identity','f(x)=−x. Odd outputs stay odd. −a=−b implies a=b. Every odd y has preimage −y. Since f(1)=−1, this is not identity.','Give a nonidentity bijection Z→Z.','f(x)=x+1. Injective by cancellation; every y has preimage y−1.'),
    ('d','neither one-to-one nor onto','f(x)=|x|. f(3)=f(−3), so not injective. Negative odd numbers have no preimage, so not onto.','Give a map Z→Z that is neither injective nor surjective.','f(x)=x²: f(1)=f(−1), and −1 has no preimage.')]:
    add('4a.'+ref,'Functions',22 if ref in 'ab' else 23,'Let O be all odd integers. Give f:O→O that is '+q+'. Justify.',a,pq,pa)
add('4b','Functions',24,
    'For g:R→R, g(x)=−2x⁵/3−3, prove whether it is one-to-one and onto. Find its inverse.',
    'Injective: g(a)=g(b) implies a⁵=b⁵ and hence a=b.\nOnto: for any real y choose x=⁵√[−(3/2)(y+3)], a real number; substitution gives g(x)=y.\nThus g is bijective and g⁻¹(x)=⁵√[−(3/2)(x+3)].',
    'Show h:R→R, h(x)=2x³+5 is bijective and find h⁻¹.',
    'Equal outputs imply equal cubes and equal inputs. Every y has real preimage ∛((y−5)/2). Thus h⁻¹(x)=∛((x−5)/2).')
add('4c','Functions',26,
    'Let f:X→Y and g:Z→X be onto. Prove f∘g is onto.',
    'Take arbitrary y∈Y. Since f is onto, choose x∈X with f(x)=y. Since g is onto, choose z∈Z with g(z)=x. Then (f∘g)(z)=f(x)=y. Every y has a preimage.',
    'If f:X→Y and g:Z→X are injective, prove f∘g is injective.',
    'If f(g(a))=f(g(b)), injectivity of f gives g(a)=g(b); injectivity of g gives a=b.')
add('5a','Puzzles',27,
    'Each of two rooms has treasure or a tiger. Door 1 inscription is true iff room 1 has treasure. Door 2 inscription is true iff room 2 has a tiger.\nDoor 1: "Both rooms have treasure or both have tigers."\nDoor 2: "The other room has treasure and this room has a tiger."\nLet p,q mean room 1,2 has treasure. Translate inscriptions and use a truth table to find contents.',
    'S1=(p∧q)∨(¬p∧¬q)=(p↔q). S2=p∧¬q.\nConstraints: C1=(p↔S1), C2=(¬q↔S2).\np q | C1 C2 | both\nT T | T T | T\nT F | F T | F\nF T | T T | T\nF F | F F | F\nRoom 2 has treasure; room 1 is undetermined.',
    'Two doors have treasure or tigers. Each inscription is true iff its own room has treasure. Door 1 says "Door 2 has treasure." Door 2 says "Both rooms have treasure." What are the possibilities?',
    'With p,q meaning treasure: p↔q and q↔(p∧q). Valid assignments are TT and FF. Both rooms have treasure or both have tigers; neither is determined uniquely.')
add('5b','Puzzles',29,
    'Knights tell truth; knaves lie. A says "B is a knight." B says "We are of opposite types." Let p,q mean A,B is a knight. Translate and determine types with a truth table.',
    'A’s statement is q; B’s statement is p⊕q. Constraints are p↔q and q↔(p⊕q).\np q | p↔q | q↔(p⊕q) | both\nT T | T | F | F\nT F | F | F | F\nF T | F | T | F\nF F | T | T | T\nBoth A and B are knaves.',
    'A says "B is a knave." B says "We are of opposite types." Determine their types.',
    'Constraints: p↔¬q and q↔(p⊕q). The first requires opposite types, so XOR is true; then q must be true. Thus A is a knave and B a knight.')
add('6.1','Circuits',30,
    'Find a Boolean formula and draw a circuit for this table:\np q r | f\nT T T | F\nT T F | T\nT F T | F\nT F F | T\nF T T | F\nF T F | T\nF F T | F\nF F F | F',
    'DNF: (p∧q∧¬r)∨(p∧¬q∧¬r)∨(¬p∧q∧¬r).\nSimplifies to f=(p∨q)∧¬r.\np ─┐\n   OR ──┐\nq ─┘    AND ── f\nr ─NOT──┘',
    'Build a formula and circuit whose output is true exactly when r is true and at least one of p,q is false.',
    'f=r∧(¬p∨¬q), equivalently r∧¬(p∧q). Feed p,q to AND, invert its output, then AND with r.')
add('6.2','Circuits',32,
    'A circuit makes X=¬A∧C and Y=¬C∨B, ORs X with Y, then ANDs the result with ¬B. Write F and its truth table.',
    'F=[(¬A∧C)∨(¬C∨B)]∧¬B, simplifying to (¬A∨¬C)∧¬B.\nA B C | F\nT T T | F\nT T F | F\nT F T | F\nT F F | T\nF T T | F\nF T F | F\nF F T | T\nF F F | T',
    'Write the truth table for F=(A∨C)∧¬B.',
    'For ABC in order TTT,TTF,TFT,TFF,FTT,FTF,FFT,FFF, F is F,F,T,T,F,F,T,F.')
add('7a','Induction',33,
    'Use induction to prove Σ(i=1..n) (i+1)i² = n(n+1)(n+2)(3n+1)/12 for n≥1.',
    'Base n=1: both sides are 2.\nAssume S(k)=k(k+1)(k+2)(3k+1)/12.\nS(k+1)=S(k)+(k+2)(k+1)²\n = (k+1)(k+2)[k(3k+1)+12(k+1)]/12\n = (k+1)(k+2)(k+3)(3k+4)/12.\nThis is the required formula at k+1, so induction proves the identity.',
    'Prove by induction Σ(i=1..n) i = n(n+1)/2.',
    'Base n=1: 1=1. Assume S(k)=k(k+1)/2. Then S(k+1)=k(k+1)/2+(k+1)=(k+1)(k+2)/2. Therefore true for every n≥1.')
add('7b','Induction',35,
    'Prove the identity from 7a again, using known formulas for sums of squares and cubes.',
    'Σ(i+1)i² = Σi³+Σi²\n = n²(n+1)²/4 + n(n+1)(2n+1)/6\n = n(n+1)[3n(n+1)+2(2n+1)]/12\n = n(n+1)(3n²+7n+2)/12\n = n(n+1)(n+2)(3n+1)/12.',
    'Find a closed form for Σ(i=1..n) i(i+1) using known sums.',
    'Σ(i²+i)=n(n+1)(2n+1)/6+n(n+1)/2=n(n+1)(n+2)/3.')
add('7c','Induction',37,
    'Prove by induction Σ(i=1..n) 1/[i(i+1)] = n/(n+1), for n≥1.',
    'Base n=1: 1/2=1/2.\nAssume S(k)=k/(k+1). Then\nS(k+1)=k/(k+1)+1/[(k+1)(k+2)]\n =[k(k+2)+1]/[(k+1)(k+2)]\n =(k+1)²/[(k+1)(k+2)]=(k+1)/(k+2).\nThus the claim follows by induction.',
    'Evaluate Σ(i=1..n) 1/[(i+1)(i+2)].',
    'Use 1/[(i+1)(i+2)]=1/(i+1)−1/(i+2). The sum telescopes to 1/2−1/(n+2)=n/[2(n+2)].')
add('7d','Induction',39,
    'Let a₁=1, a₂=4, aₙ=2aₙ₋₁−aₙ₋₂ for n≥3. Prove aₙ=3n−2.',
    'Two base cases: 3·1−2=1 and 3·2−2=4.\nAssume the formula through k≥2. Then\naₖ₊₁=2aₖ−aₖ₋₁=2(3k−2)−[3(k−1)−2]=3k+1=3(k+1)−2.\nStrong induction proves it for all n≥1.',
    'Let b₁=2,b₂=7,bₙ=2bₙ₋₁−bₙ₋₂. Find and prove a closed form.',
    'bₙ=5n−3. Bases: 2,7. Assuming the two previous formulas, bₖ₊₁=2(5k−3)−(5k−8)=5k+2=5(k+1)−3. Induction completes the proof.')
add('7e.a','Induction',41,
    'Compute Σ(i=n+1..2n) (3i²−i+1).',
    'Let S₁(m)=m(m+1)/2 and S₂(m)=m(m+1)(2m+1)/6.\nSum = 3[S₂(2n)−S₂(n)]−[S₁(2n)−S₁(n)]+n\n = n(7n²+3n+1).',
    'Compute Σ(i=n+1..2n) i.',
    'S₁(2n)−S₁(n)=n(2n+1)−n(n+1)/2=n(3n+1)/2.')
add('7e.b','Induction',41,
    'Compute Σ(k=1..n) (2n−k)².',
    'Expand: Σ(4n²−4nk+k²)\n = 4n³−4n·n(n+1)/2+n(n+1)(2n+1)/6\n = n(14n²−9n+1)/6 = n(2n−1)(7n−1)/6.',
    'Compute Σ(k=1..n) (n+k)².',
    'Expand n²+2nk+k² and sum: n³+n²(n+1)+n(n+1)(2n+1)/6=n(2n+1)(7n+1)/6.')
add('7e.c','Induction',41,
    'Compute Σ(k=1..n) (3ᵏ−2ᵏ).',
    'Geometric sums give 3(3ⁿ−1)/2 − 2(2ⁿ−1) = (3ⁿ⁺¹−2ⁿ⁺²+1)/2.',
    'Compute Σ(k=1..n) (4ᵏ−2ᵏ).',
    '4(4ⁿ−1)/3−2(2ⁿ−1)=(4ⁿ⁺¹−3·2ⁿ⁺¹+2)/3.')
add('8a','Irrationality',43,
    'Using the definition of rational number, prove ∛(√27+1) is irrational.',
    'Suppose ∛(√27+1)=p/q for integers p,q with q≠0. Cubing and using √27=3√3 gives √3=(p³−q³)/(3q³), a rational number.\nTo supply the needed contradiction from the definition: if √3=a/b in lowest terms, a²=3b². Squares mod 3 are 0 or 1, so 3|a. Put a=3k; then b²=3k², so 3|b. This contradicts lowest terms. Thus √3, and hence the original expression, is irrational.\nThis includes the √3 subproof omitted in the sheet’s solution.',
    'Prove ∛(√12+2) is irrational.',
    'If it equals p/q, cubing gives 2√3+2=p³/q³, so √3=(p³−2q³)/(2q³) is rational. But √3 is irrational: a²=3b² in lowest terms forces 3|a and 3|b. Contradiction.')
add('8b','Irrationality',44,
    'Prove √5−√3 is irrational.',
    'Suppose x=√5−√3 is rational. Then x²=8−2√15, so √15=(8−x²)/2 is rational.\nIf √15=a/b in lowest terms, a²=15b². Prime divisibility forces both 3 and 5 to divide a, hence a=15k. Then b²=15k² forces 15|b too, contradicting lowest terms. Therefore √15 is irrational, contradicting the assumed rational x.',
    'Prove √3−√2 is irrational.',
    'If x=√3−√2 is rational, x²=5−2√6 gives √6=(5−x²)/2 rational. If √6=a/b in lowest terms, a²=6b² forces 2|a and 3|a, so a=6k and b²=6k² forces 6|b, contradiction.')
for ref,q,a,pq,pa in [
    ('a','An irrational number raised to an irrational power is always irrational.',
     'False. A concrete example is (√2)^(log₂9)=3. The base √2 is irrational. The exponent log₂9 is irrational: a positive rational a/b would imply 2ᵃ=9ᵇ=3²ᵇ, impossible by prime factorization. Yet the power equals 3.\nThis uses an elementary counterexample in place of the sheet’s e and ln(2).',
     'Can an irrational base raised to an irrational exponent be rational?',
     'Yes: (√3)^(log₃4)=2. The exponent is irrational, since log₃4=a/b would force 3ᵃ=2²ᵇ, contradicting unique prime factorization.'),
    ('b','For distinct primes p,q, logₚ(q) is irrational.',
     'True. If logₚ(q)=a/b with positive integers a,b, then pᵃ=qᵇ. Unique prime factorization forbids this because p≠q.',
     'Prove log₂7 is irrational.',
     'If log₂7=a/b with positive integers a,b, then 2ᵃ=7ᵇ, impossible by unique prime factorization.'),
    ('c','The difference of two irrational numbers is irrational.',
     'False: (√2+1)−√2=1 is rational, while both terms are irrational.',
     'Is the sum of two irrational numbers always irrational?',
     'No: √2+(−√2)=0 is rational.'),
    ('d','The product of a nonzero rational and an irrational is always irrational.',
     'True. Let r≠0 be rational and t irrational. If rt=q were rational, t=q/r would be rational, a contradiction.',
     'If r is rational and t irrational, prove r+t is irrational.',
     'If r+t=q were rational, t=q−r would be rational. Contradiction.')]:
    add('8c.'+ref,'Irrationality',45 if ref!='d' else 46,'True or false? Justify:\n'+q,a,pq,pa)

if __name__ == '__main__':
    Path(__file__).with_name('decks.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2)+'\n')
    print(f'Built {len(cards)} midterm cards and {len(cards)} paired practice cards.')
