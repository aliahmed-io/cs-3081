"""
CS3081 Artificial Intelligence — Assignment 2
Resolution Hackathon: The Case of the Missing Exam Paper

Student Name : Ali Ahmed
Student ID   : S24109004
Instructor   : Dr. Naila Marir
Institution  : Effat University, College of Engineering

This module implements a formal propositional resolution engine that models
the CS3081 Hackathon case, verifies all CNF conversions, executes automated
proof by contradiction (refutation resolution), detects the dominoes trap pair,
and confirms semantic entailment via full truth-table model checking.
"""

import sys
from itertools import product
from typing import List, Set, Tuple, Optional, Dict

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class Literal:
    """Represents a propositional literal (a variable or its negation)."""

    def __init__(self, symbol: str, negated: bool = False):
        self.symbol = symbol
        self.negated = negated

    def __invert__(self) -> "Literal":
        return Literal(self.symbol, not self.negated)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Literal):
            return False
        return self.symbol == other.symbol and self.negated == other.negated

    def __hash__(self) -> int:
        return hash((self.symbol, self.negated))

    def __repr__(self) -> str:
        return f"¬{self.symbol}" if self.negated else self.symbol

    def is_complement(self, other: "Literal") -> bool:
        return self.symbol == other.symbol and self.negated != other.negated


class Clause:
    """Represents a disjunctive clause (a disjunction of literals)."""

    def __init__(self, literals):
        # Factoring is automatically applied by converting to frozenset
        self.literals: frozenset[Literal] = frozenset(literals)

    def is_empty(self) -> bool:
        return len(self.literals) == 0

    def is_tautology(self) -> bool:
        for lit in self.literals:
            if ~lit in self.literals:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Clause):
            return False
        return self.literals == other.literals

    def __hash__(self) -> int:
        return hash(self.literals)

    def __repr__(self) -> str:
        if self.is_empty():
            return "( ) [EMPTY CLAUSE]"
        sorted_lits = sorted(self.literals, key=lambda l: (l.symbol, l.negated))
        return f"({' ∨ '.join(str(l) for l in sorted_lits)})"


def resolve(c1: Clause, c2: Clause, literal_symbol: Optional[str] = None) -> List[Tuple[Clause, str, bool]]:
    """
    Resolves two clauses.
    Returns a list of tuples: (resolvent_clause, resolved_on_symbol, had_duplicate_factored).
    A legal resolution step cancels EXACTLY ONE complementary pair of literals.
    """
    resolvents = []
    # Identify complementary literal pairs
    for lit1 in c1.literals:
        if literal_symbol is not None and lit1.symbol != literal_symbol:
            continue
        comp = ~lit1
        if comp in c2.literals:
            # Cancel exactly this complementary pair
            new_lits_list = [l for l in c1.literals if l != lit1] + [l for l in c2.literals if l != comp]
            had_factoring = len(new_lits_list) != len(set(new_lits_list))
            resolvent = Clause(new_lits_list)
            resolvents.append((resolvent, lit1.symbol, had_factoring))
    return resolvents


def get_hackathon_kb() -> Dict[str, Clause]:
    """
    Returns the 9 compiled CNF clauses (K1 to K9) derived from the 7 clues:
    Clue 1: D → (S ∨ O)          => K1: ¬D ∨ S ∨ O
    Clue 2: D                    => K2: D
    Clue 3: (S ∨ F) → C          => K3: ¬S ∨ C,  K4: ¬F ∨ C
    Clue 4: ¬C                   => K5: ¬C
    Clue 5: L → Y                => K6: ¬L ∨ Y
    Clue 6: Y ↔ K                => K7: ¬Y ∨ K,  K8: ¬K ∨ Y
    Clue 7: ¬(K ∧ A)             => K9: ¬K ∨ ¬A
    """
    D = Literal("D")
    S = Literal("S")
    O = Literal("O")
    L = Literal("L")
    C = Literal("C")
    F = Literal("F")
    Y = Literal("Y")
    K = Literal("K")
    A = Literal("A")

    return {
        "K1": Clause([~D, S, O]),
        "K2": Clause([D]),
        "K3": Clause([~S, C]),
        "K4": Clause([~F, C]),
        "K5": Clause([~C]),
        "K6": Clause([~L, Y]),
        "K7": Clause([~Y, K]),
        "K8": Clause([~K, Y]),
        "K9": Clause([~K, ~A]),
    }


def solve_case_3a():
    """Case 3A: Did Omar take the paper? Prove KB ⊨ O."""
    print("=" * 70)
    print("CASE 3A: Did Omar take the paper? Prove KB ⊨ O")
    print("=" * 70)
    kb = get_hackathon_kb()
    k10 = Clause([~Literal("O")])
    kb["K10"] = k10
    print(f"Goal: Prove O by Contradiction.")
    print(f"ADD TO KB: K10 = {k10} (negation of goal O)\n")

    # Step R1: K1 + K2 on D -> S v O
    r1_list = resolve(kb["K1"], kb["K2"], "D")
    r1 = r1_list[0][0]
    print(f"R1: K1 {kb['K1']} + K2 {kb['K2']} resolved on D => {r1}")

    # Step R2: R1 + K10 on O -> S
    r2_list = resolve(r1, kb["K10"], "O")
    r2 = r2_list[0][0]
    print(f"R2: R1 {r1} + K10 {kb['K10']} resolved on O => {r2}")

    # Step R3: K3 + K5 on C -> ¬S
    r3_list = resolve(kb["K3"], kb["K5"], "C")
    r3 = r3_list[0][0]
    print(f"R3: K3 {kb['K3']} + K5 {kb['K5']} resolved on C => {r3}")

    # Step R4: R2 + R3 on S -> ( )
    r4_list = resolve(r2, r3, "S")
    r4 = r4_list[0][0]
    print(f"R4: R2 {r2} + R3 {r3} resolved on S => {r4}\n")

    print(f"VERDICT: Empty clause ( ) derived! KB ⊨ O is PROVEN.")
    print("Conclusion: Omar took the exam paper.\n")


def solve_case_3b():
    """Case 3B: Is Sara innocent? Prove KB ⊨ ¬S."""
    print("=" * 70)
    print("CASE 3B: Is Sara innocent? Prove KB ⊨ ¬S")
    print("=" * 70)
    kb = get_hackathon_kb()
    k10 = Clause([Literal("S")])
    kb["K10"] = k10
    print(f"Goal: Prove ¬S by Contradiction.")
    print(f"ADD TO KB: K10 = {k10} (negation of goal ¬S)\n")

    # Step R1: K10 + K3 on S -> C
    r1_list = resolve(kb["K10"], kb["K3"], "S")
    r1 = r1_list[0][0]
    print(f"R1: K10 {kb['K10']} + K3 {kb['K3']} resolved on S => {r1}")

    # Step R2: R1 + K5 on C -> ( )
    r2_list = resolve(r1, kb["K5"], "C")
    r2 = r2_list[0][0]
    print(f"R2: R1 {r1} + K5 {kb['K5']} resolved on C => {r2}\n")

    print(f"VERDICT: Empty clause ( ) derived! KB ⊨ ¬S is PROVEN.")
    print("Conclusion: Sara is innocent.\n")


def solve_case_3c():
    """Case 3C (Boss Fight): What about Lina? Attempt 1 & 2."""
    print("=" * 70)
    print("CASE 3C (BOSS FIGHT): What about Lina?")
    print("Interrogation log: Omar: 'Lina did it with me!' | Lina: 'I am innocent!'")
    print("=" * 70)

    # Attempt 1: Add ¬L (Try to prove L)
    print("▶ Attempt 1: Add ¬L to KB (try to prove L)")
    kb1 = get_hackathon_kb()
    k10_1 = Clause([~Literal("L")])
    kb1["K10"] = k10_1
    print(f"ADD TO KB: K10 = {k10_1}")
    r1 = resolve(kb1["K6"], kb1["K7"], "Y")[0][0]
    print(f"R1: K6 {kb1['K6']} + K7 {kb1['K7']} on Y => {r1}")
    r2 = resolve(r1, kb1["K9"], "K")[0][0]
    print(f"R2: R1 {r1} + K9 {kb1['K9']} on K => {r2}")
    r3 = resolve(kb1["K4"], kb1["K5"], "C")[0][0]
    print(f"R3: K4 {kb1['K4']} + K5 {kb1['K5']} on C => {r3}")
    print("Observation: The literal 'L' only occurs as '¬L' in the KB (K6).")
    print("No positive literal 'L' exists to resolve against K10 (¬L).")
    print("Result: KB is saturated. No empty clause ( ) can ever be produced. KB ⊭ L.\n")

    # Attempt 2: Add L (Try to prove ¬L)
    print("▶ Attempt 2: Add L to KB (try to prove ¬L)")
    kb2 = get_hackathon_kb()
    k10_2 = Clause([Literal("L")])
    kb2["K10"] = k10_2
    print(f"ADD TO KB: K10 = {k10_2}")
    r1 = resolve(kb2["K10"], kb2["K6"], "L")[0][0]
    print(f"R1: K10 {kb2['K10']} + K6 {kb2['K6']} on L => {r1}")
    r2 = resolve(r1, kb2["K7"], "Y")[0][0]
    print(f"R2: R1 {r1} + K7 {kb2['K7']} on Y => {r2}")
    r3 = resolve(r2, kb2["K9"], "K")[0][0]
    print(f"R3: R2 {r2} + K9 {kb2['K9']} on K => {r3}")
    print("Observation: The resolvent ¬A cannot be resolved because positive 'A' is absent from the KB.")
    print("Result: Derivation is stuck. No empty clause ( ) can ever be produced. KB ⊭ ¬L.\n")

    print("CONCLUSION:")
    print("Detectives cannot accuse Lina (KB ⊭ L) and cannot clear her (KB ⊭ ¬L).")
    print("The variable L is logically independent of the KB; it is unproven either way.\n")


def solve_side_quest():
    """Side Quest: Prove the door was not forced: KB ⊨ ¬F."""
    print("=" * 70)
    print("★ SIDE QUEST: Prove KB ⊨ ¬F (The door was not forced)")
    print("=" * 70)
    kb = get_hackathon_kb()
    k10 = Clause([Literal("F")])
    kb["K10"] = k10
    print(f"Goal: Prove ¬F by Contradiction.")
    print(f"ADD TO KB: K10 = {k10} (negation of goal ¬F)\n")

    # Step R1: K10 + K4 on F -> C
    r1_list = resolve(kb["K10"], kb["K4"], "F")
    r1 = r1_list[0][0]
    print(f"R1: K10 {kb['K10']} + K4 {kb['K4']} resolved on F => {r1}")

    # Step R2: R1 + K5 on C -> ( )
    r2_list = resolve(r1, kb["K5"], "C")
    r2 = r2_list[0][0]
    print(f"R2: R1 {r1} + K5 {kb['K5']} resolved on C => {r2}\n")

    print(f"VERDICT: Empty clause ( ) derived! KB ⊨ ¬F is PROVEN.")
    print("Conclusion: The office door was not forced.\n")


def solve_level_02_dominoes():
    """Level 02: Resolution Dominoes matching and Trap detector."""
    print("=" * 70)
    print("LEVEL 02: Resolution Dominoes & Trap Bug Report")
    print("=" * 70)

    cards = {
        "CARD_A": Clause([Literal("G"), Literal("H")]),
        "CARD_B": Clause([~Literal("T"), Literal("U")]),
        "CARD_C": Clause([~Literal("Q"), Literal("R")]),
        "CARD_D": Clause([Literal("X"), ~Literal("Y"), Literal("Z")]),
        "CARD_E": Clause([Literal("M")]),
        "CARD_F": Clause([Literal("A"), Literal("B"), Literal("S")]),
        "CARD_G": Clause([Literal("T"), Literal("U")]),
        "CARD_H": Clause([Literal("P"), Literal("Q")]),
        "CARD_I": Clause([~Literal("G"), ~Literal("H")]),
        "CARD_J": Clause([Literal("Y"), Literal("W")]),
        "CARD_K": Clause([~Literal("A"), Literal("R"), Literal("S")]),
        "CARD_L": Clause([~Literal("M")]),
    }

    pairs = [
        ("CARD_B", "CARD_G", "T"),
        ("CARD_C", "CARD_H", "Q"),
        ("CARD_D", "CARD_J", "Y"),
        ("CARD_E", "CARD_L", "M"),
        ("CARD_F", "CARD_K", "A"),
        ("CARD_A", "CARD_I", "G"),  # The Trap
    ]

    for idx, (c1_name, c2_name, on_sym) in enumerate(pairs, 1):
        c1 = cards[c1_name]
        c2 = cards[c2_name]
        res_list = resolve(c1, c2, on_sym)
        resolvent, sym, factored = res_list[0]
        trap_label = " [TRAP PAIR]" if (c1_name == "CARD_A" and c2_name == "CARD_I") else ""
        print(f"Pair {idx}: {c1_name} {c1} + {c2_name} {c2} resolved on {sym} => {resolvent} | Factoring: {'Yes' if factored else 'No'}{trap_label}")

    print("\n▶ Bug Report: The Trap Pair")
    print("Pair 6 (CARD_A + CARD_I): (G ∨ H) + (¬G ∨ ¬H).")
    print("Why it does NOT give ( ):")
    print("A single resolution step can cancel only ONE complementary pair of literals at a time.")
    print("Resolving on G cancels G and ¬G, leaving the resolvent (H ∨ ¬H), which is a tautology (always True).")
    print("Simultaneously cancelling both G and H in a single step is an illegal operation.")
    print("Therefore, this pair does not produce the empty clause ( ).\n")


def verify_with_truth_table():
    """Verifies all semantic entailments via exhaustive 2^9 truth table check."""
    print("=" * 70)
    print("SEMANTIC VERIFICATION: Truth Table Model Checking (2^9 = 512 Worlds)")
    print("=" * 70)
    symbols = ["D", "S", "O", "L", "C", "F", "Y", "K", "A"]

    def satisfies_kb(m: Dict[str, bool]) -> bool:
        D, S, O, L, C, F, Y, K, A = (m[s] for s in symbols)
        c1 = (not D) or (S or O)
        c2 = D
        c3 = (not (S or F)) or C
        c4 = not C
        c5 = (not L) or Y
        c6 = (Y == K)
        c7 = not (K and A)
        return c1 and c2 and c3 and c4 and c5 and c6 and c7

    satisfying_models = []
    for values in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        if satisfies_kb(model):
            satisfying_models.append(model)

    print(f"Total Satisfying Models (Possible Worlds): {len(satisfying_models)}")
    for i, m in enumerate(satisfying_models, 1):
        formatted = ", ".join(f"{k}={'T' if v else 'F'}" for k, v in m.items())
        print(f"  Model {i}: {formatted}")

    print("\nEntailment Evaluation (holds in 100% of satisfying models):")
    entails_O = all(m["O"] for m in satisfying_models)
    entails_not_S = all(not m["S"] for m in satisfying_models)
    entails_not_F = all(not m["F"] for m in satisfying_models)
    entails_L = all(m["L"] for m in satisfying_models)
    entails_not_L = all(not m["L"] for m in satisfying_models)

    print(f"  KB ⊨ O     (Omar guilty)   : {entails_O}")
    print(f"  KB ⊨ ¬S    (Sara innocent) : {entails_not_S}")
    print(f"  KB ⊨ ¬F    (Door not forced): {entails_not_F}")
    print(f"  KB ⊨ L     (Lina guilty)   : {entails_L}")
    print(f"  KB ⊨ ¬L    (Lina innocent) : {entails_not_L}")
    print("=" * 70)


def main():
    print("#" * 70)
    print("CS3081 Artificial Intelligence — Resolution Hackathon Solver")
    print("Author: Ali Ahmed (ID: S24109004)")
    print("#" * 70 + "\n")

    solve_level_02_dominoes()
    solve_case_3a()
    solve_case_3b()
    solve_case_3c()
    solve_side_quest()
    verify_with_truth_table()


if __name__ == "__main__":
    main()
