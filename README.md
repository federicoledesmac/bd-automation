# BD Automation System

**Matching Engine & Offer-Profile Automation for Protofire**

[![ClickUp Board](https://img.shields.io/badge/ClickUp-Board-7B68EE?style=flat&logo=clickup)](https://app.clickup.com/t/86ag6dmvg)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

---

## Overview

BD Automation is an AI-powered system that matches Protofire's service offerings with potential client profiles. The system ingests data from multiple sources, processes it through a 4-agent pipeline, and delivers prioritized leads to the sales team.

### Architecture Layers

| Layer | Stack | Purpose |
|-------|-------|---------|
| **Data Store** | Supabase (PostgreSQL + pgvector) | Offers, empathy maps, signals, match results |
| **Ingestion** | n8n + Python scrapers | Collect and normalize external/internal data |
| **Agent Orchestrator** | OpenRouter + LangChain | 4-agent pipeline: Filter → Score → Critic → Writer |
| **Delivery + Feedback** | React Dashboard | Sales team interface, feedback loop |

---

## Repository Structure

```
bd-automation/
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md    # PR template with ClickUp integration
├── agents/                          # Agent Orchestrator layer
│   ├── filter_agent.py
│   ├── score_agent.py
│   ├── critic_agent.py
│   └── writer_agent.py
├── ingestion/
│   ├── scrapers/                    # External data scrapers
│   ├── internal/                    # Internal data connectors
│   └── n8n-workflows/              # n8n workflow JSON exports
├── supabase/
│   ├── migrations/                  # Database migration files
│   └── functions/                   # Supabase Edge Functions
├── data/
│   ├── offers/                      # Protofire offer definitions
│   ├── empathy-maps/                # Client persona empathy maps
│   └── signals/                     # Market signal definitions
├── prompts/                         # LLM prompt templates (versioned)
├── dashboard/                       # Sales team React dashboard
├── docs/                            # Architecture docs, ADRs, runbooks
├── scripts/                         # Utility and deployment scripts
├── .gitignore
└── README.md
```

---

## ClickUp ↔ GitHub Integration

This repository is integrated with the **OKR - Matching Engine & BD Automation** board in ClickUp.

### Linking Commits and PRs to Tasks

Every commit and PR **must** reference a ClickUp task ID using the `CU-` prefix:

```
# In commit messages
feat(agents): implement filter agent scoring logic [CU-86ag6dmvg]

# In branch names
feature/CU-86ag6dzt7-repo-setup

# In PR titles
feat: repo structure and CI setup [CU-86ag6dzt7]
```

### ClickUp Task IDs Reference

| Task ID | Task Name | Owner |
|---------|-----------|-------|
| `86ag6dmvg` | Tooling Selection & System Architecture | Federico Ledesma |
| `86ag6dzt7` | Create GitHub repo and configure ClickUp integration | Federico Ledesma |

> **Note:** Full task list available on the [ClickUp Board](https://app.clickup.com/t/86ag6dmvg). Keep this table updated as tasks are created.

---

## Branching Strategy

```
main (protected — production-ready)
 └── develop (protected — integration branch)
      ├── feature/CU-{id}-short-description
      ├── fix/CU-{id}-short-description
      └── chore/CU-{id}-short-description
```

### Rules

1. **`main`** — Production-ready code only. Merges from `develop` via PR with at least 1 review.
2. **`develop`** — Integration branch. All feature branches merge here first.
3. **Feature branches** — Created from `develop`, named `feature/CU-{task_id}-short-description`.
4. **No direct pushes** to `main` or `develop`. Always use PRs.

### Branch Lifecycle

```
git checkout develop
git pull origin develop
git checkout -b feature/CU-86ag6xxxx-my-feature
# ... work ...
git push origin feature/CU-86ag6xxxx-my-feature
# Open PR → develop, get review, merge
```

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/) with ClickUp task references:

```
type(scope): description [CU-task_id]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies, CI/CD |
| `data` | Data file updates (offers, empathy maps, signals) |
| `prompt` | Prompt template changes |

### Scopes

| Scope | Directory |
|-------|-----------|
| `agents` | `agents/` |
| `ingestion` | `ingestion/` |
| `supabase` | `supabase/` |
| `dashboard` | `dashboard/` |
| `data` | `data/` |
| `prompts` | `prompts/` |
| `docs` | `docs/` |
| `scripts` | `scripts/` |
| `ci` | `.github/` |

### Examples

```bash
feat(agents): add critic agent with rubric-based evaluation [CU-86ag6xxxx]
fix(ingestion): handle rate limiting in Twitter scraper [CU-86ag6xxxx]
docs(docs): update architecture diagram for v1.1 [CU-86ag6dmvg]
data(data): add empathy map for DeFi protocols [CU-86ag6xxxx]
chore(ci): add pre-commit hooks for linting [CU-86ag6xxxx]
```

---

## Ownership Matrix

| Directory | Owner | Role |
|-----------|-------|------|
| `agents/` | TBD | Agent Developer |
| `ingestion/scrapers/` | TBD | Scraper Developer |
| `ingestion/internal/` | TBD | Internal Data Engineer |
| `ingestion/n8n-workflows/` | TBD | n8n Workflow Designer |
| `supabase/` | TBD | Database Engineer |
| `data/offers/` | BD Team | Offer Definitions |
| `data/empathy-maps/` | BD Team | Client Personas |
| `data/signals/` | TBD | Signal Analyst |
| `prompts/` | TBD | Prompt Engineer |
| `dashboard/` | TBD | Frontend Developer |
| `docs/` | Federico Ledesma | Architecture & Docs |
| `scripts/` | Federico Ledesma | DevOps & Tooling |
| `.github/` | Federico Ledesma | CI/CD & Repo Config |

---

## Getting Started

### Prerequisites

- Python 3.11+
- [Supabase CLI](https://supabase.com/docs/guides/cli)
- [n8n](https://n8n.io/) (for workflow development)
- Node.js 18+ (for dashboard)
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/federicoledesmac/bd-automation.git
cd bd-automation

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env
# Edit .env with your API keys (OpenRouter, Supabase, etc.)

# 5. Start Supabase locally
supabase start

# 6. Run database migrations
supabase db push
```

### Environment Variables

```env
# OpenRouter (Agent Orchestrator)
OPENROUTER_API_KEY=your_key_here

# Supabase
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_key

# n8n
N8N_WEBHOOK_URL=http://localhost:5678

# Dashboard
VITE_API_URL=http://localhost:3000
```

---

## Contributing

1. Pick a task from the [ClickUp Board](https://app.clickup.com/t/86ag6dmvg)
2. Create a feature branch from `develop`: `feature/CU-{task_id}-description`
3. Follow the commit convention
4. Open a PR against `develop` using the PR template
5. Get at least 1 review approval
6. Merge and update the ClickUp task status

---

## Links

- **ClickUp Board:** [OKR - Matching Engine & BD Automation](https://app.clickup.com/t/86ag6dmvg)
- **Architecture Doc:** See `docs/` or ClickUp task comments
- **Team Contact:** Federico Ledesma (federico.ledesma@protofire.io)

---

*Maintained by the BD Automation Team @ Protofire*
