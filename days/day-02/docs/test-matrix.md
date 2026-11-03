# LabShop six-case review

Rules: 100100/5 and 100101/10. No custom match does not mean that no generic Wazuh rule can match.

| Case | Recorded input | Intended result | Captured / reported result | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| 1 · Single failure | fail admin .133 1, repeated three times | 100100/5 | Three dashboard rows W2-017/018 | Recorded positive |
| 2 · Same-source bulk | fail admin .133 6, repeated three times | 100101/10 | Three correlation alerts W2-019/020; exact threshold not measured | Recorded positive |
| 3 · Monitor | fail monitor 10.10.10.1 1, repeated three times; logtest | No LabShop match | Generic **1002/2** in W2-022 | Custom exclusion; not zero alerts |
| 4 · Split sources | .50 3; .60 3 | No cross-source aggregation | W2-024 includes **100101/10**; source fields/prior state missing | Unresolved |
| 5 · LOGIN_OK | ok alice .50 2, repeated twice | No failure detector | W2-026 proves source logs; handoff reports suppression | Full negative proof missing |
| 6 · Malformed | INVALID_DATA test=hello | No structured failure match | W2-028 shows Phase 1 only; handoff reports no custom alert | Final captured verdict missing |

[Commands and original screenshots](../README.md#step-03) · [Evidence register](../evidence/README.md)

## Controlled retest to perform on the VMs

1. Retain effective unique rule IDs, decoder definitions and the generator's actual implementation/timing.
2. Separate source/time windows and allow previous correlation state to expire. Record the reset/isolation method; a new shell does not reset manager state.
3. Retain input lines/counts/timestamps and complete final alerts/logtest verdicts, including srcip.
4. Determine whether the split-source alert belongs to prior same-source activity, another event group or a real rule issue. The current crop cannot decide this.
5. Record the actual pass or failure without relabeling the old capture.

These are pending steps, not results of the static repository checks.
