# Architecture Diagrams

This directory contains all architecture and flow diagrams for the BD Automation system. Diagrams are written in **Mermaid** syntax, which GitHub renders natively.

## Diagram Index

| Diagram | Description | Scope |
|---------|-------------|-------|
| [pipeline-overview.md](pipeline-overview.md) | Full system architecture — all 4 layers and data flows | System-wide |
| [data-model.md](data-model.md) | Entity-Relationship diagram for Supabase tables | Data Store |
| [agent-filter.md](agent-filter.md) | Filter Agent internal flow (Stage 1) | Agent |
| [agent-score.md](agent-score.md) | Score Agent internal flow (Stage 2) | Agent |
| [agent-critic.md](agent-critic.md) | Critic Agent internal flow (Stage 3) | Agent |
| [agent-writer.md](agent-writer.md) | Writer Agent internal flow (Stage 4) | Agent |
| [agent-gap-finder.md](agent-gap-finder.md) | Gap Finder Agent flow (Auxiliary) | Agent |
| [agent-feedback-loop.md](agent-feedback-loop.md) | Feedback Loop Agent flow (Auxiliary) | Agent |

## How to Edit Diagrams

### Option 1: Edit directly on GitHub (simplest)
1. Navigate to the diagram file on GitHub
2. Click the pencil (✏️) icon to edit
3. Modify the Mermaid code inside the ` ```mermaid ` block
4. Preview renders automatically in GitHub
5. Commit to a new branch and open a PR

### Option 2: Mermaid Live Editor (visual)
1. Go to [mermaid.live](https://mermaid.live)
2. Copy the Mermaid code block from the diagram file
3. Edit visually with real-time preview
4. Copy the updated code back
5. Submit a PR with changes

### Option 3: VS Code extension (local)
1. Install [Mermaid Preview](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) extension
2. Open the `.md` file
3. Use `Ctrl+Shift+V` to preview with rendered diagrams
4. Edit and push via feature branch

## Architecture Change Process

```
1. Edit diagram in a feature branch
2. Open PR against develop
3. Architecture Owner (Federico Ledesma) reviews
4. If approved → merge to develop
5. Update corresponding agent code if needed
6. Merge develop → main when stable
```

> **Rule:** Changes to `pipeline-overview.md` or `data-model.md` require Architecture Owner review. Individual agent diagrams can be updated by the agent's owner with any team member as reviewer.

## Naming Convention
- `pipeline-*.md` — System-level diagrams
- `data-*.md` — Data model diagrams
- `agent-*.md` — Individual agent flow diagrams
- `infra-*.md` — Infrastructure/deployment diagrams (future)
