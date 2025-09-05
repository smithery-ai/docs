# Python Server Discovery Mechanism

## The Missing Piece from Quickstart

The Python quickstart shows you how to write a `create_server` function but doesn't explain how Smithery actually finds and calls it. Here's the complete discovery mechanism.

## Configuration-Based Discovery

Smithery uses the `pyproject.toml` file to discover your server function:

```toml
[tool.smithery]
server = "hello_server.server:create_server"
```

This tells Smithery:
- Import the module `hello_server.server`
- Look for the function `create_server`
- Call it with a config object

## Module Contract

Your server module must export:

1. **Required**: A server creation function with this signature:
   ```python
   def create_server(config: ConfigSchema) -> SmitheryFastMCP:
       # Your server logic here
   ```

2. **Optional**: A config schema class:
   ```python
   config_schema = ConfigSchema  # Export at module level
   ```

## How Discovery Works

1. **Read Config**: Smithery reads `[tool.smithery].server` from `pyproject.toml`
2. **Import Module**: Uses Python's import system to load the specified module
3. **Find Function**: Looks for the named function (e.g., `create_server`)
4. **Find Schema**: Optionally looks for a `config_schema` variable in the same module
5. **Validate Contract**: Checks function signature and return type
6. **Instantiate**: Creates config instance and calls your function

## What Gets Validated

Smithery validates your module contract:

- Function exists and is callable
- Function takes exactly one parameter (the config)
- Return type annotation is `SmitheryFastMCP` (warning if missing)
- Config schema is a Pydantic `BaseModel` subclass (if provided)

## Common Patterns

```python
# server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from smithery import from_fastmcp
from smithery.server.fastmcp_patch import SmitheryFastMCP

class ConfigSchema(BaseModel):
    api_key: str
    debug: bool = False

def create_server(config: ConfigSchema) -> SmitheryFastMCP:
    server = from_fastmcp(FastMCP(name="My Server"))
    # Add your tools, resources, prompts
    return server

# Optional: Export schema for discovery
config_schema = ConfigSchema
```

## Why This Matters

This discovery mechanism enables:
- **Deployment**: Smithery can find your server function in production
- **Local Development**: `uv run dev` knows what to start
- **Configuration**: Users can provide session-specific config
- **Validation**: Type checking and contract enforcement

## Alternative Discovery Approaches

The current approach uses module-level variable discovery, but other approaches are possible:

### 1. Function Signature Inspection (Type Analysis)
```python
def create_server(config: ConfigSchema) -> SmitheryFastMCP:
    pass
# Smithery could inspect the type annotation of the config parameter
```
**Pros**: More explicit, no extra exports needed
**Cons**: Complex type analysis, doesn't work with generic types or forward references

### 2. Decorator-Based Discovery ⭐
```python
from smithery import server

@server(config_schema=ConfigSchema)
def create_server(config: ConfigSchema) -> SmitheryFastMCP:
    server = from_fastmcp(FastMCP(name="My Server"))
    # Add tools, resources, prompts
    return server
```

**Pros**: 
- Explicit and discoverable
- IDE-friendly with autocomplete
- Self-documenting code
- No magic variable names
- Could validate at decoration time
- Natural Python pattern

**Cons**: 
- Slightly more verbose
- Requires importing decorators
- Need to design decorator API carefully

**Enhanced possibilities:**
```python
@server(
    config_schema=ConfigSchema,
    name="My Server",
    description="Does cool things",
    version="1.0.0"
)
def create_server(config: ConfigSchema) -> SmitheryFastMCP:
    # Decorator could handle FastMCP creation
    pass
```

### 3. Class-Based Server Definition
```python
class MyServer(SmitheryServer):
    config_schema = ConfigSchema
    
    def create(self, config: ConfigSchema) -> SmitheryFastMCP:
        pass
```
**Pros**: Object-oriented, clear inheritance
**Cons**: More boilerplate, different paradigm from FastMCP

### 4. Configuration File Declaration
```toml
[tool.smithery]
server = "hello_server.server:create_server"
config_schema = "hello_server.server:ConfigSchema"  # Explicit
```
**Pros**: Centralized config, explicit
**Cons**: Duplication, more configuration to maintain

### 5. Return Type Analysis
```python
def get_config_schema() -> type[BaseModel]:
    return ConfigSchema

def create_server(config: ConfigSchema) -> SmitheryFastMCP:
    pass
```
**Pros**: Functional approach, explicit
**Cons**: Extra function, not as clean

### 6. Module Metadata
```python
__smithery_config_schema__ = ConfigSchema
# or
__all__ = ["create_server", "ConfigSchema"]
```
**Pros**: Python convention, explicit exports
**Cons**: Magic variable names, not obvious

## Current Approach Analysis

The current **module-level variable** approach (`config_schema = ConfigSchema`) is:

**Pros**:
- Simple and Pythonic
- No complex type analysis needed
- Works with any config schema structure
- Optional by design
- Easy to implement and understand

**Cons**:
- Not obvious to new developers
- Relies on naming convention
- Easy to forget the export
- No IDE hints about the requirement

## Recommendation

The current approach is solid, but documentation should be clearer about:
1. The module-level export requirement
2. The naming convention (`config_schema`)
3. That it's optional (defaults to empty config)

## Documentation Gap

The quickstart should mention:
1. The `[tool.smithery]` section in `pyproject.toml` is what connects everything
2. The optional `config_schema` export for schema discovery
3. The function signature contract that must be followed
4. The module-level variable naming convention
