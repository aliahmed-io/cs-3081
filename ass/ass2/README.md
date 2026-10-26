# CS3081 Artificial Intelligence — Assignment 2
## Resolution Hackathon: The Case of the Missing Exam Paper

- **Student Name:** Ali Ahmed
- **Student ID:** S24109004
- **Course:** CS3081 — Artificial Intelligence
- **Instructor:** Dr. Naila Marir
- **Institution:** Effat University, College of Engineering
- **Deliverables:**
  - [Solved Worksheet PDF](./Resolution_Hackathon_Solved_Ali_Ahmed_S24109004.pdf)
  - [Hackathon Presentation Slides (.pptx)](./Resolution%20Hackathon%20-%20Ali%20Ahmed.pptx)
  - [Automated Resolution Solver (`resolution_solver.py`)](./resolution_solver.py)

---

### System Enhancement Brief
- **Summary:** This project provides an end-to-end, mathematically rigorous solution to the CS3081 Resolution Hackathon ("The Case of the Missing Exam Paper"). Using formal propositional logic, Conjunctive Normal Form (CNF) transformations, refutation resolution (proof by contradiction), and exhaustive truth-table model checking across all $2^9 = 512$ interpretations, the investigation formally proves that Omar stole the exam paper ($KB \models O$), Sara is innocent ($KB \models \neg S$), the office door was not forced ($KB \models \neg F$), and accusations against Lina cannot be proven true or false ($KB \not\models L$ and $KB \not\models \neg L$).
- **Impact:**
  - Establishes mathematical certainty for criminal guilt and innocence via refutation resolution.
  - Formally identifies and debugs illegal multi-literal resolution shortcuts (the Dominoes Trap Pair).
  - Clarifies the boundary between lack of proof and proof of innocence through open-world model independence.
- **Technical Changes:**
  - Implemented an automated propositional logic resolution engine (`resolution_solver.py`) with literal factoring, clause reduction, and refutation trace generation.
  - Constructed an exhaustive $2^9$ model validator verifying semantic entailment against syntactic refutations.
- **Metric to Monitor:** $100\%$ refutation convergence rate (deriving the empty clause `()` in $\le 4$ inference steps for entailed queries) and $0$ false-positive contradiction traps.

---

## 1. Case Overview & Incident Report

### Incident Log
On Monday at 08:00, the CS3081 final exam paper was discovered missing from the instructor's locked office. Security footage and swipe logs identified three students near the office on Sunday night:
- **Sara** ($S$)
- **Omar** ($O$)
- **Lina** ($L$)

Campus security collected 7 evidence clues. The objective is to use propositional resolution to determine:
1. Who took the exam paper?
2. Who is innocent?
3. Which accusation cannot be proven?

### Propositional Symbol Table

| Symbol | Propositional Meaning |
| :---: | :--- |
| **$D$** | The office door was unlocked |
| **$S$** | Sara took the exam paper |
| **$O$** | Omar took the exam paper |
| **$L$** | Lina took the exam paper |
| **$C$** | The security camera was switched off |
| **$F$** | The office door was forced open |
| **$Y$** | Lina had a copy of the office key |
| **$K$** | Khalid lent his office key |
| **$A$** | The alarm rang |

### Raw Clues from Campus Security

| # | Clue (English Description) | Propositional Logic |
| :-: | :--- | :--- |
| **1** | If the door was unlocked, then Sara or Omar took the paper. | $D \rightarrow (S \lor O)$ |
| **2** | The door was unlocked. | $D$ |
| **3** | If Sara took the paper or the door was forced, then the camera was off. | $(S \lor F) \rightarrow C$ |
| **4** | The camera was NOT off (it recorded all night). | $\neg C$ |
| **5** | Lina could only have taken it if she had a copy of the key. | $L \rightarrow Y$ |
| **6** | Lina had a copy of the key if and only if Khalid lent his key. | $Y \leftrightarrow K$ |
| **7** | It is not true that Khalid lent his key AND the alarm rang. | $\neg (K \land A)$ |

---

## 2. Level 01: CNF Relay

Each compound clue is transformed into Conjunctive Normal Form (CNF) using formal equivalence rules:

### Clue 1: $D \rightarrow (S \lor O)$
1. **Eliminate $\rightarrow$:** $\neg D \lor (S \lor O)$
2. **Associativity:** $\neg D \lor S \lor O$
3. **Final CNF:** $(\neg D \lor S \lor O)$ [Yields **1 clause**]

### Clue 3: $(S \lor F) \rightarrow C$
1. **Eliminate $\rightarrow$:** $\neg(S \lor F) \lor C$
2. **De Morgan's Law:** $(\neg S \land \neg F) \lor C$
3. **Distribution of $\lor$ over $\land$:** $(\neg S \lor C) \land (\neg F \lor C)$ [Yields **2 clauses**]

### Clue 6: $Y \leftrightarrow K$
1. **Eliminate $\leftrightarrow$:** $(Y \rightarrow K) \land (K \rightarrow Y)$
2. **Eliminate $\rightarrow$:** $(\neg Y \lor K) \land (\neg K \lor Y)$
3. **Final CNF:** $(\neg Y \lor K) \land (\neg K \lor Y)$ [Yields **2 clauses**]

### Clue 7: $\neg(K \land A)$
1. **De Morgan's Law:** $\neg K \lor \neg A$
2. **Final CNF:** $(\neg K \lor \neg A)$ [Yields **1 clause**]

### Compiled Knowledge Base ($KB$) in CNF

| Clause ID | CNF Clause | Source Clue | Description |
| :---: | :---: | :---: | :--- |
| **$K1$** | $\neg D \lor S \lor O$ | Clue 1 | If unlocked, Sara or Omar took paper |
| **$K2$** | $D$ | Clue 2 | Door was unlocked |
| **$K3$** | $\neg S \lor C$ | Clue 3 | If Sara took paper, camera was off |
| **$K4$** | $\neg F \lor C$ | Clue 3 | If door was forced, camera was off |
| **$K5$** | $\neg C$ | Clue 4 | Camera was NOT off |
| **$K6$** | $\neg L \lor Y$ | Clue 5 | If Lina took paper, she had key copy |
| **$K7$** | $\neg Y \lor K$ | Clue 6 | If Lina had key copy, Khalid lent key |
| **$K8$** | $\neg K \lor Y$ | Clue 6 | If Khalid lent key, Lina had key copy |
| **$K9$** | $\neg K \lor \neg A$ | Clue 7 | Not both Khalid lent key and alarm rang |
| **$K10$** | *(Reserved)* | Level 03 | Negated goal $\neg \alpha$ added for refutation |

---

## 3. Level 02: Resolution Dominoes & Bug Report

12 clause cards are matched using complementary literals ($P$ and $\neg P$). Each card belongs to exactly one pair:

| Pair # | Card 1 + Card 2 | Resolved Literal | Resolvent Clause | Factoring Applied? |
| :---: | :---: | :---: | :---: | :---: |
| **1** | **CARD_B** $(\neg T \lor U)$ + **CARD_G** $(T \lor U)$ | $T$ | $U \lor U \Rightarrow U$ | **Yes** (Factored duplicate $U$) |
| **2** | **CARD_C** $(\neg Q \lor R)$ + **CARD_H** $(P \lor Q)$ | $Q$ | $P \lor R$ | **No** |
| **3** | **CARD_D** $(X \lor \neg Y \lor Z)$ + **CARD_J** $(Y \lor W)$ | $Y$ | $X \lor Z \lor W$ | **No** |
| **4** | **CARD_E** $(M)$ + **CARD_L** $(\neg M)$ | $M$ | $( )$ **[Empty Clause]** | **No** |
| **5** | **CARD_F** $(A \lor B \lor S)$ + **CARD_K** $(\neg A \lor R \lor S)$ | $A$ | $B \lor S \lor R \lor S \Rightarrow B \lor R \lor S$ | **Yes** (Factored duplicate $S$) |
| **6** | **CARD_A** $(G \lor H)$ + **CARD_I** $(\neg G \lor \neg H)$ | $G$ | $H \lor \neg H$ **[Tautology]** | **No [TRAP PAIR]** |

### ⚠ Bug Report: The Trap Pair
- **Trap Identification:** Pair 6 consisting of **CARD_A** $(G \lor H)$ and **CARD_I** $(\neg G \lor \neg H)$.
- **Why it does NOT produce the empty clause $( )$:**
  A sound resolution step is defined on **exactly one complementary pair of literals** at a time. Resolving on $G$ cancels $G$ and $\neg G$, which yields the resolvent clause $(H \lor \neg H)$. The formula $(H \lor \neg H)$ is a propositional **tautology** (identically true in every model), not the empty clause $( )$. Cancelling both $G$ and $H$ simultaneously in a single resolution operation is an **illegal deduction rule** that violates logical soundness.

---

## 4. Level 03: Solve the Case (Proof by Contradiction)

To prove $KB \models \alpha$, we add the negated goal $K10 = \neg \alpha$ to $KB$ and systematically resolve until deriving the empty clause $( )$.

### Case 3A: Did Omar take the paper? (Prove $KB \models O$)
- **Goal:** $O$
- **Add to KB:** $K10 = \neg O$

| Step | Clause 1 | Clause 2 | Resolved Literal | Resolvent Clause |
| :---: | :---: | :---: | :---: | :--- |
| **$R1$** | $K1$ $(\neg D \lor S \lor O)$ | $K2$ $(D)$ | $D$ | $S \lor O$ |
| **$R2$** | $R1$ $(S \lor O)$ | $K10$ $(\neg O)$ | $O$ | $S$ |
| **$R3$** | $K3$ $(\neg S \lor C)$ | $K5$ $(\neg C)$ | $C$ | $\neg S$ |
| **$R4$** | $R2$ $(S)$ | $R3$ $(\neg S)$ | $S$ | $( )$ **[EMPTY CLAUSE]** |

- **Verdict:** Contradiction reached ($( )$ derived). **$KB \models O$ is PROVEN.** Omar took the exam paper.

---

### Case 3B: Is Sara innocent? (Prove $KB \models \neg S$)
- **Goal:** $\neg S$
- **Add to KB:** $K10 = \neg(\neg S) \equiv S$

| Step | Clause 1 | Clause 2 | Resolved Literal | Resolvent Clause |
| :---: | :---: | :---: | :---: | :--- |
| **$R1$** | $K10$ $(S)$ | $K3$ $(\neg S \lor C)$ | $S$ | $C$ |
| **$R2$** | $R1$ $(C)$ | $K5$ $(\neg C)$ | $C$ | $( )$ **[EMPTY CLAUSE]** |

- **Verdict:** Contradiction reached ($( )$ derived). **$KB \models \neg S$ is PROVEN.** Sara is innocent.

---

### Case 3C (Boss Fight): What about Lina?
During interrogation, Omar claimed: *"Lina did it with me!"* while Lina asserted: *"I am innocent!"*

#### Attempt 1: Add $\neg L$ to KB (Try to prove $L$)
- **Add to KB:** $K10 = \neg L$
- **Derivations:**
  - $R1$: Resolve $K6$ $(\neg L \lor Y)$ with $K7$ $(\neg Y \lor K)$ on $Y \Rightarrow \neg L \lor K$
  - $R2$: Resolve $R1$ $(\neg L \lor K)$ with $K9$ $(\neg K \lor \neg A)$ on $K \Rightarrow \neg L \lor \neg A$
  - $R3$: Resolve $K4$ $(\neg F \lor C)$ with $K5$ $(\neg C)$ on $C \Rightarrow \neg F$
- **Resolution Limit:** The literal $L$ appears in the knowledge base exclusively as a negative literal ($\neg L$ in $K6$). There is no positive literal $L$ anywhere in $KB$ to cancel against $K10 = \neg L$. The clause set saturates with no new clauses.
- **Outcome:** No empty clause can be produced $\implies \mathbf{KB \not\models L}$.

#### Attempt 2: Add $L$ to KB (Try to prove $\neg L$)
- **Add to KB:** $K10 = L$
- **Derivations:**
  - $R1$: Resolve $K10$ $(L)$ with $K6$ $(\neg L \lor Y)$ on $L \Rightarrow Y$
  - $R2$: Resolve $R1$ $(Y)$ with $K7$ $(\neg Y \lor K)$ on $Y \Rightarrow K$
  - $R3$: Resolve $R2$ $(K)$ with $K9$ $(\neg K \lor \neg A)$ on $K \Rightarrow \neg A$
- **Resolution Limit:** The resolvent $\neg A$ cannot be resolved further because positive literal $A$ is absent from the entire knowledge base. The chain terminates.
- **Outcome:** No empty clause can be produced $\implies \mathbf{KB \not\models \neg L}$.

#### Conclusion on Lina
- **Can detectives accuse Lina?** No ($KB \not\models L$).
- **Can detectives clear Lina?** No ($KB \not\models \neg L$).
- **Entailment Analysis:** The proposition $L$ is **logically independent** of the knowledge base. There exist consistent models where $L = \text{True}$ and models where $L = \text{False}$. Failing to prove guilt is not proof of innocence; Omar's accusation remains legally and logically unproven.

---

### ★ Side Quest: Prove the door was not forced (Prove $KB \models \neg F$)
- **Goal:** $\neg F$
- **Add to KB:** $K10 = \neg(\neg F) \equiv F$

| Step | Clause 1 | Clause 2 | Resolved Literal | Resolvent Clause |
| :---: | :---: | :---: | :---: | :--- |
| **$R1$** | $K10$ $(F)$ | $K4$ $(\neg F \lor C)$ | $F$ | $C$ |
| **$R2$** | $R1$ $(C)$ | $K5$ $(\neg C)$ | $C$ | $( )$ **[EMPTY CLAUSE]** |

- **Verdict:** Contradiction reached ($( )$ derived). **$KB \models \neg F$ is PROVEN.** The office door was not forced open.

---

## 5. Level 04: Final Accusation & Post-Mortem

### Final Case Summary

```
                                 THE FINAL VERDICTS
  ┌──────────────────┬──────────────────┬───────────────────────────────────────────┐
  │ Suspect / Claim  │ Formal Entailment│ Legal & Factual Verdict                   │
  ├──────────────────┼──────────────────┼───────────────────────────────────────────┤
  │ Omar             │ KB ⊨ O           │ GUILTY: Took the exam paper               │
  │ Sara             │ KB ⊨ ¬S          │ INNOCENT: Fully exonerated by camera logs │
  │ Lina             │ KB ⊭ L, KB ⊭ ¬L  │ UNPROVEN: Insufficient evidence either way│
  │ Door Forced Open │ KB ⊨ ¬F          │ NOT FORCED: Door was unlocked normally    │
  └──────────────────┴──────────────────┴───────────────────────────────────────────┘
```

### Post-Mortem Reflections
1. **Why is resolution called a "proof by contradiction"?**
   > Resolution operates on refutation: to prove that a query $\alpha$ necessarily follows from a knowledge base $KB$, we hypothesize its negation $\neg \alpha$. If $KB \land \neg \alpha$ derives the empty clause $( )$, it proves that no model can satisfy both the premises and the falsehood of $\alpha$; hence, $\alpha$ must hold in all valid models ($KB \models \alpha$).

2. **What does it mean when no empty clause can ever be produced?**
   > When resolution inference saturates (no new resolvent clauses can be derived) without generating $( )$, it proves that $KB \land \neg \alpha$ is logically satisfiable. Therefore, there exists at least one possible world where the premises are true but $\alpha$ is false, confirming that $KB$ does not entail $\alpha$ ($KB \not\models \alpha$).

---

## 6. Truth Table Model Checking Verification

The knowledge base over the 9 propositions ($D, S, O, L, C, F, Y, K, A$) defines $2^9 = 512$ possible truth assignments. Exhaustive model evaluation reveals that exactly **4 models** satisfy $KB$:

```
Model 1: D=T, S=F, O=T, L=F, C=F, F=F, Y=F, K=F, A=F
Model 2: D=T, S=F, O=T, L=F, C=F, F=F, Y=F, K=F, A=T
Model 3: D=T, S=F, O=T, L=F, C=F, F=F, Y=T, K=T, A=F
Model 4: D=T, S=F, O=T, L=T, C=F, F=F, Y=T, K=T, A=F
```

- In **100%** of satisfying models ($4/4$): $O = \text{True}$ $\implies KB \models O$.
- In **100%** of satisfying models ($4/4$): $S = \text{False}$ $\implies KB \models \neg S$.
- In **100%** of satisfying models ($4/4$): $F = \text{False}$ $\implies KB \models \neg F$.
- $L$ is $\text{False}$ in Models 1–3, but $\text{True}$ in Model 4 $\implies KB \not\models L$ and $KB \not\models \neg L$.

---

## 7. How to Execute the Resolution Solver

Execute the verified Python solver directly from the terminal:

```bash
# Run from repository root
python ass/ass2/resolution_solver.py

# Or run directly inside the folder
python resolution_solver.py
```
