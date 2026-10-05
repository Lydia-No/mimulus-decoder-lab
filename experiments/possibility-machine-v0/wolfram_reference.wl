(* Possibility Machine v0 — independent Wolfram reference
   Synthetic known-answer only; non-canonical. *)

ClearAll[succ, nodes, stateKey];

stateKey[s_List] := StringJoin[ToString /@ s];

succ[{s_List, h_List}, historyGate_: True] := Module[
  {a, b, c, d, out = {}, gateOK},
  {a, b, c, d} = s;

  If[a == 0,
    AppendTo[out, {{1, b, c, d}, Append[h, "set_a"]}]
  ];

  If[b == 0,
    AppendTo[out, {{a, 1, c, d}, Append[h, "set_b"]}]
  ];

  If[c == 0 && a == 1 && b == 1,
    AppendTo[out, {{a, b, 1, d}, Append[h, "set_c"]}]
  ];

  gateOK = ! historyGate || (
    MemberQ[h, "set_a"] &&
    MemberQ[h, "set_b"] &&
    FirstPosition[h, "set_a"][[1]] < FirstPosition[h, "set_b"][[1]]
  );

  If[d == 0 && c == 1 && gateOK,
    AppendTo[out, {{a, b, c, 1}, Append[h, "set_d"]}]
  ];

  out
];

nodes = FixedPoint[
  Union[#, Flatten[succ /@ #, 1]] &,
  {{{0, 0, 0, 0}, {}}}
];

With[
  {
    states = Sort[stateKey /@ DeleteDuplicates[nodes[[All, 1]]]],
    histories1110 = Sort[
      Last /@ Select[nodes, First[#] == {1, 1, 1, 0} &]
    ],
    ab = {{1, 1, 1, 0}, {"set_a", "set_b", "set_c"}},
    ba = {{1, 1, 1, 0}, {"set_b", "set_a", "set_c"}}
  },
  <|
    "ReachableCurrentStates" -> states,
    "ReachableCurrentStateCount" -> Length[states],
    "ReachableStateHistoryNodes" -> Length[nodes],
    "HistoriesAt1110" -> histories1110,
    "ABCanReach1111" -> MemberQ[
      First /@ succ[ab], {1, 1, 1, 1}
    ],
    "BACanReach1111" -> MemberQ[
      First /@ succ[ba], {1, 1, 1, 1}
    ],
    "BAAfterGateRemoval" -> MemberQ[
      First /@ succ[ba, False], {1, 1, 1, 1}
    ],
    "InvariantCImpliesAB" -> And @@ (
      (#[[1, 3]] == 0 || (#[[1, 1]] == 1 && #[[1, 2]] == 1)) & /@ nodes
    ),
    "InvariantDImpliesC" -> And @@ (
      (#[[1, 4]] == 0 || #[[1, 3]] == 1) & /@ nodes
    )
  |>
]
