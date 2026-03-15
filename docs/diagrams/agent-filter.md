# Filter Agent — Flow Diagram

> **Owner:** TBD (Agent Developer) | **Model:** `mistral-small` | **Stage:** 1 of 4

```mermaid
flowchart TD
    START(["🔽 Filter Agent Start"])
    
    LOAD["Load offer + profile pair<br/>from Supabase queue"]
    VALIDATE_IN{"Input valid?<br/><i>offer + profile present</i>"}
    LOAD_PROMPT["Load prompt template<br/><code>prompts/filter_agent.md</code>"]
    
    BUILD["Build LLM request<br/>system: prompt template<br/>user: offer + profile JSON"]
    CALL["Call OpenRouter API<br/><i>mistral-small • temp 0.1 • max 1024</i>"]
    PARSE{"Response valid JSON?"}
    
    EVALUATE{"pass == true?"}
    
    CHECKPOINT_PASS["📋 Log checkpoint<br/>status: pass<br/>confidence: N"]
    CHECKPOINT_FAIL["📋 Log checkpoint<br/>status: filtered_out<br/>confidence: N"]
    
    PASS_OUT(["✅ Send to Score Agent"])
    FAIL_OUT(["❌ Discard — log rationale"])
    ERROR_OUT(["⚠️ Error — retry or skip"])

    START --> LOAD
    LOAD --> VALIDATE_IN
    VALIDATE_IN -->|"❌ missing fields"| ERROR_OUT
    VALIDATE_IN -->|"✅"| LOAD_PROMPT
    LOAD_PROMPT --> BUILD
    BUILD --> CALL
    CALL --> PARSE
    PARSE -->|"❌ parse error"| ERROR_OUT
    PARSE -->|"✅"| EVALUATE
    EVALUATE -->|"pass=true"| CHECKPOINT_PASS
    EVALUATE -->|"pass=false"| CHECKPOINT_FAIL
    CHECKPOINT_PASS --> PASS_OUT
    CHECKPOINT_FAIL --> FAIL_OUT

    classDef start fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef process fill:#f5f5f5,stroke:#616161,color:#212121
    classDef decision fill:#fff8e1,stroke:#f9a825,color:#f57f17
    classDef success fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef fail fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef error fill:#fce4ec,stroke:#ad1457,color:#880e4f

    class START start
    class LOAD,LOAD_PROMPT,BUILD,CALL,CHECKPOINT_PASS,CHECKPOINT_FAIL process
    class VALIDATE_IN,PARSE,EVALUATE decision
    class PASS_OUT success
    class FAIL_OUT fail
    class ERROR_OUT error
```

## Input Schema
| Field | Type | Required |
|-------|------|----------|
| `offer` | `{ id, title, services, verticals, tech_stack }` | ✅ |
| `profile` | `{ id, company, industry, signals, tech_used }` | ✅ |

## Output Schema
| Field | Type | Description |
|-------|------|-------------|
| `pass` | `bool` | Whether the pair should proceed |
| `rationale` | `str` | One-sentence explanation |
| `confidence` | `float (0-1)` | Certainty of the decision |

## Design Decisions
- **Inclusive by default:** When in doubt, pass. False negatives are worse than false positives at this stage.
- **Cheap model:** Uses mistral-small for cost efficiency — this runs on every pair.
- **Low temperature (0.1):** Consistency over creativity for binary decisions.
