# Blog Post Creator Agent

An intelligent multi-agent system built with LangChain that automatically researches, writes, and publishes blog posts to Ghost CMS.

## Features

- **Automated Research**: Uses Tavily API to search the web for current information on any topic
- **Intelligent Writing**: Leverages GPT-4 or Claude to create well-structured, engaging blog posts
- **Automatic Publishing**: Publishes directly to Ghost CMS with proper formatting and tags
- **Multi-Agent Architecture**: Choose between full agent autonomy or step-by-step chain implementation
- **Flexible LLM Support**: Works with OpenAI (GPT-4) or Anthropic (Claude) models

## Architecture

The system offers two implementations:

### 1. Full Agent (BlogPostAgent)
Uses LangChain's agent framework with tool-calling capabilities for autonomous operation.

### 2. Simple Chain (SimpleResearchWriter)
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
2. Choose between full agent or simple chain implementation

### Command Line Mode

Provide the topic as command-line arguments:

```bash
python main.py "Write about the latest trends in AI and machine learning"
```

### Programmatic Usage

Use in your own Python code:

```python
from agent import SimpleResearchWriter

# Create the writer
writer = SimpleResearchWriter()

# Define your topic
topic = """Write a blog post about sustainable living practices
for urban dwellers. Include practical tips and recent statistics."""

# Create and publish
result = writer.create_and_publish_post(topic)
print(result)
```

### Examples

Run the example script:

```bash
# Simple step-by-step writer (recommended)
python example.py simple

# Full agent implementation
python example.py agent

# Short topic examples
python example.py short
```

## Project Structure

```
post-creator/
├── agent.py              # Main agent implementations
├── tools.py              # Custom LangChain tools (Tavily, Ghost)
├── config.py             # Configuration and environment validation
├── main.py               # CLI entry point
├── example.py            # Usage examples
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## How It Works

### SimpleResearchWriter (Recommended)

1. **Research Phase**:
   - Takes your topic description
   - Searches the web using Tavily for current information
   - Gathers facts, statistics, and insights

2. **Writing Phase**:
   - Generates an engaging, SEO-friendly title
   - Creates well-structured HTML content (800-1500 words)
   - Includes headings, paragraphs, lists, and formatting
   - Incorporates research findings

3. **Publishing Phase**:
   - Generates relevant tags
   - Publishes to Ghost CMS
   - Returns the published post URL

### BlogPostAgent (Advanced)

Uses LangChain's agent framework to autonomously:
- Decide when to search for information
- Determine how much research is needed
- Write and structure the content
- Publish to Ghost

## Customization

### Change LLM Model

Edit `agent.py` and modify the model parameter:

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
- Use `SimpleResearchWriter` instead of `BlogPostAgent`
- Reduce the `max_iterations` in `agent.py`
- Use a smaller model like GPT-3.5-turbo

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed topic descriptions
2. **Include Context**: Mention the target audience, tone, or specific angles
3. **Use Examples**: Reference similar posts or specific points to cover
4. **Review Output**: Check the generated content before it goes live (use "draft" status)

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
- [ ] Support for featured images
- [ ] Multiple Ghost site support
- [ ] Scheduled publishing
- [ ] SEO optimization analysis
- [ ] Social media preview generation
- [ ] Draft review workflow
- [ ] Custom tone/style profiles
- [ ] Multi-language support

## Credits

Built with:
- [LangChain](https://python.langchain.com/) - Agent framework
- [Tavily](https://tavily.com/) - Web search API
- [Ghost](https://ghost.org/) - Publishing platform
- [OpenAI](https://openai.com/) / [Anthropic](https://anthropic.com/) - Language models
