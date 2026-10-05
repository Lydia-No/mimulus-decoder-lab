"""Reference enumerator for Possibility Machine v0.

Synthetic known-answer only. This file deliberately uses the Python standard
library and keeps state, history and intervention separate so the same fixture
can later be represented in Wolfram/Maude, Alloy/SMT, beQube and a verifier.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Iterable

State = tuple[int, int, int, int]
History = tuple[str, ...]
Node = tuple[State, History]

INITIAL: State = (0, 0, 0, 0)
TARGET: State = (1, 1, 1, 1)


@dataclass(frozen=True)
class Transition:
    event: str
    after: State


def bits(state: State) -> str:
    return "".join(str(v) for v in state)


def a_before_b(history: History) -> bool:
    return (
        "set_a" in history
        and "set_b" in history
        and history.index("set_a") < history.index("set_b")
    )


def successors(
    state: State,
    history: History,
    *,
    history_gate: bool = True,
) -> list[Transition]:
    """Return enabled monotone transitions.

    `history_gate=False` is the explicit counterfactual intervention that removes
    the path-sensitive condition from set_d while leaving the present-state rule
    C=1 unchanged.
    """

    a, b, c, d = state
    out: list[Transition] = []

    if a == 0:
        out.append(Transition("set_a", (1, b, c, d)))
    if b == 0:
        out.append(Transition("set_b", (a, 1, c, d)))
    if c == 0 and a == 1 and b == 1:
        out.append(Transition("set_c", (a, b, 1, d)))

    gate_ok = (not history_gate) or a_before_b(history)
    if d == 0 and c == 1 and gate_ok:
        out.append(Transition("set_d", (a, b, c, 1)))

    return out


def enumerate_nodes(*, history_gate: bool = True) -> set[Node]:
    """Enumerate all reachable (present state, explicit history) nodes."""

    start: Node = (INITIAL, ())
    queue: deque[Node] = deque([start])
    seen: set[Node] = {start}

    while queue:
        state, history = queue.popleft()
        for transition in successors(state, history, history_gate=history_gate):
            node = (transition.after, history + (transition.event,))
            if node not in seen:
                seen.add(node)
                queue.append(node)

    return seen


def histories_by_state(nodes: Iterable[Node]) -> dict[str, list[History]]:
    grouped: dict[str, list[History]] = defaultdict(list)
    for state, history in nodes:
        grouped[bits(state)].append(history)
    for histories in grouped.values():
        histories.sort()
    return dict(sorted(grouped.items()))


def target_reachable_from(
    state: State,
    history: History,
    *,
    history_gate: bool = True,
) -> bool:
    """Whether TARGET remains reachable from one concrete state-history node."""

    queue: deque[Node] = deque([(state, history)])
    seen: set[Node] = {(state, history)}

    while queue:
        current, current_history = queue.popleft()
        if current == TARGET:
            return True
        for transition in successors(
            current, current_history, history_gate=history_gate
        ):
            node = (transition.after, current_history + (transition.event,))
            if node not in seen:
                seen.add(node)
                queue.append(node)

    return False


def inverse_histories(observed_state: str) -> list[History]:
    """Return all reachable histories compatible with an observed current state."""

    grouped = histories_by_state(enumerate_nodes())
    return grouped.get(observed_state, [])


def check_invariants(nodes: Iterable[Node]) -> list[str]:
    failures: list[str] = []

    for state, history in nodes:
        a, b, c, d = state
        if c and not (a and b):
            failures.append(f"C_WITHOUT_AB:{bits(state)}:{history}")
        if d and not c:
            failures.append(f"D_WITHOUT_C:{bits(state)}:{history}")
        if state == TARGET and not a_before_b(history):
            failures.append(f"TARGET_WITHOUT_A_BEFORE_B:{history}")

    return failures


def summary() -> dict[str, object]:
    nodes = enumerate_nodes()
    grouped = histories_by_state(nodes)
    witness_state: State = (1, 1, 1, 0)
    forward_history: History = ("set_a", "set_b", "set_c")
    reverse_history: History = ("set_b", "set_a", "set_c")

    return {
        "raw_state_count": 16,
        "reachable_current_states": list(grouped),
        "reachable_current_state_count": len(grouped),
        "reachable_state_history_nodes": len(nodes),
        "inverse_1110_histories": [list(h) for h in inverse_histories("1110")],
        "path_sensitive_witness": {
            "present_state": bits(witness_state),
            "a_then_b_target_reachable": target_reachable_from(
                witness_state, forward_history
            ),
            "b_then_a_target_reachable": target_reachable_from(
                witness_state, reverse_history
            ),
            "b_then_a_after_gate_removal": target_reachable_from(
                witness_state, reverse_history, history_gate=False
            ),
        },
        "invariant_failures": check_invariants(nodes),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(summary(), indent=2))
