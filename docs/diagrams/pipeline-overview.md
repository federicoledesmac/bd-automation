# BD Automation — Pipeline Overview

> **Edit this diagram:** Open in [Mermaid Live Editor](https://mermaid.live) — paste the code below, edit visually, then copy back and submit a PR.

```mermaid
flowchart TB
    subgraph INGESTION["🔄 Ingestion Layer"]
        direction LR
        EXT["📡 External Scrapers<br/>(LinkedIn, Twitter, Crunchbase)"]
        INT["🏢 Internal Data<br/>(CRM, Notion, Slack)"]
        N8N["⚡ n8n Workflows<br/>(Orchestration)"]
        EXT --> N8N
        INT --> N8N
    end

    subgraph DATASTORE["💾 Data Store (Supabase)"]
        direction LR
        OFFERS[("📋 Offers")]
        PROFILES[("👤 Profiles")]
        EMPATHY[("🗺️ Empathy Maps")]
        SIGNALS[("📶 Signals")]
        MATCHES[("🎯 Match Results")]
    end

    subgraph ORCHESTRATOR["🤖 Agent Orchestrator (OpenRouter)"]
        direction TB
        
        subgraph PREPIPELINE["Pre-Pipeline"]
            GAP["🔍 Gap Finder Agent<br/><i>mistral-small • temp 0.1</i>"]
        end

        subgraph PIPELINE["Sequential Pipeline"]
            direction TB
            FILTER["🔽 Filter Agent<br/><i>mistral-small • temp 0.1</i><br/>Fast pre-filter"]
            SCORE["📊 Score Agent<br/><i>claude-sonnet • temp 0.2</i><br/>5-dimension scoring"]
            CRITIC["🔎 Critic Agent<br/><i>claude-sonnet • temp 0.1</i><br/>Quality validation"]
            WRITER["✍️ Writer Agent<br/><i>gpt-4o • temp 0.7</i><br/>Outreach generation"]
            
            FILTER -->|"pass=true"| SCORE
            FILTER -->|"pass=false"| DISCARD["❌ Discarded"]
            SCORE --> CRITIC
            CRITIC -->|"approved"| WRITER
            CRITIC -->|"rejected<br/>(max 2 retries)"| SCORE
        end

        subgraph POSTPIPELINE["Post-Pipeline"]
            FEEDBACK["🔄 Feedback Loop Agent<br/><i>claude-sonnet • temp 0.2</i>"]
        end
    end

    subgraph DELIVERY["📨 Delivery + Feedback"]
        direction LR
        DASHBOARD["📊 Sales Dashboard<br/>(React)"]
        OUTREACH["📧 Outreach Queue"]
        FB_INPUT["💬 Sales Feedback"]
    end

    %% Data flows
    N8N -->|"normalized data"| DATASTORE
    DATASTORE -->|"offer + profile pairs"| GAP
    GAP -->|"completeness report"| DATASTORE
    DATASTORE -->|"filtered pairs"| FILTER
    DATASTORE -->|"empathy maps + signals"| SCORE
    WRITER -->|"match + outreach"| MATCHES
    MATCHES --> DASHBOARD
    MATCHES --> OUTREACH
    FB_INPUT -->|"ratings + outcomes"| FEEDBACK
    FEEDBACK -->|"calibration signals"| DATASTORE

    %% Styling
    classDef ingestion fill:#e1f5fe,stroke:#0288d1,color:#01579b
    classDef datastore fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c
    classDef agent fill:#e8f5e9,stroke:#388e3c,color:#1b5e20
    classDef delivery fill:#fff3e0,stroke:#f57c00,color:#e65100
    classDef discard fill:#ffebee,stroke:#c62828,color:#b71c1c

    class EXT,INT,N8N ingestion
    class OFFERS,PROFILES,EMPATHY,SIGNALS,MATCHES datastore
    class GAP,FILTER,SCORE,CRITIC,WRITER,FEEDBACK agent
    class DASHBOARD,OUTREACH,FB_INPUT delivery
    class DISCARD discard
```

## How to Edit

1. Copy the Mermaid code block above
2. Open [Mermaid Live Editor](https://mermaid.live)
3. Paste and edit visually
4. Copy the updated code back
5. Submit a PR with your changes to `docs/diagrams/pipeline-overview.md`

Changes to this diagram should be discussed with the Architecture Owner (Federico Ledesma) before merging.
