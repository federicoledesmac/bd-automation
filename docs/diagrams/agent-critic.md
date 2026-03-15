# Critic Agent — Flow Diagram

> **Owner:** TBD (Agent Developer) | **Model:** `claude-sonnet` | **Stage:** 3 of 4 | ⚠️ **MANDATORY — cannot be skipped**

```mermaid
flowchart TD
    START(["🔎 Critic Agent Start"])
    
    RECEIVE["Receive score result<br/>+ original offer/profile data"]
    CHECK_RETRY{"retry_count<br/>< MAX_RETRIES (2)?"}
    
    LOAD_PROMPT["Load prompt template<br/><code>prompts/critic_agent.md</code>"]
    
    BUILD["Build LLM request<br/>system: prompt + validation checklist<br/>user: score result + original data"]
    CALL["Call OpenRouter API<br/><i>claude-sonnet • temp 0.1 • max 4096</i>"]
    PARSE{"Response valid JSON?"}

    subgraph CHECKS["Validation Checks"]
        direction TB
        HALLUCINATION["🔍 Hallucination Detection<br/><i>Claims supported by data?</i>"]
        CONSISTENCY["📏 Score Consistency<br/><i>Scores match reasoning?</i>"]
        EVIDENCE["📎 Evidence Quality<br/><i>Strengths/risks grounded?</i>"]
        COMPLETENESS["✅ Completeness<br/><i>All dimensions addressed?</i>"]
    end

    VERDICT{"Verdict?"}
    
    APPROVED["verdict: approved<br/>quality_score: high"]
    ADJUSTED["verdict: adjusted<br/>Apply corrections<br/>quality_score: medium"]
    REJECTED["verdict: rejected<br/>Generate feedback"]

    CHECKPOINT_OK["📋 Log checkpoint<br/>verdict: approved/adjusted"]
    CHECKPOINT_RETRY["📋 Log checkpoint<br/>verdict: rejected (retry N)"]
    
    OUT_WRITER(["✅ Send to Writer Agent"])
    OUT_RETRY(["🔄 Return to Score Agent<br/>with feedback"])
    OUT_FORCE(["⚠️ Force approve<br/>(low quality flag)"])
    ERROR_OUT(["⚠️ Error"])

    START --> RECEIVE
    RECEIVE --> CHECK_RETRY
    CHECK_RETRY -->|"retries exhausted"| OUT_FORCE
    CHECK_RETRY -->|"✅ can retry"| LOAD_PROMPT
    LOAD_PROMPT --> BUILD
    BUILD --> CALL
    CALL --> PARSE
    PARSE -->|"❌"| ERROR_OUT
    PARSE -->|"✅"| CHECKS
    CHECKS --> VERDICT
    VERDICT -->|"approved"| APPROVED
    VERDICT -->|"adjusted"| ADJUSTED
    VERDICT -->|"rejected"| REJECTED
    APPROVED --> CHECKPOINT_OK
    ADJUSTED --> CHECKPOINT_OK
    REJECTED --> CHECKPOINT_RETRY
    CHECKPOINT_OK --> OUT_WRITER
    CHECKPOINT_RETRY --> OUT_RETRY

    classDef start fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef process fill:#f5f5f5,stroke:#616161,color:#212121
    classDef decision fill:#fff8e1,stroke:#f9a825,color:#f57f17
    classDef success fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef warning fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef retry fill:#e8eaf6,stroke:#283593,color:#1a237e
    classDef error fill:#fce4ec,stroke:#ad1457,color:#880e4f
    classDef check fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c

    class START start
    class RECEIVE,LOAD_PROMPT,BUILD,CALL,CHECKPOINT_OK,CHECKPOINT_RETRY process
    class CHECK_RETRY,PARSE,VERDICT decision
    class APPROVED,ADJUSTED success
    class REJECTED retry
    class OUT_WRITER success
    class OUT_RETRY retry
    class OUT_FORCE warning
    class ERROR_OUT error
    class HALLUCINATION,CONSISTENCY,EVIDENCE,COMPLETENESS check
```

## Validation Checklist
| Check | Severity if Failed | Action |
|-------|--------------------|--------|
| Hallucination detected | 🔴 High | Reject + retry |
| Score-reasoning mismatch | 🟡 Medium | Adjust or reject |
| Unsupported claims | 🟡 Medium | Adjust scores |
| Missing dimension analysis | 🟢 Low | Adjust (note gap) |

## Retry Logic
- **Max retries:** 2
- **On reject:** Score Agent re-runs with critic's specific feedback
- **On exhaustion:** Force-approve with `quality_score < 0.5` flag
