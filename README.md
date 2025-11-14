# Blog Post Creator Agent

An intelligent multi-agent system built with LangChain and CrewAI that automatically researches, writes, and publishes blog posts to Ghost CMS.

## Features

- **Automated Research**: Uses Tavily API to search the web for current information on any topic
- **Intelligent Writing**: Leverages GPT-4 or Claude to create well-structured, engaging blog posts
- **Automatic Publishing**: Publishes directly to Ghost CMS with proper formatting and tags
- **Multi-Agent Collaboration**: CrewAI-powered specialized agents (Researcher, Writer, Publisher) working together
- **Multiple Implementations**: Choose between CrewAI multi-agent, LangChain agent, or simple chain
- **Flexible LLM Support**: Works with OpenAI (GPT-4) or Anthropic (Claude) models
- **Built-in Observability**: Track agent performance, task execution, and content quality metrics
- **Content Evaluation**: Automated quality assessment for readability, structure, and SEO

## Architecture

The system offers three implementations:

### 1. CrewAI Multi-Agent System (Recommended)
A sophisticated multi-agent collaboration using CrewAI framework with specialized agents:

**Agents:**
- **Content Researcher**: Expert at finding comprehensive, accurate information using web search
- **Blog Content Writer**: Professional writer creating engaging, SEO-optimized content
- **Content Publisher**: Publishing specialist handling Ghost CMS integration and metadata

**Workflow:**
1. **Research Task**: Researcher gathers facts, statistics, trends, and insights
2. **Title Generation**: Writer creates compelling, SEO-friendly title
3. **Content Creation**: Writer produces well-structured HTML content (800-1500 words)
4. **Tag Generation**: Writer generates relevant tags for categorization
5. **Publishing**: Publisher posts to Ghost CMS with proper formatting

**Advantages:**
- Clear separation of concerns with specialized agents
- Built-in task dependencies and context sharing
- Sequential process ensures quality at each stage
- Integrated observability and evaluation
- Better handling of complex workflows

### 2. Full Agent (BlogPostAgent)
Uses LangChain's agent framework with tool-calling capabilities for autonomous operation.

### 3. Simple Chain (SimpleResearchWriter)
A more predictable step-by-step approach:
1. **Research**: Searches the web using Tavily
2. **Title Generation**: Creates an SEO-friendly title
3. **Content Creation**: Writes the blog post with proper HTML formatting
4. **Tag Generation**: Creates relevant tags
5. **Publishing**: Posts to Ghost CMS

## Prerequisites

1. **Python 3.9+**
2. **API Keys**:
   - OpenAI API key OR Anthropic API key
   - Tavily API key (for web search)
   - Ghost Admin API key

## Installation

1. **Clone or navigate to this directory**:
   ```bash
   cd /Users/osa/Documents/storyland/agents/post-creator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   # Choose your LLM provider
   LLM_PROVIDER=openai  # or "anthropic"

   # OpenAI (if using GPT-4)
   OPENAI_API_KEY=sk-...

   # OR Anthropic (if using Claude)
   ANTHROPIC_API_KEY=sk-ant-...

   # Tavily (required for web search)
   TAVILY_API_KEY=tvly-...

   # Ghost CMS
   GHOST_URL=https://your-ghost-site.com
   GHOST_ADMIN_API_KEY=your_ghost_id:your_ghost_secret
   ```

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

### Anthropic API Key (Alternative to OpenAI)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key

### Tavily API Key
1. Go to https://tavily.com/
2. Sign up for an account
3. Get your API key from the dashboard

### Ghost Admin API Key

To get your Ghost Admin API Key, follow these steps:

1. **Log into your Ghost admin panel**
   - Navigate to your Ghost site (e.g., `https://your-site.com`)
   - Click "Sign in" and enter your credentials

2. **Navigate to Settings**
   - In the left sidebar, click on "Settings" (gear icon)
   - Click on "Integrations"

3. **Create a Custom Integration**
   - Click the "Add custom integration" button
   - Give it a descriptive name (e.g., "Blog Creator Agent" or "Post Creator")
   - Click "Create"

4. **Copy the Admin API Key**
   - In the integration details, you'll see an "Admin API Key" section
   - The key will be displayed in the format: `id:secret` (e.g., `5f8e3b2a1c4d6e7f:8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2`)
   - Click "Copy" next to the Admin API Key to copy the entire key (both ID and secret)
   - **Important**: You need the full key in the format `id:secret` - both parts separated by a colon

5. **Copy your Ghost Site URL**
   - Make sure you have your Ghost site URL (e.g., `https://your-site.com` or `https://your-site.ghost.io`)
   - Include the `https://` protocol
   - Don't include a trailing slash

6. **Add to your .env file**
   ```env
   GHOST_URL=https://your-site.com
   GHOST_ADMIN_API_KEY=your_id:your_secret
   ```
   - Replace `your_id:your_secret` with the actual key you copied
   - Make sure there are no spaces around the colon

**Note**: The Admin API Key has full access to your Ghost site, so keep it secure and never commit it to version control. The `.env` file should already be in your `.gitignore`.

## Usage

### Interactive Mode

Run the main script and follow the prompts:

```bash
python main.py
```

You'll be asked to:
1. Enter your blog topic description
2. Choose between three implementations:
   - **Option 1**: Full Agent (LangChain - more autonomous)
   - **Option 2**: Simple Chain (LangChain - step-by-step)
   - **Option 3**: CrewAI Multi-Agent (Recommended - structured workflow)

### Command Line Mode

Provide the topic as command-line arguments:

```bash
python main.py "Write about the latest trends in AI and machine learning"
```

### Programmatic Usage

Use in your own Python code:

**Option 1: CrewAI Multi-Agent (Recommended)**
```python
from src.agents.crew_agent import BlogPostCrew

# Create the crew
crew = BlogPostCrew()

# Define your topic
topic = """Write a blog post about sustainable living practices
for urban dwellers. Include practical tips and recent statistics."""

# Create and publish
result = crew.create_and_publish_post(topic)
print(result)
```

**Option 2: LangChain Simple Chain**
```python
from src.agents.langchain_agent import SimpleResearchWriter

# Create the writer
writer = SimpleResearchWriter()

# Define your topic
topic = """Write a blog post about sustainable living practices
for urban dwellers. Include practical tips and recent statistics."""

# Create and publish
result = writer.create_and_publish_post(topic)
print(result)
```

**Option 3: LangChain Full Agent**
```python
from src.agents.langchain_agent import BlogPostAgent

# Create the agent
agent = BlogPostAgent()

# Define your topic
topic = """Write a blog post about sustainable living practices
for urban dwellers. Include practical tips and recent statistics."""

# Create and publish
result = agent.create_and_publish_post(topic)
print(result)
```

### Examples

Run the example script:

```bash
# CrewAI multi-agent system (recommended)
python examples/example.py crewai

# LangChain simple step-by-step writer
python examples/example.py simple

# LangChain full agent implementation
python examples/example.py agent

# Short topic examples
python examples/example.py short
```

### Interactive Jupyter Notebook

For interactive testing and experimentation, use the Jupyter notebook:

```bash
# Start Jupyter
jupyter notebook

# Then open: notebooks/test_agents.ipynb
```

The notebook provides:
- Pre-configured test topics
- Interactive testing of all three implementations
- Side-by-side comparison tools
- Debugging and exploration cells
- Quick test functions for rapid iteration

## Project Structure

```
post-creator/
├── src/                           # Source code directory
│   ├── __init__.py
│   ├── agents/                    # Agent implementations
│   │   ├── __init__.py
│   │   ├── langchain_agent.py    # LangChain agents (Full Agent & Simple Chain)
│   │   └── crew_agent.py         # CrewAI multi-agent system (RECOMMENDED)
│   ├── tools/                     # Tool implementations
│   │   ├── __init__.py
│   │   ├── langchain_tools.py    # LangChain tools (Tavily, Ghost)
│   │   └── crew_tools.py         # CrewAI tools (Tavily, Ghost)
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       ├── config.py             # Configuration and environment validation
│       ├── observability.py      # Agent performance tracking and metrics
│       └── evaluation.py         # Content quality evaluation system
├── notebooks/                     # Jupyter notebooks for testing
│   └── test_agents.ipynb         # Interactive agent testing notebook
├── examples/                      # Example scripts
│   └── example.py                # Usage examples for all implementations
├── docs/                          # Documentation
│   ├── QUICKSTART.md             # Quick start guide
│   ├── OBSERVABILITY.md          # Observability documentation
│   └── EVALUATION.md             # Evaluation framework documentation
├── main.py                        # CLI entry point
├── setup.sh                       # Setup script
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment variables
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## How It Works

### CrewAI Multi-Agent System (Recommended)

The CrewAI implementation uses a collaborative team of specialized agents:

1. **Research Task** (Content Researcher Agent):
   - Receives the topic description
   - Uses Tavily search tool to gather comprehensive information
   - Collects facts, statistics, trends, and expert insights
   - Produces a detailed research summary

2. **Title Generation Task** (Blog Content Writer Agent):
   - Reviews the research findings
   - Creates a compelling, SEO-friendly title (50-70 characters)
   - Ensures clarity and keyword relevance

3. **Content Creation Task** (Blog Content Writer Agent):
   - Uses research insights to write engaging content
   - Produces 800-1500 words in proper HTML format
   - Structures content with H2/H3 headings, paragraphs, and lists
   - Maintains consistency with title and research

4. **Tag Generation Task** (Blog Content Writer Agent):
   - Analyzes title and content
   - Generates 3-5 relevant tags for categorization
   - Ensures tags are useful for SEO and discovery

5. **Publishing Task** (Content Publisher Agent):
   - Receives title, content, and tags from previous tasks
   - Uses Ghost publish tool to create the post
   - Returns confirmation with published post URL

**Benefits of CrewAI Approach:**
- **Task Dependencies**: Each task has access to outputs from previous tasks
- **Specialization**: Each agent has a clear role and expertise
- **Process Control**: Sequential execution ensures quality at each stage
- **Built-in Metrics**: Automatic tracking of task duration and agent performance
- **Quality Assurance**: Integrated content evaluation and scoring

### SimpleResearchWriter (LangChain)

Step-by-step approach using LangChain:

1. **Research Phase**: Searches the web using Tavily for current information
2. **Writing Phase**: Generates title and creates well-structured HTML content
3. **Publishing Phase**: Generates tags and publishes to Ghost CMS

### BlogPostAgent (LangChain - Advanced)

Autonomous LangChain agent that:
- Decides when to search for information
- Determines how much research is needed
- Writes and structures the content
- Publishes to Ghost

## Customization

### Change LLM Model

**For CrewAI (crew_agent.py):**
```python
# For OpenAI
self.llm = ChatOpenAI(
    model="gpt-4-turbo-preview",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0.7,
)

# For Anthropic
self.llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # or "claude-3-opus-20240229"
    temperature=0.7,
)
```

**For LangChain (agent.py):**
```python
# Same as above
self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7)
# or
self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
```

### Customize Agent Roles and Tasks (CrewAI)

Edit `crew_agent.py` to modify agent behaviors:

```python
# Customize the researcher
def _create_researcher(self) -> Agent:
    return Agent(
        role="Content Researcher",
        goal="Your custom goal",
        backstory="Your custom backstory...",
        tools=[self.search_tool],
        llm=self.llm,
        verbose=True,
    )

# Customize task descriptions in create_tasks()
research_task = Task(
    description="Your custom research instructions...",
    expected_output="What you expect as output...",
    agent=self.researcher,
)
```

### Adjust Content Length

Modify the prompt in `agent.py`:

```python
content_prompt = f"""Write a comprehensive blog post (1500-2500 words) about: {topic_description}
```

### Change Post Status

In `tools.py`, modify the `GhostPublishTool`:

```python
post_data = {
    "posts": [{
        # ...
        "status": "draft",  # or "published"
    }]
}
```

### Add More Tools

Create new tools in `tools.py`:

```python
class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "What this tool does"

    def _run(self, input: str) -> str:
        # Your tool logic
        return result
```

Then add to `get_all_tools()` function.

### Configure Observability and Evaluation (CrewAI)

The CrewAI implementation includes built-in observability and evaluation features. Configure them in your `.env` file:

```env
# Observability Settings
ENABLE_OBSERVABILITY=true          # Track agent performance and metrics
EXPORT_METRICS=true                # Export metrics to JSON files

# LangSmith Integration (optional)
ENABLE_LANGSMITH=true              # Enable LangSmith tracing
LANGSMITH_API_KEY=your_key_here    # Your LangSmith API key
LANGSMITH_PROJECT=blog-post-creator # Project name in LangSmith

# Evaluation Settings
ENABLE_EVALUATION=true             # Evaluate content quality
EXPORT_EVALUATION=true             # Export evaluation results to JSON
MIN_QUALITY_SCORE=0.7             # Minimum acceptable quality score (0-1)
```

**What you get:**
- **Agent Metrics**: Track LLM calls, tokens used, errors, and execution time per agent
- **Task Metrics**: Monitor task duration, status, and outputs
- **Content Evaluation**: Automatic scoring for readability, structure, completeness, and SEO
- **LangSmith Tracing**: Visualize agent interactions and debug in LangSmith dashboard
- **Quality Warnings**: Get alerted if content quality falls below threshold

See `OBSERVABILITY.md` and `EVALUATION.md` for detailed documentation.

## Troubleshooting

### "Missing required environment variables"
- Make sure you've created a `.env` file
- Check that all required variables are set
- Verify API keys are valid

### "Error publishing to Ghost"
- Verify your Ghost URL is correct (include https://)
- Check your Admin API key format (should be `id:secret`)
- Ensure your Ghost integration has Admin API access

### "Tavily search failed"
- Verify your Tavily API key
- Check your internet connection
- Ensure you haven't exceeded rate limits

### Agent uses too many tokens
- Use `BlogPostCrew` (CrewAI) for better token efficiency with structured workflow
- Use `SimpleResearchWriter` instead of `BlogPostAgent` for LangChain
- Reduce the `max_iterations` in `agent.py` for the full agent
- Use a smaller model like GPT-3.5-turbo
- Monitor token usage with observability features (CrewAI)

### CrewAI-specific issues
- **Tasks not completing**: Check agent verbose output for errors
- **Quality score too low**: Adjust task descriptions or provide more detailed topics
- **Missing task outputs**: Ensure task dependencies are properly configured in `create_tasks()`

## Tips for Best Results

1. **Use CrewAI for Production**: The multi-agent system provides better consistency and quality
2. **Be Specific**: Provide clear, detailed topic descriptions
3. **Include Context**: Mention the target audience, tone, or specific angles
4. **Use Examples**: Reference similar posts or specific points to cover
5. **Enable Evaluation**: Turn on content evaluation to monitor quality metrics
6. **Review Output**: Check the generated content and evaluation scores before publishing
7. **Monitor Metrics**: Use observability features to track token usage and optimize costs
8. **Start with Drafts**: Set Ghost status to "draft" initially to review before making posts live

## Example Topics

```python
# Detailed topic
"Write a comprehensive guide about starting a meditation practice for beginners.
Include scientific benefits, different meditation techniques, and a 30-day starter plan."

# Simple topic
"The impact of remote work on employee productivity"

# Technical topic
"Explain Docker containerization for web developers with practical examples"

# Current events
"Analyze the latest developments in renewable energy technology"
```

## License

MIT License - feel free to use and modify for your needs.

## Contributing

This is a personal project, but feel free to fork and adapt it for your use case!

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example usage in `example.py`
3. Verify your `.env` configuration

## Future Enhancements

Potential improvements:
- [ ] Support for featured images via DALL-E or Stable Diffusion
- [ ] Multiple Ghost site support (publish to multiple blogs)
- [ ] Scheduled publishing with cron integration
- [ ] Enhanced SEO optimization with keyword analysis
- [ ] Social media preview generation (OG tags, Twitter cards)
- [ ] A/B testing for titles and content variations
- [ ] Custom tone/style profiles per blog category
- [ ] Multi-language support with translation agents
- [ ] Image sourcing and attribution from Unsplash/Pexels
- [ ] Automated content calendar planning

## Credits

Built with:
- [CrewAI](https://www.crewai.io/) - Multi-agent orchestration framework
- [LangChain](https://python.langchain.com/) - Agent framework and tools
- [Tavily](https://tavily.com/) - Web search API
- [Ghost](https://ghost.org/) - Publishing platform
- [OpenAI](https://openai.com/) / [Anthropic](https://anthropic.com/) - Language models
- [LangSmith](https://smith.langchain.com/) - Observability and tracing (optional)
