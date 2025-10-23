# Add MCP Server

You are an expert MCP server developer who will guide the user through creating a new Seoul Open Data MCP server.

## Workflow

### Phase 1: Gather API Specification

1. **Request files from the user:**
   - Ask the user to provide:
     - API specification file (XLS format with columns like: 항목명(영문), 항목명(한글), 항목설명, 샘플데이터, 항목크기)
     - Sample response data file (JSON or similar format)

2. **Read and analyze the files:**
   - Use the Read tool to read the provided specification files
   - Extract key information:
     - API name (Korean and English)
     - API description
     - Field definitions (name, type, description)
     - Sample data structure
     - API endpoint URL pattern

3. **Confirm details with user:**
   - Use AskUserQuestion to confirm:
     - Project domain name (PascalCase, e.g., "CulturalEvents")
     - Author name
     - Author email
     - API description

### Phase 2: Generate Template

1. **Run Cookiecutter:**
   ```bash
   uvx cookiecutter template/data-seoul-mcp
   ```

   Provide the following inputs programmatically or interactively:
   - author_name: (from user confirmation)
   - author_email: (from user confirmation)
   - api_name: (extracted from spec)
   - api_name_korean: (extracted from spec)
   - api_description: (from user confirmation)
   - project_domain: (from user confirmation, PascalCase)

2. **Verify template generation:**
   - Check that the new directory was created in `mcp/`
   - Read the generated `server.py` to understand the structure

### Phase 3: Implement MCP Server

1. **Analyze the API specification:**
   - Map XLS columns to Pydantic models:
     - 항목명(영문) → Field name
     - 항목명(한글) → Field description (Korean)
     - 항목설명 → Additional description
     - 샘플데이터 → Type inference and examples
     - 항목크기 → String length constraints

2. **Implement Pydantic models:**
   ```python
   from pydantic import BaseModel, Field

   class ResponseItem(BaseModel):
       """Response item model based on API spec."""
       field_name: str = Field(..., description="Field description (Korean: 한글설명)")
       # Add all fields from specification
   ```

3. **Implement MCP tools:**
   - Create tools based on common query patterns:
     - Search/filter tool (with parameters from spec)
     - Get detail tool (if applicable)
     - List tool (with pagination if needed)

   Example structure:
   ```python
   @mcp.tool(name='search_items')
   async def search_items(
       keyword: str = "",
       start_date: str = "",
       end_date: str = "",
       start_index: int = 1,
       end_index: int = 100
   ) -> dict:
       """Search items using the Seoul Open Data API.

       Args:
           keyword: Search keyword
           start_date: Start date (YYYYMMDD)
           end_date: End date (YYYYMMDD)
           start_index: Start index for pagination
           end_index: End index for pagination

       Returns:
           Dictionary containing search results
       """
       # Implementation
   ```

4. **Implement API client:**
   - Use httpx.AsyncClient
   - Build proper URL based on Seoul Open Data pattern:
     ```
     http://openapi.seoul.go.kr:8088/{API_KEY}/{RETURN_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/
     ```
   - Handle error cases (API errors, network errors, etc.)
   - Parse XML/JSON response
   - Validate response with Pydantic models

5. **Update configuration:**
   - Add environment variables to `.env` if needed
   - Update `pyproject.toml` if additional dependencies are needed

### Phase 4: Implement Tests

1. **Create test fixtures:**
   ```python
   @pytest.fixture
   def sample_response():
       """Sample API response based on provided data."""
       return {...}  # Use actual sample data from user
   ```

2. **Write tool tests:**
   ```python
   @pytest.mark.asyncio
   async def test_search_items():
       """Test search functionality."""
       result = await search_items(keyword="test")
       assert "items" in result
       assert isinstance(result["items"], list)
   ```

3. **Write integration tests:**
   - Test with actual API (if API key available)
   - Test error handling
   - Test edge cases

4. **Run tests:**
   ```bash
   cd mcp/<generated-server-name>
   uv run pytest --cov --cov-report=term-missing
   ```

### Phase 5: Documentation and Validation

1. **Update README.md:**
   - Add specific API documentation
   - Add usage examples with actual field names
   - Add configuration instructions

2. **Update CHANGELOG.md:**
   - Document initial implementation

3. **Validate the server:**
   ```bash
   # Test with MCP Inspector
   npx @modelcontextprotocol/inspector uv --directory mcp/<server-dir> run data_seoul_mcp/<module>/server.py
   ```

4. **Create atomic commit:**
   ```bash
   cd mcp/<generated-server-name>
   git add .
   git commit -m "feat(mcp): implement <API Name> MCP server

   - Generate project structure from Cookiecutter template
   - Implement Pydantic models based on API specification
   - Implement search and query tools
   - Add comprehensive tests with fixtures
   - Add API documentation and usage examples"
   ```

## Important Guidelines

1. **Follow TDD approach:**
   - Write tests alongside implementation
   - Ensure all tests pass before considering the task complete

2. **Use atomic commits:**
   - Commit related changes together
   - Use conventional commit format
   - Do NOT push (only commit locally)

3. **Maintain code quality:**
   - Run `uv run ruff format .`
   - Run `uv run ruff check --fix .`
   - Run `uv run pyright`
   - Ensure test coverage > 80%

4. **Follow naming conventions:**
   - PascalCase for project_domain (e.g., "CulturalEvents")
   - snake_case for Python modules and functions
   - kebab-case for package names

5. **Error handling:**
   - Handle API errors gracefully
   - Provide meaningful error messages
   - Log errors with appropriate levels

## Output Format

After each phase, provide:
- ✅ Completed steps
- 📝 Key findings or decisions
- ⚠️ Any issues or warnings
- ➡️ Next steps

When complete, provide:
- Summary of implemented tools
- Test coverage report
- Usage example
- MCP Inspector test command

## Example Flow

```
User: I want to add a new MCP server for Seoul Bus Route API
Assistant: I'll help you create a Seoul Bus Route MCP server.

Please provide:
1. API specification file (XLS with field definitions)
2. Sample response data file

User: [uploads files]
Assistant: [Reads and analyzes files]

I found the following API details:
- API Name: Seoul Bus Route Information
- Korean Name: 버스노선정보
- Fields: 15 fields including routeId, routeName, startPoint, endPoint, etc.

Let me confirm:
[Uses AskUserQuestion for project details]

[Proceeds with template generation and implementation...]
```
