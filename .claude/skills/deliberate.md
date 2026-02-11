# /deliberate — Collaborative Deliberation Skill

Facilitate a multi-perspective collaborative analysis to converge on the best course of action.

## Usage

```
/deliberate <decision question>
/deliberate <decision question> --perspectives 3
/deliberate <decision question> --criteria "security,cost,speed"
```

## Instructions

When the user invokes `/deliberate`, facilitate a cooperative deliberation using the process defined in `.claude/agents/deliberate.md`.

Unlike `/debate` (adversarial), `/deliberate` is **cooperative** — perspectives work together to find the best solution, not to defeat each other.

### Execution Strategy

1. **Assemble perspectives** (default: Architect, Operator, Product, Security)
2. **Information seeking** — Each perspective researches the question from their domain
3. **Proposal generation** — Each perspective proposes an approach using Walton's Practical Reasoning
4. **Cross-evaluation** — Every perspective critiques every proposal (including their own)
5. **Decision matrix** — Multi-criteria weighted scoring
6. **Consensus building** — Rank, synthesize, or escalate
7. **Action plan** — Concrete steps with checkpoints

### Custom Perspectives (`--perspectives`)

```
/deliberate "..." --perspectives "frontend,backend,data"
```

This creates domain-specific perspectives instead of the defaults.

### Custom Criteria (`--criteria`)

```
/deliberate "..." --criteria "security,compliance,user-experience,performance"
```

Override the default evaluation criteria (Business Value, Feasibility, Cost, Timeline, Risk, Maintainability).

### Quick Mode (default)

Run the full deliberation in the current context by simulating all perspectives. Suitable for most decisions.

### Deep Mode (`--deep`)

Spawn the `deliberate` agent via Task tool for complex decisions that require extensive codebase research across multiple domains.

## Output

Produce the structured output format defined in `.claude/agents/deliberate.md`, including:
- Perspective analysis with gathered evidence
- Proposals with critical question answers
- Cross-evaluation with disagreement diagnosis (ASPIC+)
- Decision matrix with weighted scores
- Consensus solution with incorporated concerns
- Dissenting opinions (preserved)
- Action plan with checkpoints and re-deliberation triggers

## Key Principles

- Cooperative, not adversarial
- All perspectives heard and recorded
- Classify disagreements (factual/inferential/preferential/goal conflict)
- Reversibility premium (prefer undoable decisions)
- Always evaluate "do nothing" as an option
- Preserve dissenting opinions as canary signals
