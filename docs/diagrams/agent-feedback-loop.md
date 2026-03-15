# Feedback Loop Agent — Flow Diagram

> **Owner:** TBD (Agent Developer) | **Model:** `claude-sonnet` | **Type:** Auxiliary (post-pipeline)

```mermaid
flowchart TD
    START(["🔄 Feedback Loop Agent Start"])
    
    COLLECT["Collect feedback batch<br/>from sales dashboard"]
    VALIDATE{"Batch valid?<br/><i>≥1 entry with ratings</i>"}
    
    subgraph STATS["📈 Statistical Analysis (Rule-Based)"]
        direction TB
        AVG_RATING["Compute avg sales rating"]
        OUTCOME_DIST["Outcome distribution<br/><i>replied, ignored, won, lost...</i>"]
        CORRELATION["Score vs outcome correlation<br/><i>per dimension</i>"]
    end
    
    LOAD_PROMPT["Load prompt template<br/><code>prompts/feedback_loop_agent.md</code>"]
    BUILD["Build LLM request<br/>system: prompt<br/>user: batch + stats + current weights"]
    CALL["Call OpenRouter API<br/><i>claude-sonnet • temp 0.2</i>"]
    
    subgraph OUTPUTS["Calibration Outputs"]
        direction TB
        WEIGHTS["⚖️ Weight Adjustments<br/><i>per dimension (±0.2 max)</i>"]
        THRESHOLD["🔽 Filter Threshold<br/><i>more/less inclusive</i>"]
        PATTERNS["🔍 Patterns Detected<br/><i>what's working, what's not</i>"]
        PROMPTS["📝 Prompt Improvements<br/><i>suggestions for agent prompts</i>"]
        DATA_FLAGS["🚩 Data Quality Flags<br/><i>systematic gaps found</i>"]
    end
    
    STORE["Store calibration signals<br/>in Supabase"]
    
    APPLY(["✅ Apply to next pipeline run<br/>• Updated weights<br/>• Adjusted thresholds"])
    NOTIFY(["📊 Update dashboard<br/>with performance metrics"])
    ERROR_OUT(["⚠️ Error"])

    START --> COLLECT
    COLLECT --> VALIDATE
    VALIDATE -->|"❌ empty batch"| ERROR_OUT
    VALIDATE -->|"✅"| STATS
    STATS --> LOAD_PROMPT
    LOAD_PROMPT --> BUILD
    BUILD --> CALL
    CALL --> OUTPUTS
    OUTPUTS --> STORE
    STORE --> APPLY
    STORE --> NOTIFY

    classDef start fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef process fill:#f5f5f5,stroke:#616161,color:#212121
    classDef decision fill:#fff8e1,stroke:#f9a825,color:#f57f17
    classDef stat fill:#e8eaf6,stroke:#283593,color:#1a237e
    classDef output fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef apply fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef error fill:#fce4ec,stroke:#ad1457,color:#880e4f

    class START start
    class COLLECT,LOAD_PROMPT,BUILD,CALL,STORE process
    class VALIDATE decision
    class AVG_RATING,OUTCOME_DIST,CORRELATION stat
    class WEIGHTS,THRESHOLD,PATTERNS,PROMPTS,DATA_FLAGS output
    class APPLY,NOTIFY apply
    class ERROR_OUT error
```

## Calibration Constraints
| Parameter | Range | Frequency |
|-----------|-------|-----------|
| Weight adjustments | ±0.2 per dimension per cycle | Weekly batch |
| Filter threshold | ±0.1 per cycle | Weekly batch |
| Minimum sample size | 10 feedback entries | Required |
| Confidence threshold | 0.7 for pattern detection | Per pattern |
