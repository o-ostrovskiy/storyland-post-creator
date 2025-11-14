# Interactive Testing Notebooks

This folder contains Jupyter notebooks for interactive testing and development of the blog post creator agents.

## Getting Started

### 1. Activate Virtual Environment

```bash
source ../venv/bin/activate
```

### 2. Launch Jupyter

```bash
jupyter notebook
```

This will open Jupyter in your browser at `http://localhost:8888`

### 3. Open the Test Notebook

Open `test_agents.ipynb` from the Jupyter interface.

## Available Notebooks

### test_agents.ipynb

Comprehensive testing notebook with:
- **Configuration Validation**: Check your environment setup
- **Pre-configured Topics**: Ready-to-use test topics for all implementations
- **All Three Agents**: Test CrewAI, Simple Chain, and Full Agent
- **Comparison Tools**: Run the same topic through all implementations
- **Debugging Cells**: Inspect agent configuration and test individual tools
- **Quick Test Functions**: Convenient wrapper functions for rapid iteration

## Tips for Using Notebooks

1. **Run Cells Sequentially**: Execute cells in order from top to bottom initially
2. **Modify Topics**: Edit the topic variables to test different content
3. **Watch Output**: Observe agent behavior and output quality in real-time
4. **Experiment**: Try different configurations and compare results
5. **Save Results**: Notebook automatically saves your session and outputs

## Example Workflow

```python
# 1. Import and validate
from src.agents.crew_agent import BlogPostCrew
from src.utils.config import validate_config
validate_config()

# 2. Define your topic
topic = "Write about the future of AI in healthcare"

# 3. Create and run
crew = BlogPostCrew()
result = crew.create_and_publish_post(topic)

# 4. Review results
print(result)
```

## Troubleshooting

**Kernel Not Found?**
- Make sure you activated the virtual environment
- Try: `python -m ipykernel install --user --name=post-creator`

**Import Errors?**
- Verify you're in the project root directory
- Check that `sys.path.insert(0, os.path.abspath('..'))` is executed

**API Key Issues?**
- Ensure `.env` file exists in the project root
- Run `validate_config()` to check all keys are present

## Creating New Notebooks

To create a new notebook:

1. Click "New" → "Python 3" in Jupyter
2. Add the setup cell:
   ```python
   import sys, os
   sys.path.insert(0, os.path.abspath('..'))
   from src.agents.crew_agent import BlogPostCrew
   ```
3. Start experimenting!

## Keyboard Shortcuts

- **Shift + Enter**: Run cell and move to next
- **Ctrl + Enter**: Run cell and stay
- **A**: Insert cell above
- **B**: Insert cell below
- **D + D**: Delete cell
- **M**: Convert to markdown
- **Y**: Convert to code

Happy Testing! 🚀
