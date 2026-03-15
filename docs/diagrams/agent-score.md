# Score Agent — Flow Diagram

> **Owner:** TBD (Agent Developer) | **Model:** `claude-sonnet` | **Stage:** 2 of 4

```mermaid
flowchart TD
    START(["📊 Score Agent Start"])
    
    RECEIVE["Receive filtered pair<br/>+ empathy map + signals"]
    VALIDATE_IN{"Input valid?<br/><i>filter_result.pass == true</i>"}
    LOAD_PROMPT["Load prompt template<br/><code>prompts/score_agent.md</code>"]
    
    ENRICH["Enrich context<br/>• Fetch empathy map (if exists)<br/>• Fetch recent signals<br/>• Load scoring weights"]
    
    BUILD["Build LLM request<br/>system: prompt + weights<br/>user: full context JSON"]
    CALL["Call OpenRouter API<br/><i>claude-sonnet • temp 0.2 • max 4096</i>"]
    PARSE{"Response valid JSON?"}
    
    VALIDATE_SCORES{"All 5 dimensions<br/>scored (0-100)?"}
    
    COMPUTE["Compute composite score<br/><i>weighted average of 5 dimensions</i>"]
    
    CHECKPOINT["📋 Log checkpoint<br/>scores + reasoning"]
    
    OUT(["➡️ Send to Critic Agent"])
    ERROR_OUT(["⚠️ Error — retry"])

    START --> RECEIVE
    RECEIVE --> VALIDATE_IN
    VALIDATE_IN -->|"❌ not filtered"| ERROR_OUT
    VALIDATE_IN -->|"✅"| LOAD_PROMPT
    LOAD_PROMPT --> ENRICH
    ENRICH --> BUILD
    BUILD --> CALL
    CALL --> PARSE
    PARSE -->|"❌ parse error"| ERROR_OUT
    PARSE -->|"✅"| VALIDATE_SCORES
    VALIDATE_SCORES -->|"❌ missing dims"| ERROR_OUT
    VALIDATE_SCORES -->|"✅"| COMPUTE
    COMPUTE --> CHECKPOINT
    CHECKPOINT --> OUT

    classDef start fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef process fill:#f5f5f5,stroke:#616161,color:#212121
    classDef decision fill:#fff8e1,stroke:#f9a825,color:#f57f17
    classDef success fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef error fill:#fce4ec,stroke:#ad1457,color:#880e4f

    class START start
    class RECEIVE,LOAD_PROMPT,ENRICH,BUILD,CALL,COMPUTE,CHECKPOINT process
    class VALIDATE_IN,PARSE,VALIDATE_SCORES decision
    class OUT success
    class ERROR_OUT error
```

## Scoring Dimensions
| # | Dimension | Weight (default) | Description |
|---|-----------|-----------------|-------------|
| 1 | Industry Alignment | 0.25 | Vertical/sub-industry match |
| 2 | Technical Fit | 0.25 | Tech stack overlap |
| 3 | Budget Signals | 0.20 | Spending capacity indicators |
| 4 | Timing/Urgency | 0.15 | Need-now signals |
| 5 | Relationship Proximity | 0.15 | Network closeness |

*Weights are calibrated by the Feedback Loop Agent over time.*
