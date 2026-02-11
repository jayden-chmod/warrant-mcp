# /argue — Structured Argumentation Skill

Build a rigorous, evidence-based argument for (or against) a technical claim using formal argumentation theory.

## Usage

```
/argue <claim>
/argue --challenge <claim>
```

## Instructions

When the user invokes `/argue`, follow the structured argumentation process defined in the `argue` agent (`.claude/agents/argue.md`).

You have access to the current conversation context. Use it as additional evidence.

### Quick Mode (default)

If the claim is straightforward, execute the argumentation analysis directly in the current context:

1. **Parse the claim type** (Causal / Evaluative / Prescriptive / Factual / Authority)
2. **Gather evidence** from the codebase and conversation history
3. **Build Toulmin argument** (Claim → Data → Warrant → Backing → Rebuttal → Qualifier)
4. **Apply Walton's critical questions** for the relevant argumentation scheme
5. **Identify defeaters** (Pollock: Rebutting vs Undercutting)
6. **Score the argument** using gradual semantics [0, 1]
7. **Output** the structured analysis

### Deep Mode

If the user adds `--deep` or the claim is complex (involves multiple subsystems, conflicting evidence, or architectural decisions), spawn the `argue` agent via Task tool for a thorough analysis.

### Challenge Mode

If `--challenge` is used, invert the analysis: find the strongest attacks against the claim instead of supporting it. This is useful for stress-testing your own proposals before presenting them.

## Output

Produce the structured output format defined in `.claude/agents/argue.md`, including:
- Argument score with breakdown
- Evidence table with quality tags
- Defeaters with strength classification
- Clear recommendation
- "What Would Change My Mind" section

## Key Principles

- Evidence over rhetoric
- Always surface the strongest counterarguments
- All conclusions are defeasible (provisional)
- No logical fallacies
