# Gap Finder Agent — Flow Diagram

> **Owner:** TBD (Agent Developer) | **Model:** `mistral-small` | **Type:** Auxiliary (pre/post pipeline)

```mermaid
flowchart TD
    START(["🔍 Gap Finder Agent Start"])
    
    RECEIVE["Receive entity for analysis"]
    VALIDATE{"entity_type valid?<br/><i>offer | profile | empathy_map</i>"}
    
    LOAD_SCHEMA["Load expected fields<br/>for entity type"]
    
    subgraph RULE_CHECK["Rule-Based Checks"]
        direction TB
        PRESENT["✅ Fields present<br/>& populated"]
        MISSING["❌ Fields missing<br/>entirely"]
        EMPTY["⚠️ Fields present<br/>but empty/vague"]
    end
    
    COMPLETENESS["Calculate completeness score<br/><i>present / expected fields</i>"]
    
    LOAD_PROMPT["Load prompt template<br/><code>prompts/gap_finder_agent.md</code>"]
    BUILD["Build LLM request<br/>for quality analysis"]
    CALL["Call OpenRouter API<br/><i>mistral-small • temp 0.1</i>"]
    
    COMBINE["Combine rule-based + LLM results"]
    
    PRIORITY{"Completeness<br/>score?"}
    
    CRITICAL["🔴 priority: critical<br/><i>< 50% complete</i>"]
    HIGH["🟠 priority: high<br/><i>50-70% complete</i>"]
    MEDIUM["🟡 priority: medium<br/><i>70-90% complete</i>"]
    LOW["🟢 priority: low<br/><i>> 90% complete</i>"]
    
    REPORT["Generate gap report<br/>• missing fields + importance<br/>• quality issues + suggestions<br/>• recommended data sources"]
    
    OUT_INGEST(["📡 Feed to Ingestion Layer<br/>prioritize data collection"])
    OUT_TEAM(["👥 Notify data owners<br/>via dashboard"])

    START --> RECEIVE
    RECEIVE --> VALIDATE
    VALIDATE -->|"❌"| ERROR_OUT(["⚠️ Error"])
    VALIDATE -->|"✅"| LOAD_SCHEMA
    LOAD_SCHEMA --> RULE_CHECK
    RULE_CHECK --> COMPLETENESS
    COMPLETENESS --> LOAD_PROMPT
    LOAD_PROMPT --> BUILD
    BUILD --> CALL
    CALL --> COMBINE
    COMBINE --> PRIORITY
    PRIORITY -->|"< 50%"| CRITICAL
    PRIORITY -->|"50-70%"| HIGH
    PRIORITY -->|"70-90%"| MEDIUM
    PRIORITY -->|"> 90%"| LOW
    CRITICAL --> REPORT
    HIGH --> REPORT
    MEDIUM --> REPORT
    LOW --> REPORT
    REPORT --> OUT_INGEST
    REPORT --> OUT_TEAM

    classDef start fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef process fill:#f5f5f5,stroke:#616161,color:#212121
    classDef decision fill:#fff8e1,stroke:#f9a825,color:#f57f17
    classDef critical fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef high fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef medium fill:#fffde7,stroke:#f9a825,color:#f57f17
    classDef low fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef output fill:#e0f2f1,stroke:#00695c,color:#004d40

    class START start
    class RECEIVE,LOAD_SCHEMA,COMPLETENESS,LOAD_PROMPT,BUILD,CALL,COMBINE,REPORT process
    class VALIDATE,PRIORITY decision
    class CRITICAL critical
    class HIGH high
    class MEDIUM medium
    class LOW low
    class OUT_INGEST,OUT_TEAM output
```

## Expected Fields per Entity
| Entity | Critical Fields | Total Expected |
|--------|----------------|----------------|
| Offer | title, services, verticals, tech_stack | 8 |
| Profile | company, industry, tech_used, pain_points | 9 |
| Empathy Map | thinks, feels, pain_points, goals | 9 |
