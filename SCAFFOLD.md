# Scaffold

## Get Started

- What is Smithery?
- Connect to an MCP server
    - Playground
    - TypeScript/Python Connect to Exa
- Build an MCP server
    - TypeScript: `npm create smithery` + `npm run dev`
    - Python: FastMCP + Streamable HTTP
        - Future: `uvx create`
- Best Practices
    - Profiles
    - Auth (high level/data policy)

## Concepts

- What is MCP?
    - Local v. Remote, STDIO v. SSE v. SHTTP
- What is the Playground?

## MCP clients

- Search for servers
- Connect to a Smithery server via OAuth
    - Next.js
    - FastAPI
    - Express.js
    - Hono
- Future: Add features to your client
    - Elicitation
    - Sampling

## MCP servers

- Best Practices
    - Smithery.yaml
    - Sample prompts
- Implement OAuth in your server
- Future:
    - Elicitation
    - Sampling

## CLI

- Get ngrok URL
- Use Playground
- Add servers to cursor/windsurf/etc.
- basically what’s in the [README](https://github.com/smithery-ai/cli)

## API reference

- Export OpenAPI spec from registry and [make it interactable](https://docs.browserbase.com/reference/api/create-a-session)