# warrant-mcp

An MCP (Model Context Protocol) server that provides formal reasoning and argument validation tools for AI agents. Built on established computational argumentation theories — Dung, Toulmin, Walton, Pollock, Prakken, and ASPIC+.

## Features

- **Dung's Abstract Argumentation Framework**: Extensions (grounded, preferred, stable).
- **Toulmin Model**: Structured argument validation.
- **Walton's Schemes**: Critical questions for common reasoning patterns.
- **Pollock's Defeasible Reasoning**: Rebutting and undercutting defeaters.
- **Prakken's Dialogue Protocol**: Persuasion dialogue management.
- **ASPIC+**: Disagreement diagnosis.
- **Gradual Semantics**: Argument scoring (h-Categorizer, Counting).
- **Bipolar Argumentation Framework**: Support + Attack relations.

## Installation

This project uses `uv` for dependency management.

```bash
# Clone the repository
git clone https://github.com/jayden-chmod/warrant-mcp.git
cd warrant-mcp

# Install dependencies
uv sync
```

## Usage

### Running the MCP Server

`warrant-mcp` can be run using `uv run`.

```bash
uv run warrant-mcp
```

### Configure for Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "warrant-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/warrant-mcp",
        "warrant-mcp"
      ]
    }
  }
}
```

---

## 🔧 MCP Tools Reference

warrant-mcp exposes **10 MCP tools** that AI agents can call directly. Below is the full reference for each tool.

### 1. `build_argument` — Build Structured Argument (Toulmin)

Build a structured argument using Toulmin's model (Claim → Data → Warrant → Backing → Rebuttal → Qualifier).

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim` | `string` | ✅ | The assertion to be supported |
| `data` | `List[{content, type}]` | ✅ | Evidence supporting the claim. Each item must have `content` (string) and `type` (`certain`, `objective`, `uncertain`, `subjective`, `hypothetical`) |
| `warrant` | `string` | ❌ | Why the data supports the claim |
| `backing` | `List[string]` | ❌ | Evidence supporting the warrant |
| `rebuttal` | `List[string]` | ❌ | Conditions under which the claim might not hold |
| `qualifier` | `string` | ❌ | Strength modifier. Default: `"presumably"`. Options: `certainly`, `very likely`, `presumably`, `possibly`, `uncertain` |

**Example:**

```json
{
  "claim": "We should use PostgreSQL instead of MongoDB for this project",
  "data": [
    {"content": "Our data has strong relational structure with foreign keys", "type": "certain"},
    {"content": "Team has 5 years of PostgreSQL experience", "type": "objective"}
  ],
  "warrant": "Relational databases excel with structured, relational data",
  "backing": ["PostgreSQL consistently outperforms MongoDB in JOIN-heavy workloads (TPC-H benchmarks)"],
  "rebuttal": ["If the data schema changes frequently, MongoDB's flexibility may be advantageous"],
  "qualifier": "very likely"
}
```

**Returns:** `{ argument, validation, score }`

---

### 2. `identify_scheme` — Identify Walton's Argumentation Scheme

Identify which Walton argumentation scheme matches a claim, or retrieve details for a specific scheme.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claim` | `string` | ✅ | The claim to analyze |
| `context` | `string` | ❌ | Additional context for better matching |
| `scheme` | `string` | ❌ | Retrieve a specific scheme by name (e.g., `expert_opinion`) |

**Example:**

```json
{
  "claim": "We should refactor the auth module before adding OAuth support",
  "context": "The auth module has high cyclomatic complexity and no tests"
}
```

**Returns:** `{ matches, topScheme }` — Ranked scheme matches with critical questions.

---

### 3. `classify_defeater` — Classify Counterargument (Pollock)

Classify a counterargument as a rebutting defeater (attacks the conclusion) or undercutting defeater (breaks the reasoning link).

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `target` | `string` | ✅ | The argument being attacked |
| `content` | `string` | ✅ | The counterargument content |
| `type` | `string` | ✅ | `rebutting` or `undercutting` |
| `evidence_type` | `string` | ❌ | `certain`, `objective`, `uncertain`, `subjective`, `hypothetical`. Default: `"uncertain"` |

**Example:**

```json
{
  "target": "PostgreSQL is faster for our workload",
  "content": "The benchmark was run on different hardware with different data distribution",
  "type": "undercutting",
  "evidence_type": "objective"
}
```

**Returns:** `{ defeater, strength, penalty }`

---

### 4. `create_framework` — Create Argumentation Framework

Create a Dung Argumentation Framework (AF) or a Bipolar AF with both attack and support relations.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `arguments` | `List[string]` | ✅ | List of argument identifiers |
| `attacks` | `List[[attacker, target]]` | ✅ | Attack relations as pairs `[attacker, target]` |
| `supports` | `List[[supporter, target]]` | ❌ | Support relations (creates a Bipolar AF if provided) |

**Example:**

```json
{
  "arguments": ["A1", "A2", "A3", "A4"],
  "attacks": [["A2", "A1"], ["A3", "A2"]],
  "supports": [["A4", "A1"]]
}
```

**Returns:** `{ type, arguments, attacks, supports }`

---

### 5. `compute_extensions` — Compute Acceptable Arguments (Dung)

Compute acceptable arguments using Dung's semantics (grounded, preferred, stable).

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `arguments` | `List[string]` | ✅ | List of argument identifiers |
| `attacks` | `List[[attacker, target]]` | ✅ | Attack relations |
| `semantics` | `string` | ❌ | `grounded`, `preferred`, `stable`, or `all` (default) |

**Example:**

```json
{
  "arguments": ["A", "B", "C"],
  "attacks": [["B", "A"], ["C", "B"]],
  "semantics": "all"
}
```

**Returns:** `{ grounded, preferred, stable }` — Sets of acceptable arguments under each semantics.

---

### 6. `score_arguments` — Score Arguments (Gradual Semantics)

Score arguments on a continuous [0, 1] scale using gradual semantics.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `arguments` | `List[string]` | ✅ | List of argument identifiers |
| `attacks` | `List[[attacker, target]]` | ✅ | Attack relations |
| `supports` | `List[[supporter, target]]` | ❌ | Support relations (used with `bipolar` method) |
| `method` | `string` | ❌ | `h-categorizer` (default), `counting`, or `bipolar` |

**Example:**

```json
{
  "arguments": ["A", "B", "C"],
  "attacks": [["B", "A"], ["C", "B"]],
  "method": "h-categorizer"
}
```

**Returns:** `{ method, scores }` — Arguments sorted by score descending.

---

### 7. `create_dialogue` — Start Dialogue Session (Prakken)

Start a new argumentation dialogue session using Prakken's protocol.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | `string` | ✅ | The topic of the dialogue |
| `participants` | `List[string]` | ✅ | List of participant names |
| `type` | `string` | ❌ | Dialogue type. Default: `"persuasion"` |

**Example:**

```json
{
  "topic": "Should we migrate from REST to GraphQL?",
  "participants": ["Proponent", "Opponent"]
}
```

**Returns:** Serialized dialogue state with ID, commitment stores, and available moves.

---

### 8. `dialogue_move` — Make a Dialogue Move

Make a speech act move in an active dialogue session.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dialogue_id` | `string` | ✅ | ID from `create_dialogue` |
| `speaker` | `string` | ✅ | Participant name |
| `act` | `string` | ✅ | Speech act: `claim`, `why`, `concede`, `retract`, or `since` |
| `content` | `string` | ✅ | The content of the speech act |
| `premises` | `List[string]` | ❌ | Premises (required for `since` act) |

**Speech Act Protocol:**

| Speech Act | Meaning | Valid Responses |
|------------|---------|-----------------|
| `claim φ` | Assert φ is the case | `why φ`, `claim ¬φ`, `concede φ` |
| `why φ` | Challenge: ask for reasons | `since`, `retract` |
| `concede φ` | Admit φ is the case | — |
| `retract φ` | Withdraw commitment to φ | — |
| `since` | Provide reasons (premises) for φ | `why`, `concede` |

**Example:**

```json
{
  "dialogue_id": "d-abc123",
  "speaker": "Proponent",
  "act": "claim",
  "content": "GraphQL reduces over-fetching and improves frontend performance"
}
```

**Returns:** Updated dialogue state with commitment stores.

---

### 9. `diagnose_disagreement` — Diagnose Disagreement (ASPIC+)

Diagnose WHY two agents disagree, classifying the root cause of the disagreement.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_a` | `Dict` | ✅ | Agent A's position with `claim`, `premises`, and `rules` |
| `agent_b` | `Dict` | ✅ | Agent B's position with `claim`, `premises`, and `rules` |

**Disagreement Types:**

| Type | Meaning | Resolution Strategy |
|------|---------|---------------------|
| **Factual** | Different data/evidence | Gather more data |
| **Inferential** | Same data, different conclusions | Examine reasoning rules |
| **Preferential** | Same conclusions, different priorities | Negotiate weights |
| **Goal conflict** | Fundamentally incompatible objectives | Escalate for human decision |

**Example:**

```json
{
  "agent_a": {
    "claim": "Use microservices",
    "premises": ["System needs to scale independently", "Teams work in isolation"],
    "rules": ["Independent scaling requires service boundaries"]
  },
  "agent_b": {
    "claim": "Use monolith",
    "premises": ["Team is small", "Deployment complexity is a risk"],
    "rules": ["Small teams benefit from simple deployment"]
  }
}
```

**Returns:** `{ diagnosis, suggestedResolutions }`

---

### 10. `list_schemes` — List Argumentation Schemes

List all available Walton argumentation schemes with their critical question counts.

**Parameters:** None

**Returns:** `{ schemes: [{ name, title, criticalQuestions }] }`

---

## ⚡ Skill Commands (Slash Commands)

Skills are **shortcut commands** that trigger structured reasoning workflows. Use them directly in conversation with an AI agent that has warrant-mcp connected.

### `/argue` — Structured Argumentation

Build a rigorous, evidence-based argument for (or against) a technical claim.

```
/argue <claim>
/argue --challenge <claim>
/argue --deep <claim>
```

| Flag | Description |
|------|-------------|
| *(default)* | Support mode — build the strongest case FOR the claim |
| `--challenge` | Challenge mode — find the strongest attacks AGAINST the claim |
| `--deep` | Deep mode — spawn a dedicated agent for thorough analysis |

**What it does:**

1. Parses the claim type (Causal / Evaluative / Prescriptive / Factual / Authority)
2. Gathers evidence from the codebase and conversation history
3. Builds a Toulmin argument (Claim → Data → Warrant → Backing → Rebuttal → Qualifier)
4. Applies Walton's critical questions for the relevant argumentation scheme
5. Identifies defeaters (Pollock: Rebutting vs Undercutting)
6. Scores the argument using gradual semantics [0, 1]
7. Outputs a structured analysis with score breakdown and actionable recommendation

**Example:**

```
/argue "We should migrate from REST to GraphQL for our mobile API"
/argue --challenge "Microservices is the right architecture for our 5-person team"
```

---

### `/debate` — Multi-Agent Adversarial Debate

Run a structured adversarial debate between virtual agents to stress-test a technical decision.

```
/debate <topic>
/debate <topic> --rounds 3
/debate <topic> --focus security
/debate <topic> --full
```

| Flag | Description |
|------|-------------|
| `--rounds N` | Number of debate rounds (default: 2) |
| `--focus DOMAIN` | Focus opponent's perspective: `security`, `performance`, `cost`, `maintenance` |
| `--full` | Full debate mode — spawns 3 separate agents (PRO, OPP, MOD) for maximum diversity |

**Participants:**

| Role | Persona | Bias |
|------|---------|------|
| **PRO** (Proponent) | Pragmatic engineer | Prefers solutions that ship fast and are easy to maintain |
| **OPP** (Opponent) | Cautious architect | Prefers solutions that minimize risk and technical debt |
| **MOD** (Moderator) | Senior staff engineer | None — evaluates argument strength, not rhetoric |

**What it produces:**

- Full debate transcript with speech acts (Prakken's protocol)
- Commitment stores (what each side publicly committed to and retracted)
- Argumentation framework (arguments + attack/support relations with ASCII map)
- Argument scores via gradual semantics
- Moderator's verdict with winner, consensus solution, and conditions for revisiting

**Example:**

```
/debate "Should we rewrite the payment service in Rust?"
/debate "Monorepo vs polyrepo for our growing team" --rounds 3
/debate "Adopting Kubernetes for our infrastructure" --focus cost
```

---

### `/deliberate` — Collaborative Multi-Perspective Deliberation

Facilitate a cooperative multi-perspective analysis where virtual experts work together (not against each other) to find the best course of action.

```
/deliberate <decision question>
/deliberate <decision question> --perspectives 3
/deliberate <decision question> --perspectives "frontend,backend,data"
/deliberate <decision question> --criteria "security,cost,speed"
/deliberate <decision question> --deep
```

| Flag | Description |
|------|-------------|
| `--perspectives N` | Number of perspectives (default: 4) |
| `--perspectives "a,b,c"` | Custom named perspectives |
| `--criteria "x,y,z"` | Custom evaluation criteria (default: Business Value, Feasibility, Cost, Timeline, Risk, Maintainability) |
| `--deep` | Deep mode — spawn a dedicated agent for complex decisions requiring extensive research |

**Default Perspectives:**

| Role | Focus | Optimizes For |
|------|-------|---------------|
| **ARCHITECT** | System design, scalability, patterns | Technical excellence |
| **OPERATOR** | DevOps, deployment, monitoring, cost | Operational reliability |
| **PRODUCT** | Business value, user impact, timeline | Delivery & impact |
| **SECURITY** | Threat modeling, compliance, data safety | Safety & compliance |

**What it produces:**

- Perspective analysis with gathered evidence
- Proposals with Walton's Practical Reasoning critical questions answered
- Cross-evaluation with disagreement diagnosis (ASPIC+: factual / inferential / preferential / goal conflict)
- Decision matrix with weighted multi-criteria scores
- Consensus solution with incorporated concerns from all sides
- Dissenting opinions preserved as "canary signals"
- Action plan with concrete steps, checkpoints, and re-deliberation triggers

**Example:**

```
/deliberate "How should we handle authentication for our new public API?"
/deliberate "Which database should we use for the analytics pipeline?" --perspectives "data-engineer,backend,devops"
/deliberate "Should we build or buy a feature flag system?" --criteria "cost,integration,flexibility,maintenance"
```

---

## 🤖 Agent Triggers

Agents are **autonomous reasoning personas** that perform deep, multi-step analysis. They are defined in `.claude/agents/` and can be triggered by the AI when executing skill commands in `--deep` or `--full` mode.

### `argue` Agent — Structured Argumentation Agent

A rigorous evidence-based argument builder that uses Toulmin's Model, Walton's Schemes, and Pollock's Defeaters.

**Triggered by:** `/argue --deep <claim>`

**Process:**
1. Parse claim type → Gather evidence (with quality tags: `[CERTAIN]`, `[OBJECTIVE]`, `[UNCERTAIN]`, `[SUBJECTIVE]`, `[HYPOTHETICAL]`) → Build Toulmin argument → Apply Walton's critical questions → Identify defeaters (Pollock) → Calculate argument strength [0, 1]

**Score interpretation:**

| Score | Qualifier |
|-------|-----------|
| 0.8+ | Strongly recommended |
| 0.6–0.8 | Recommended |
| 0.4–0.6 | Viable but uncertain |
| 0.2–0.4 | Weak — consider alternatives |
| < 0.2 | Not recommended |

---

### `debate` Agent — Multi-Agent Debate Orchestrator

Runs a structured adversarial debate using Prakken's Persuasion Dialogue Model with Dung's semantics and gradual scoring.

**Triggered by:** `/debate --full <topic>`

**Process:**
1. Setup 3 virtual debater personas (PRO, OPP, MOD) → Information gathering → Execute Prakken's protocol (speech acts with commitment stores) → Build Bipolar Argumentation Framework → Compute acceptability via gradual semantics → Moderator verdict

---

### `deliberate` Agent — Collaborative Deliberation Facilitator

Facilitates cooperative multi-perspective analysis using Walton & Krabbe's Deliberation Dialogue model.

**Triggered by:** `/deliberate --deep <question>`

**Process:**
1. Assemble perspectives (4 domain experts) → Information seeking phase → Proposal generation (Walton's Practical Reasoning) → Cross-perspective evaluation with ASPIC+ disagreement diagnosis → Multi-criteria decision matrix → Consensus building → Action plan generation

---

## 🧩 Choosing the Right Tool

| Situation | Use |
|-----------|-----|
| You have a claim and want to build/validate an argument | `/argue` |
| You want to stress-test a decision with adversarial scrutiny | `/debate` |
| You need a collaborative, multi-perspective decision analysis | `/deliberate` |
| You want to compare two arguments mathematically | `score_arguments` tool |
| You need to classify a counterargument | `classify_defeater` tool |
| You want to run a step-by-step formal dialogue | `create_dialogue` + `dialogue_move` tools |
| You need to understand why two positions conflict | `diagnose_disagreement` tool |

---

## Development

```bash
# Run tests
uv run pytest

# Run specific test
uv run pytest tests/test_core.py -v

# Run with coverage
uv run pytest --cov=warrant_mcp
```

## Project Structure

```
warrant-mcp/
├── src/warrant_mcp/
│   ├── __init__.py
│   ├── server.py           # MCP server — exposes 10 tools
│   └── core/               # Core argumentation modules
│       ├── dung.py          # Abstract Argumentation Framework
│       ├── bipolar.py       # Bipolar AF (attack + support)
│       ├── gradual.py       # Gradual semantics (h-Categorizer, Counting)
│       ├── toulmin.py       # Toulmin argument model
│       ├── walton.py        # Walton's argumentation schemes
│       ├── pollock.py       # Pollock's defeasible reasoning
│       ├── prakken.py       # Prakken's dialogue protocol
│       └── aspic.py         # ASPIC+ disagreement diagnosis
├── tests/                   # Test suite
├── .claude/
│   ├── agents/              # Agent definitions (autonomous reasoning personas)
│   │   ├── argue.md         # Structured argumentation agent
│   │   ├── debate.md        # Multi-agent debate orchestrator
│   │   └── deliberate.md    # Collaborative deliberation facilitator
│   └── skills/              # Skill definitions (slash commands)
│       ├── argue.md         # /argue skill
│       ├── debate.md        # /debate skill
│       └── deliberate.md    # /deliberate skill
├── pyproject.toml
└── README.md
```

## Theoretical Background

### Dung's Abstract Argumentation Framework (1995)

Models arguments and attacks as a directed graph. Semantics determine acceptable arguments:

- **Grounded**: Skeptical, unique extension.
- **Preferred**: Credulous, maximal admissible sets.
- **Stable**: Conflict-free sets that attack everything outside.

### Toulmin's Argument Model (1958)

Structures arguments with Claim, Data, Warrant, Backing, Rebuttal, and Qualifier.

### Walton's Argumentation Schemes (1996)

Presumptive reasoning templates with critical questions (e.g., Expert Opinion, Consequences, Practical Reasoning, Analogy).

### Pollock's Defeasible Reasoning (1987)

Rebutting (contradicts conclusion) vs Undercutting (breaks inference) defeaters.

### Prakken's Dialogue Protocol (2006)

Formal dialogue with commitment stores and speech acts (claim, why, concede, retract, since).

### ASPIC+ Disagreement Diagnosis

Classifies disagreements as Factual, Inferential, Preferential, or Goal Conflict.

### Bipolar Argumentation Framework

Extended AF with both attack and support relations between arguments. Enables richer modeling of argument interactions including supported attacks and secondary attacks.

### Gradual Semantics

Scores arguments on a continuous [0, 1] scale instead of binary accept/reject. Methods: h-Categorizer and Counting semantics.

## License

MIT
