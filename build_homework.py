"""Homework study cards, with worked answers to required problems in both PDFs."""
import json
from pathlib import Path

cards = []


def add(hw, ref, topic, page, question, answer):
    cards.append(dict(id=f'HW{hw} {ref}', set='homework', topic=topic, page=page,
                      source=f'Homework {hw} p.{page} | CS205F26-HW-{"1-1" if hw == 1 else "2"}.pdf',
                      question=question, answer=answer))


for ref, q, a in [
    ('a', 'Users can log in only if the server is online.', 'r → p. "Only if" introduces a necessary condition.'),
    ('b', 'The database is available unless the server is offline.', 'q ∨ ¬p, equivalently p → q. "A unless B" translates as ¬B → A.'),
    ('c', 'If either the server is offline or the database is unavailable, users cannot log in.', '(¬p ∨ ¬q) → ¬r.'),
    ('d', 'Users can log in iff the server is online and the database is available.', 'r ↔ (p ∧ q).'),
    ('e', 'The server being online does not guarantee that users can log in.', '¬(p → r), equivalently p ∧ ¬r, in the propositional reading requested. In ordinary usage this may instead describe a possible counterexample; propositional logic has no possibility operator.')]:
    add(1, '1'+ref, 'Logic', 2, 'Translate using p = server online, q = database available, r = users can log in:\n'+q, a)

for ref, q, a in [
    ('a', 'Every student who attended every recitation and submitted the assignment passed the exam.', '∀x ((R(x) ∧ P(x)) → Q(x)).'),
    ('b', 'Some student submitted the assignment but did not pass the exam.', '∃x (P(x) ∧ ¬Q(x)).'),
    ('c', 'Not every student who submitted the assignment passed the exam.', '¬∀x (P(x) → Q(x)), equivalently ∃x (P(x) ∧ ¬Q(x)).'),
    ('d', 'No student who failed to submit the assignment attended every recitation.', '∀x (¬P(x) → ¬R(x)), equivalently ¬∃x (¬P(x) ∧ R(x)).'),
    ('e', 'Exactly one student passed the exam without submitting the assignment.', '∃x [Q(x) ∧ ¬P(x) ∧ ∀y ((Q(y) ∧ ¬P(y)) → y=x)]. The last clause establishes uniqueness.')]:
    add(1, '2'+ref, 'Logic', 2, 'Domain: all students. P(x) = submitted assignment; Q(x) = passed exam; R(x) = attended every recitation. Translate:\n'+q, a)

add(1, '3a', 'Puzzles', 2,
    'Victoria says "Ingrid lies." Ingrid says "Trevor never tells the truth." Trevor says "Victoria is a knight." Yasmin says "Trevor is a knave and I am a knave."\nLet p,q,r,s mean Victoria, Ingrid, Trevor, Yasmin is a knight, respectively. Formalize all constraints.',
    'C1: p ↔ ¬q.\nC2: q ↔ ¬r.\nC3: r ↔ p.\nC4: s ↔ (¬r ∧ ¬s).\nAll four constraints must hold together. A speaker is a knight exactly when their statement is true.')
from itertools import product
rows = []
for p, q, r, s in product([True, False], repeat=4):
    values = [p == (not q), q == (not r), r == p, s == ((not r) and (not s))]
    rows.append(' '.join('T' if x else 'F' for x in [p,q,r,s])+' | '+' '.join('T' if x else 'F' for x in values)+' | '+('T' if all(values) else 'F'))
add(1, '3b', 'Puzzles', 2,
    'Use a truth table to solve the four-islander puzzle. p,q,r,s mean Victoria, Ingrid, Trevor, Yasmin is a knight.\nC1=(p↔¬q), C2=(q↔¬r), C3=(r↔p), C4=(s↔(¬r∧¬s)).',
    'p q r s | C1 C2 C3 C4 | all\n'+'\n'.join(rows)+'\nOnly (T,F,T,F) works: Victoria and Trevor are knights; Ingrid and Yasmin are knaves.')
add(1, '4a', 'Circuits', 3,
    'A candidate is hired if President and Vice-President both vote yes OR at least three of President, Vice-President, Secretary, Treasurer vote yes. Write an unsimplified Boolean formula.',
    'H=(p∧v) ∨ (p∧v∧s) ∨ (p∧v∧t) ∨ (p∧s∧t) ∨ (v∧s∧t).\nEach three-person conjunction also allows the fourth person to vote yes.')
add(1, '4b', 'Circuits', 3,
    'Simplify H=(p∧v)∨(p∧v∧s)∨(p∧v∧t)∨(p∧s∧t)∨(v∧s∧t). Show Boolean laws.',
    'Absorption A∨(A∧B)=A removes p∧v∧s and p∧v∧t:\nH=(p∧v)∨(p∧s∧t)∨(v∧s∧t).\nDistribute the last two terms:\nH=(p∧v)∨((p∨v)∧s∧t).')
add(1, '4c', 'Circuits', 3,
    'Describe a logic circuit for H=(p∧v)∨((p∨v)∧s∧t).',
    'Gate 1: AND(p,v) → A.\nGate 2: OR(p,v) → B.\nGate 3: AND(B,s,t) → C.\nGate 4: OR(A,C) → H.\nThis uses two AND gates and two OR gates; no NOT gates are needed.')
for ref, q, a in [
    ('a', 'Translate: real-time requires cloud; cloud requires NoSQL; client requires real-time and forbids NoSQL.', 'r → c; c → m; r ∧ ¬m.'),
    ('b', 'Are r→c, c→m, r∧¬m consistent?', 'No. From r∧¬m obtain r and ¬m. Modus ponens on r→c gives c, and on c→m gives m. This contradicts ¬m.'),
    ('c', 'Replace the last constraint with r∧¬c. Are r→c, c→m, r∧¬c consistent?', 'No. r∧¬c gives r and ¬c; r→c and r yield c, contradicting ¬c.'),
    ('d', 'Is r→m a consequence of r→c and c→m?', 'Yes, by hypothetical syllogism. Assume r; modus ponens yields c, then m. Therefore r→m. Thus ((r→c)∧(c→m))→(r→m) is a tautology.')]:
    add(1, '5'+ref, 'Logic', 3, 'Project variables: r = real-time, c = cloud, m = NoSQL.\n'+q, a)
add(1, '6', 'Puzzles', 3,
    'Each of two rooms holds treasure or a tiger. Door 1 tells the truth iff room 1 has treasure. Door 2 tells the truth iff room 2 has a tiger.\nDoor 1 says "Both rooms have treasure." Door 2 says "This room has treasure and the other room has a tiger." Formalize and find the treasure.',
    'Let p,q mean room 1,2 has treasure. Inscriptions are S1=p∧q and S2=q∧¬p.\nConstraints: p↔(p∧q) and ¬q↔(q∧¬p).\np q | constraint 1 | constraint 2 | both\nT T | T | T | T\nT F | F | F | F\nF T | T | F | F\nF F | T | F | F\nBoth rooms have treasure. Door 1 is truthful and Door 2 lies.')
for ref, page, q, a in [
    ('a.a',3,'Translate ∀x∈Z ∃y∈Z (x+y=0) into English and negate it.', 'Every integer has an integer additive inverse.\nNegation: ∃x∈Z ∀y∈Z (x+y≠0). There is an integer with no integer additive inverse.'),
    ('a.b',3,'Translate ∃z∈Z ∀x∈Z ∀y∈Z (x+y=z) into English and negate it.', 'One fixed integer equals the sum of every pair of integers.\nNegation: ∀z∈Z ∃x∈Z ∃y∈Z (x+y≠z). For each candidate integer, some pair does not sum to it.'),
    ('b.a',3,'True or false over Z: ∀x ∃y (x+y=0)?', 'True. Given any integer x, choose y=−x, also an integer.'),
    ('b.b',4,'True or false over Q: ∀z ∃x,y (x+y=z)?', 'True. Given rational z, choose x=z and y=0; both are rational.'),
    ('b.c',4,'True or false over Z: ∃z ∀x (x+x=z)?', 'False. x=0 forces z=0, while x=1 forces z=2. No fixed z satisfies both.'),
    ('c-d.a',4,'Formalize "Every integer has an additive inverse," then give the formal negation and its English meaning.', 'Statement: ∀x∈Z ∃y∈Z (x+y=0).\nNegation: ∃x∈Z ∀y∈Z (x+y≠0).\nEnglish negation: Some integer has no integer additive inverse.'),
    ('c-d.b',4,'Formalize "There is a prime number greater than 100," then negate formally and in English.', 'Statement: ∃p∈Z (Prime(p) ∧ p>100).\nNegation: ∀p∈Z (¬Prime(p) ∨ p≤100).\nEnglish negation: Every prime number is at most 100.'),
    ('c-d.c',4,'Formalize "Not all rationals are integers," then negate formally and in English.', 'Statement: ∃x∈Q (x∉Z), equivalently ¬∀x∈Q (x∈Z).\nNegation: ∀x∈Q (x∈Z).\nEnglish negation: Every rational number is an integer.'),
    ('c-d.d',4,'Formalize "For every real x, there exists a rational y with y>x," then negate formally and in English.', 'Statement: ∀x∈R ∃y∈Q (y>x).\nNegation: ∃x∈R ∀y∈Q (y≤x).\nEnglish negation: Some real number is an upper bound for every rational number.')]:
    add(1, '7'+ref, 'Logic', page, q, a)
add(1, '8.translations', 'Logic', 4,
    'Domain: Ron, Adi, Leonard, Whit, Susan. K(x) means x knows the secret key. Translate:\n(i) ∃x∃y (x≠y∧K(x)∧K(y))\n(ii) ¬∃x∃y∃z (x≠y∧x≠z∧y≠z∧K(x)∧K(y)∧K(z))\n(iii) K(Ron)→K(Whit)\n(iv) K(Adi)∨K(Ron)\n(v) K(Whit)→K(Adi)\n(vi) K(Adi)→¬K(Susan)\n(vii) K(Leonard)→K(Ron)',
    '(i) At least two people know the key.\n(ii) At most two people know the key.\n(iii) If Ron knows it, Whit knows it.\n(iv) Adi or Ron (or both) knows it.\n(v) If Whit knows it, Adi knows it.\n(vi) If Adi knows it, Susan does not.\n(vii) If Leonard knows it, Ron knows it.')
add(1, '8.solution', 'Puzzles', 4,
    'Exactly two of Ron, Adi, Leonard, Whit, Susan know the key. Ron→Whit; Adi∨Ron; Whit→Adi; Adi→¬Susan; Leonard→Ron. Who knows it?',
    'If Ron knew it, Whit and then Adi would too: three people, impossible. So Ron does not.\nAdi∨Ron now forces Adi. Then Susan does not know it. Leonard cannot know it, since Leonard→Ron.\nExactly two know it, so Whit is the second. The key holders are Adi and Whit.')
add(1, '9a', 'Proofs', 4,
    'Starting from the definition, prove the sum of two rational numbers is rational.',
    'Let r=a/b and s=c/d, where a,b,c,d are integers and b,d≠0. Then r+s=(ad+bc)/(bd). The numerator and denominator are integers, and bd≠0. Hence r+s is rational by definition.')
add(1, '9b', 'Irrationality', 4,
    'Starting from the definition, prove the sum of an irrational number and a rational number is irrational.',
    'Let x be irrational and r=a/b rational, b≠0. Suppose x+r=c/d is rational, d≠0. Then x=c/d−a/b=(bc−ad)/(bd), a ratio of integers with nonzero denominator. This contradicts x being irrational.')
add(1, '9c', 'Irrationality', 4,
    'Prove these are equivalent: (i) x is rational; (ii) x/2 is rational; (iii) 3x−5 is rational. Start from the definition of rational number.',
    '(i)→(ii): If x=a/b with integers a,b and b≠0, then x/2=a/(2b), rational.\n(ii)→(iii): If x/2=c/d with integers c,d and d≠0, then x=2c/d, so 3x−5=(6c−5d)/d, rational.\n(iii)→(i): If 3x−5=e/f with integers e,f and f≠0, then x=(e+5f)/(3f), rational.\nEvery numerator and denominator is an integer and all denominators are nonzero. This cycle proves all three statements equivalent. The source expression is x/2, not x².')

add(2, '1', 'Logic', 1,
    'Formalize and prove using named inference rules:\nEvery council member who is a wizard is a powerful mage. Gandalf is a wizard and a council member. Sauron is rising or Gandalf is not a powerful mage. If Sauron rises, the Ring is destroyed. If the Ring is destroyed, peace comes. Conclude peace.',
    'Let C,W,M be council member, wizard, mage predicates; g=Gandalf; S=Sauron rises; D=Ring destroyed; P=peace.\nPremises: ∀x ((C(x)∧W(x))→M(x)); W(g)∧C(g); S∨¬M(g); S→D; D→P.\n1. W(g), C(g): conjunction elimination.\n2. C(g)∧W(g): conjunction introduction.\n3. (C(g)∧W(g))→M(g): universal instantiation.\n4. M(g): modus ponens, 2 and 3.\n5. ¬¬M(g): double negation, 4.\n6. S: disjunctive syllogism, S∨¬M(g) and 5.\n7. D: modus ponens, S→D and 6.\n8. P: modus ponens, D→P and 7.')
add(2, '2', 'Induction', 1,
    'Successor arithmetic / Lean Number Game study: how do you prove a·(b+c)=a·b+a·c from recursive addition and multiplication? Identify the needed lemmas.',
    'This is a study outline, not a transcript of completed game levels. Take n+0=n, n+succ(m)=succ(n+m), n·0=0, n·succ(m)=n·m+n as the recursive definitions.\nFirst prove 0+n=n and succ(n)+m=succ(n+m) by induction on the second input. Prove addition associativity by induction on its last input; prove addition commutativity by induction on its second input using the successor lemma.\nNow induct on c. Base c=0: a·(b+0)=a·b=a·b+0=a·b+a·0.\nStep: a·(b+succ(c))=a·succ(b+c)=a·(b+c)+a=(a·b+a·c)+a=a·b+(a·c+a)=a·b+a·succ(c). Use the induction hypothesis at the third equality and associativity at the fourth.\nIn Lean, induction supplies the base and step; rw applies definitions, the induction hypothesis, and associativity; rfl closes identical expressions. The assignment separately requests your actual commands from earlier game levels.')
for ref, topic, q, a in [
    ('a','Proofs','Prove every odd integer is a difference of two perfect squares.', 'Let k=2n+1 with n∈Z. Then (n+1)²−n²=2n+1=k. Both squares are squares of integers, even when n is negative.'),
    ('b','Proofs','Prove the product of three consecutive integers is divisible by 6.', 'Among n,n+1,n+2, at least one is even. Their residues modulo 3 cover 0,1,2, so one is divisible by 3. The product is divisible by both 2 and 3, hence by 6 because these factors are relatively prime.'),
    ('c','Irrationality','Prove √5−√3 is irrational.', 'Suppose r=√5−√3 is rational. Since √5>√3, r≠0. Squaring √5=r+√3 yields 5=r²+2r√3+3, hence √3=(2−r²)/(2r), rational. But if √3=a/b in lowest terms, a²=3b². Squares mod 3 are 0 or 1, so 3|a. Write a=3k; then b²=3k², giving 3|b, a contradiction. Thus r is irrational.'),
    ('d','Proofs','For integer n≥10, prove n⁴−2n²>3n³.', 'Subtract the right side: n⁴−3n³−2n²=n²[n(n−3)−2]. For n≥10, n²>0 and n(n−3)−2≥10·7−2=68>0. The difference is positive.'),
    ('e','Proofs','Prove integers x,y are both odd iff xy+2y is odd.', 'Forward: x=2a+1 and y=2b+1 give y(x+2)=(2b+1)(2a+3)=2(2ab+3b+a+1)+1, odd.\nReverse: if y(x+2) is odd, neither factor can be even (an even factor makes the product even). Thus y and x+2 are odd. Subtracting the even number 2 shows x is odd.'),
    ('f','Proofs','Prove at least three of any 25 chosen days fall in the same month of the year.', 'There are 12 month categories. If each contained at most two chosen days, the total would be at most 24. Since 25>24, some month contains at least three (pigeonhole principle).'),
    ('g','Proofs','Prove x²−5y²=8 has no integer solutions.', 'Reduce modulo 5: x²≡8≡3 (mod 5). For residues x=0,1,2,3,4, the squares are 0,1,4,4,1. None is 3. Contradiction.')]:
    add(2, '3'+ref, topic, 1, q, a)

add(2, '4.1', 'Proofs', 2,
    'Using only commutativity, associativity, identities, inverses, and substitution, prove uniqueness of additive inverse: a+b=0 and a+c=0 imply b=c.',
    'b = b+0                         [additive identity]\n  = b+(a+c)                     [substitute a+c=0]\n  = (b+a)+c                     [associativity]\n  = (a+b)+c                     [commutativity]\n  = 0+c                         [substitute a+b=0]\n  = c+0                         [commutativity]\n  = c.                          [additive identity]')
add(2, '4.2', 'Proofs', 2,
    'Derive 0·a=0 and a·0=0 using only the given field axioms. Do not assume cancellation of addition without proving it.',
    'Set z=a·0.\nz = a·(0+0)                     [identity 0+0=0, substitution]\n  = a·0+a·0 = z+z.              [distributivity; definition of z]\nAdd −z to z=z+z:\nz+(−z) = (z+z)+(−z)            [add equals]\n0 = (z+z)+(−z)                 [inverse]\n  = z+(z+(−z))                 [associativity]\n  = z+0                        [inverse]\n  = z.                         [identity]\nThus a·0=0. Commutativity gives 0·a=a·0=0.')
add(2, '4.3', 'Proofs', 2,
    'Using only field axioms, prove: if a≠0 and a·b=a·c, then b=c.',
    'Because a≠0, its inverse a⁻¹ exists.\na·a⁻¹=1                       [inverse]\na⁻¹·a=1                       [commutativity]\na⁻¹·(a·b)=a⁻¹·(a·c)           [multiply given equality]\n(a⁻¹·a)·b=(a⁻¹·a)·c           [associativity on each side]\n1·b=1·c                       [substitute a⁻¹·a=1]\nb·1=c·1                       [commutativity on each side]\nb=c.                          [multiplicative identities]')
add(2, '4.4', 'Proofs', 2,
    'Using only the field axioms and previously proved facts, prove (−1)·a=−a.',
    'a+(−1)·a\n = a·1+(−1)·a                 [multiplicative identity]\n = a·1+a·(−1)                 [commutativity of multiplication]\n = a·(1+(−1))                 [distributivity, reversed]\n = a·0                        [additive inverse of 1]\n = 0.                         [previously proved zero product]\nAlso a+(−a)=0 by the inverse axiom. Uniqueness of additive inverse (4.1) therefore yields (−1)·a=−a.')
add(2, '5a', 'Sets', 2,
    'Prove A∪(B∩C) ⊆ (A∪B)∩(A∪C) by element chasing.',
    'Let x∈A∪(B∩C). If x∈A, then x∈A∪B and x∈A∪C. Otherwise x∈B∩C, so x∈B and x∈C; again x belongs to both unions. Thus x∈(A∪B)∩(A∪C). Since x was arbitrary, the inclusion follows.')
add(2, '5b', 'Sets', 2,
    'Prove (A∪B)∩(A∪C) ⊆ A∪(B∩C) by element chasing.',
    'Let x belong to the intersection. Then x∈A∪B and x∈A∪C. If x∈A, it already belongs to A∪(B∩C). If x∉A, the first union forces x∈B and the second forces x∈C. Thus x∈B∩C, so x∈A∪(B∩C). Together with the opposite inclusion, this proves the distributive identity.')
for ref, q, a in [
    ('a','f:Z→Z, f(n)=n−2.', 'Injective: a−2=b−2 implies a=b. Onto: given y∈Z, choose n=y+2∈Z, so f(n)=y. Thus bijective, with inverse f⁻¹(y)=y+2.'),
    ('b','g:R→[0,∞), g(x)=x².', 'Not injective: g(1)=g(−1)=1. Onto the stated codomain: every y≥0 has preimage √y∈R. Thus not bijective and has no two-sided inverse on this domain. Choosing √y gives a right inverse, but it does not recover negative inputs.'),
    ('c','p:N→N, p(n)=n+2+(−1)ⁿ. Discuss either convention for N.', 'For even n, p(n)=n+3 (odd); for odd n, p(n)=n+1 (even). Equal outputs must have inputs of the same parity; then cancellation yields equal inputs. Thus injective.\nIf N={0,1,...}, the image is {2,3,4,...}, missing 0 and 1. If N={1,2,...}, the image is {2,4,5,6,...}, missing 1 and 3. Thus not onto for either convention, not bijective, and no inverse on all N. On the image, even y has preimage y−1 and odd y has preimage y−3.'),
    ('d','s:(−∞,−2)∪(2,∞)→R, s(x)=(x+1)/(x+2).', 'Write s(x)=1−1/(x+2). If s(a)=s(b), cross-multiplication gives (a+1)(b+2)=(b+1)(a+2), hence a=b. Thus injective.\nFor x<−2, the image is (1,∞). For x>2, the image is (3/4,1). Thus the full image is (3/4,1)∪(1,∞), not R. Hence not onto, not bijective, and no inverse defined on all R.\nOn its image only, solving y=(x+1)/(x+2) yields s⁻¹(y)=(1−2y)/(y−1).')]:
    add(2, '6'+ref, 'Functions', 2, 'Determine injectivity, surjectivity, bijectivity, and inverse existence. Prove your claims.\n'+q, a)
add(2, '7', 'Sets', 2,
    'If A is countably infinite and B is finite, prove A∪B is countably infinite by giving a bijection.',
    'Let N={0,1,...} and let f:A→N be a bijection. List the distinct new elements B\\A={b₀,...,bₘ₋₁}. Define h:A∪B→N by h(bᵢ)=i for 0≤i<m, and h(a)=m+f(a) for a∈A.\nThese definitions have disjoint domains. Their images are {0,...,m−1} and {m,m+1,...}; each branch is injective. Thus h is injective and onto N, proving countable infinitude. If B\\A is empty, m=0 and h=f. For N starting at 1, shift indices by 1.')

if __name__ == '__main__':
    Path(__file__).with_name('homework.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2)+'\n')
    print(f'Built {len(cards)} homework cards.')
