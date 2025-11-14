# Quick Start Guide

Get up and running with the Blog Post Creator Agent in 5 minutes!

## 1. Setup (One-time)

### Option A: Automatic Setup (Recommended)
```bash
./setup.sh
```

### Option B: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

## 2. Configure API Keys

Edit `.env` file and add your keys:

```env
LLM_PROVIDER=openai

OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
GHOST_URL=https://your-site.com
GHOST_ADMIN_API_KEY=id:secret
```

### Where to get API keys:

- **OpenAI**: https://platform.openai.com/api-keys
- **Tavily**: https://tavily.com/ (sign up for free)
- **Ghost Admin API Key**: 
  1. Log into your Ghost admin panel
  2. Go to Settings → Integrations
  3. Click "Add custom integration"
  4. Give it a name (e.g., "Blog Creator Agent")
  5. Copy the Admin API Key (format: `id:secret`)
  6. Copy your Ghost site URL (e.g., `https://your-site.com`)

## 3. Run the Agent

### Interactive Mode
```bash
python main.py
```

Then enter your topic when prompted:
```
> Write a blog post about the benefits of morning meditation for busy professionals
```

### Command Line Mode
```bash
python main.py "Your topic description here"
```

### Programmatic Mode
```python
from agent import SimpleResearchWriter

writer = SimpleResearchWriter()
result = writer.create_and_publish_post("Your topic here")
print(result)
```

## 4. Example Usage

```bash
# Run a simple example
python example.py simple

# Or just test with a quick topic
python main.py "The future of electric vehicles"
```

## What Happens

1. **Research**: Agent searches the web for current information
2. **Write**: Creates an 800-1500 word blog post with proper formatting
3. **Publish**: Automatically posts to your Ghost site
4. **Done**: You get the published URL!

## Tips

- Be specific with your topic description
- The more context you provide, the better the output
- Use "draft" status in tools.py if you want to review before publishing
- Start with SimpleResearchWriter (more predictable than full agent)

## Troubleshooting

**"Missing required environment variables"**
- Check your .env file exists and has all required keys

**"Error publishing to Ghost"**
- Verify Ghost URL includes https://
- Check Admin API key format (should be `id:secret`)

**Need help?**
- Check README.md for full documentation
- Review example.py for usage patterns
- Test your API keys individually

## Next Steps

Once it works:
- Customize prompts in agent.py for your writing style
- Adjust content length in the prompts
- Add more tools in tools.py
- Create custom topic templates

Happy blogging!
