# Experiment Design Card - recorded before the first benchmark

| Field | Edit distance | String search |
|---|---|---|
| Question | Does removing repeated subproblems control work, and do two rows save storage? | How much repeated work does KMP avoid on late mismatches? |
| Sizes | All three: n=2,4,6,8; table and rows additionally n=64,128,256,512,1024. Recursion is deliberately capped. | n=1024,2048,4096,8192; m=n/16. Both grow to reveal the naive worst case. |
| Inputs | equal: best recursion path; disjoint: every comparison mismatches and branches; random: four-letter alphabet. Both words have length n. | early_mismatch: immediate rejection; late_mismatch: A^n against A^(m-1)B, worst case for naive; random: four-letter alphabet. |
| Metrics | recursive calls, evaluated interior DP cells, character comparisons, allocated integer slots, median time of 5 runs. Slots exclude JVM object headers and recursive stack. | text-pattern comparisons plus LPS comparisons; report their sum for fair total work; median time of 5 runs includes preprocessing. |
| Prediction | Disjoint recursion grows exponentially; equal recursion grows linearly; both DP variants evaluate n^2 cells, storage differs by a factor (n+1)/2. | Early mismatches grow linearly. Late mismatches grow quadratically for naive with m=n/16; KMP remains linear including LPS. |
| Plots | Log-y common-size operation counts; DP slot counts over larger sizes; DP median times. | Total comparisons in three panels; median times in three panels with log-y axes. |

Protocol: seed 20261108, one independent deterministic case per size/type, 5 untimed warmups and 5 measured runs per case/algorithm. Instrumentation stays enabled. Time is not deterministic; inputs, answers and counters must repeat exactly. No prediction was changed after collecting results.
