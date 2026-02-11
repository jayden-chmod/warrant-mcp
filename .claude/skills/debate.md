# /debate — Multi-Agent Debate Skill

Run a structured adversarial debate between virtual agents to stress-test a technical decision.

## Usage

```
/debate <topic>
/debate <topic> --rounds 3
/debate <topic> --focus security
```

## Instructions

When the user invokes `/debate`, orchestrate a formal argumentation-based debate using the protocol defined in `.claude/agents/debate.md`.

### Execution Strategy

For a debate, you SHOULD spawn multiple agents to get genuinely diverse perspectives:

1. **Spawn the debate orchestrator agent** via Task tool with `subagent_type: "general-purpose"` using the debate agent prompt
2. Alternatively, for maximum diversity, use **TeamCreate** to set up:
   - A Proponent agent (argues FOR)
   - An Opponent agent (argues AGAINST)
   - A Moderator agent (judges)
3. Each agent conducts independent research before arguing

### Quick Debate (default)

If the topic is focused and the user wants a fast result, run the debate in a single agent context by simulating the three perspectives internally. Follow Prakken's dialogue protocol strictly.

### Full Debate (`--full`)

If `--full` is specified or the decision is high-stakes:
1. Create a team with TeamCreate
2. Spawn 3 separate agents (PRO, OPP, MOD)
3. Use TaskCreate to structure the debate rounds
4. Agents communicate via SendMessage
5. Moderator collects results and renders verdict

### Focus Mode (`--focus DOMAIN`)

When a focus is specified, adjust the Opponent's perspective to emphasize that domain:
- `--focus security` → Opponent argues from security risks
- `--focus performance` → Opponent focuses on performance implications
- `--focus cost` → Opponent emphasizes cost/resource concerns
- `--focus maintenance` → Opponent highlights long-term maintenance burden

## Output

Produce the structured output format defined in `.claude/agents/debate.md`, including:
- Full debate transcript with speech acts
- Commitment stores (final state)
- Argumentation framework (arguments + attack/support relations)
- Argument scores via gradual semantics
- Moderator's verdict with consensus solution
- Conditions for revisiting the decision

## Key Principles

- Steel-man both sides (strongest possible version of each argument)
- Evidence required for every claim
- Honest concessions when a position is indefensible
- Prefer undercutting analysis over simple rebuttals
- Convergence guaranteed within max rounds
