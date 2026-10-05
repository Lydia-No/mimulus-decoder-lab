from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import reference as model


class PossibilityMachineV0Tests(unittest.TestCase):
    def test_forward_reachability_matches_known_answer(self):
        nodes = model.enumerate_nodes()
        grouped = model.histories_by_state(nodes)
        self.assertEqual(
            list(grouped),
            ["0000", "0100", "1000", "1100", "1110", "1111"],
        )
        self.assertEqual(len(grouped), 6)
        self.assertEqual(len(nodes), 8)

    def test_convergent_state_preserves_distinct_histories(self):
        histories = model.inverse_histories("1110")
        self.assertEqual(
            set(histories),
            {
                ("set_a", "set_b", "set_c"),
                ("set_b", "set_a", "set_c"),
            },
        )

    def test_same_present_state_can_have_different_future_reachability(self):
        state = (1, 1, 1, 0)
        self.assertTrue(
            model.target_reachable_from(
                state, ("set_a", "set_b", "set_c")
            )
        )
        self.assertFalse(
            model.target_reachable_from(
                state, ("set_b", "set_a", "set_c")
            )
        )

    def test_intervention_removing_history_gate_reopens_future(self):
        state = (1, 1, 1, 0)
        history = ("set_b", "set_a", "set_c")
        self.assertTrue(
            model.target_reachable_from(
                state, history, history_gate=False
            )
        )

    def test_invariants_hold(self):
        self.assertEqual(model.check_invariants(model.enumerate_nodes()), [])


if __name__ == "__main__":
    unittest.main()
