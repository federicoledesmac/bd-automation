# Profiles & Contacts — Data Model Detail

> **Owner:** Ivor Jugo (external) / Rado Patus (internal) | **Contacts Owner:** Diego Torres

```mermaid
erDiagram
    PROFILES {
        uuid id PK
        string company
        string industry
        string sub_industry
        string company_size
        string[] tech_used
        string funding_stage
        jsonb decision_makers
        string[] pain_points
        string budget_range
        jsonb raw_signals
        timestamp created_at
        timestamp updated_at
    }

    CONTACTS {
        uuid id PK
        uuid profile_id FK
        string first_name
        string last_name
        string role
        string country_of_origin
        string gender
        int age
        string linkedin_url
        string twitter_url
        timestamp created_at
        timestamp updated_at
    }

    EMPATHY_MAPS {
        uuid id PK
        uuid profile_id FK
        string role
        string country_of_origin
        string gender
        int age
        string[] thinks
        string[] feels
        string[] says
        string[] does_actions
        string[] pain_points
        string[] gains
        string[] goals
        string[] influences
        string[] preferred_channels
        float quality_score
        timestamp created_at
    }

    SIGNALS {
        uuid id PK
        uuid profile_id FK
        string signal_type
        string source
        string description
        float strength
        timestamp detected_at
    }

    MATCH_RESULTS {
        uuid id PK
        uuid offer_id FK
        uuid profile_id FK
        float composite_score
        string critic_verdict
    }

    PROFILES ||--o{ CONTACTS : "has team members"
    PROFILES ||--o| EMPATHY_MAPS : "has persona"
    PROFILES ||--o{ SIGNALS : "emits"
    PROFILES ||--o{ MATCH_RESULTS : "matched in"
```

## Contacts

People within each company profile. Used by the Writer Agent to personalize outreach to specific decision makers.

| Field | Type | Description |
|-------|------|-------------|
| `id` | uuid (PK) | Contact identifier |
| `profile_id` | uuid (FK) | Parent company profile |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `role` | string | Job title / role in the company |
| `country_of_origin` | string | Country of origin |
| `gender` | string | Gender |
| `age` | int | Age |
| `linkedin_url` | string | LinkedIn profile URL |
| `twitter_url` | string | Twitter/X profile URL |

## Empathy Maps — Demographic Fields

The empathy map now includes demographic context to improve personalization:

| Field | Type | Purpose |
|-------|------|---------|
| `role` | string | Persona's role — affects tone and talking points |
| `country_of_origin` | string | Cultural context for communication style |
| `gender` | string | Inclusive language adaptation |
| `age` | int | Generational communication preferences |

These fields feed into the **Writer Agent** for channel selection and tone matching, and into the **Score Agent** for relationship proximity assessment.
