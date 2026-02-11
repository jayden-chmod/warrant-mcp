# warrant-mcp

An MCP (Model Context Protocol) server that provides formal reasoning and argument validation tools for AI agents. Built on established computational argumentation theories — Dung, Toulmin, Walton, Pollock, Prakken, and ASPIC+.

Migrated from Node.js/TypeScript to Python/uv.

## Features

- **Dung's Abstract Argumentation Framework**: Extensions (grounded, preferred, stable).
- **Toulmin Model**: Structured argument validation.
- **Walton's Schemes**: Critical questions for common reasoning patterns.
- **Pollock's Defeasible Reasoning**: Rebutting and undercutting defeaters.
- **Prakken's Dialogue Protocol**: Persuasion dialogue management.
- **ASPIC+**: Disagreement diagnosis.
- **Gradual Semantics**: Argument scoring (h-Categorizer, Counting).

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

## Development

```bash
# Run tests
uv run pytest
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

Presumptive reasoning templates with critical questions (e.g., Expert Opinion, Consequences).

### Pollock's Defeasible Reasoning (1987)

Rebutting (contradicts conclusion) vs Undercutting (breaks inference) defeaters.

### Prakken's Dialogue Protocol (2006)

Formal dialogue with commitment stores and speech acts (claim, why, concede, retract).

### ASPIC+ Disagreement Diagnosis

Classifies disagreements as Factual, Inferential, Preferential, or Goal Conflict.

## License

MIT
