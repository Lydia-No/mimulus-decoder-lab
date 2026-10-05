// Possibility Machine v0 — inverse/constraint view
// Synthetic known-answer only; non-canonical.
//
// Question: given present observation 1110, which histories are compatible?
// Expected compatible histories:
//   set_a -> set_b -> set_c
//   set_b -> set_a -> set_c
// The two histories disagree on whether baseline set_d remains reachable.

abstract sig Slot {}
one sig S0, S1, S2 extends Slot {}

abstract sig Event {}
one sig SetA, SetB, SetC extends Event {}

one sig History {
  at: Slot -> one Event
}

// `at` is a permutation: every slot contains exactly one event and every event
// appears in exactly one slot.
fact EventPermutation {
  all e: Event | one e.~(History.at)
}

pred occursAt[s: Slot, e: Event] {
  s->e in History.at
}

pred before[e1: Event, e2: Event] {
  (occursAt[S0, e1] and (occursAt[S1, e2] or occursAt[S2, e2]))
  or
  (occursAt[S1, e1] and occursAt[S2, e2])
}

// Observation 1110 means A, B and C have occurred while D has not.
// Baseline rules require C after both A and B, so C must be the third event.
pred compatible1110 {
  occursAt[S2, SetC]
}

// Under the baseline world, D remains reachable only if A occurred before B.
pred baselineDReachable {
  compatible1110
  before[SetA, SetB]
}

pred baselineDBlocked {
  compatible1110
  not before[SetA, SetB]
}

// Counterfactual intervention: remove the history-order gate from set_d.
// Once C=1, either compatible history can then reach D.
pred afterHistoryGateRemoval {
  compatible1110
}

// These commands should each produce a compatible instance.
run baselineDReachable for exactly 1 History, exactly 3 Slot, exactly 3 Event
run baselineDBlocked for exactly 1 History, exactly 3 Slot, exactly 3 Event
run afterHistoryGateRemoval for exactly 1 History, exactly 3 Slot, exactly 3 Event

// There must not be a compatible history where C occurs before A or B.
assert CIsLastInCompatible1110 {
  compatible1110 implies (
    before[SetA, SetC] and before[SetB, SetC]
  )
}
check CIsLastInCompatible1110 for exactly 1 History, exactly 3 Slot, exactly 3 Event
