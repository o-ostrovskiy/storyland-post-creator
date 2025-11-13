# Agent Observability

Comprehensive observability and monitoring for your CrewAI blog post creator agents.

## Features

### 1. Real-Time Progress Tracking
- **Colored Console Output** - Visual feedback with color-coded messages
- **Task Progress** - See each task as it starts and completes
- **Agent Activity** - Monitor which agent is working on what
- **Tool Usage** - Track every tool call made by agents

### 2. Performance Metrics
- **Execution Time** - Total time and per-task duration
- **Agent Breakdown** - Time spent by each agent
- **Task Statistics** - Success rates, output sizes
- **Tool Analytics** - Which tools were used and how often

### 3. Token Usage & Cost Estimation
- **Token Tracking** - Approximate input/output tokens
- **Cost Estimation** - Estimated API costs in USD
- **Resource Monitoring** - Track API usage patterns

### 4. LangSmith Integration (Optional)
- **Distributed Tracing** - See full execution traces
- **LLM Call Monitoring** - Track every LLM interaction
- **Debug & Replay** - Replay failed runs for debugging
- **Performance Analytics** - Analyze bottlenecks

### 5. Metrics Export
- **JSON Export** - Export full metrics to JSON files
- **Event Timeline** - Complete timeline of all events
- **Agent Metrics** - Detailed per-agent performance data

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Observability Settings
ENABLE_OBSERVABILITY=true          # Enable/disable observability (default: true)
EXPORT_METRICS=true                # Export metrics to JSON (default: true)

# LangSmith Integration (Optional)
ENABLE_LANGSMITH=false             # Enable LangSmith tracing (default: false)
LANGSMITH_API_KEY=your_key_here    # Get from https://smith.langchain.com
LANGSMITH_PROJECT=blog-post-creator  # Project name in LangSmith
```

### Quick Setup

1. **Basic Observability** (enabled by default):
   ```bash
   # Just run normally - observability is on by default
   python main.py
   ```

2. **With LangSmith** (for advanced tracing):
   ```bash
   # Get API key from https://smith.langchain.com
   echo "ENABLE_LANGSMITH=true" >> .env
   echo "LANGSMITH_API_KEY=your_key" >> .env
   python main.py
   ```

3. **Disable Observability** (if needed):
   ```bash
   echo "ENABLE_OBSERVABILITY=false" >> .env
   python main.py
   ```

## What You'll See

### During Execution

```
============================================================
🤖 Agent Started: Content Researcher
============================================================

📋 Task Started: Research the following topic thoroughly...
   Agent: Content Researcher

🔧 Tool Used: search_web by Content Researcher

✓ Task COMPLETED: Research the following topic thoroughly...
   Duration: 12.45s
   Output: 2,450 characters
```

### After Completion

```
======================================================================
📊 AGENT OBSERVABILITY SUMMARY
======================================================================

⏱️  Total Execution Time: 45.67 seconds
📝 Total Tasks: 5
🤖 Total Agents: 3

──────────────────────────────────────────────────────────────────────
🤖 AGENT BREAKDOWN
──────────────────────────────────────────────────────────────────────

Agent: Content Researcher
  • Time: 15.23s
  • Tool Calls: 3
  • Tools Used: search_web
  • Errors: 0

Agent: Blog Content Writer
  • Time: 25.89s
  • Tool Calls: 0
  • Tools Used: None
  • Errors: 0

Agent: Content Publisher
  • Time: 4.55s
  • Tool Calls: 1
  • Tools Used: publish_to_ghost
  • Errors: 0

──────────────────────────────────────────────────────────────────────
📋 TASK BREAKDOWN
──────────────────────────────────────────────────────────────────────

Task 1: Research the following topic thoroughly...
  • Agent: Content Researcher
  • Status: completed
  • Duration: 15.23s
  • Output Length: 2,450 characters

Task 2: Based on the research findings...
  • Agent: Blog Content Writer
  • Status: completed
  • Duration: 3.45s
  • Output Length: 67 characters

Task 3: Write a comprehensive blog post...
  • Agent: Blog Content Writer
  • Status: completed
  • Duration: 22.44s
  • Output Length: 5,234 characters

Task 4: Based on the blog post title...
  • Agent: Blog Content Writer
  • Status: completed
  • Duration: 2.11s
  • Output Length: 48 characters

Task 5: Publish the blog post to Ghost CMS...
  • Agent: Content Publisher
  • Status: completed
  • Duration: 4.55s
  • Output Length: 156 characters

──────────────────────────────────────────────────────────────────────
💰 TOKEN USAGE & COST ESTIMATES
──────────────────────────────────────────────────────────────────────

  • Input Tokens (est.): 3,245
  • Output Tokens (est.): 2,167
  • Total Tokens (est.): 5,412
  • Estimated Cost: $0.2274 USD
    - Input Cost: $0.0974
    - Output Cost: $0.1300

======================================================================
```

### Exported Metrics (JSON)

Metrics are automatically exported to `crew_metrics_[timestamp].json`:

```json
{
  "execution_summary": {
    "start_time": "2025-01-12T14:30:22.123456",
    "end_time": "2025-01-12T14:31:07.789012",
    "total_duration": 45.67
  },
  "agents": {
    "Content Researcher": {
      "agent_name": "Content Researcher",
      "task_count": 1,
      "tool_calls": 3,
      "total_time": 15.23,
      "tools_used": ["search_web"],
      "errors": []
    }
  },
  "tasks": [...],
  "cost_estimate": {...},
  "events": [...]
}
```

## Use Cases

### 1. Performance Optimization
Monitor execution times to identify slow tasks or bottlenecks:
```bash
# Look for tasks taking >20s
grep "Duration:" crew_metrics_*.json
```

### 2. Cost Tracking
Track API costs across multiple runs:
```bash
# Sum up all costs
jq '.cost_estimate.estimated_cost_usd' crew_metrics_*.json | awk '{s+=$1} END {print s}'
```

### 3. Debugging
When something goes wrong, check the event timeline:
```json
{
  "events": [
    {
      "timestamp": "2025-01-12T14:30:25.456",
      "event_type": "tool_use",
      "data": {...}
    },
    {
      "timestamp": "2025-01-12T14:30:30.789",
      "event_type": "error",
      "data": {"error": "Connection timeout"}
    }
  ]
}
```

### 4. Quality Assurance
Track output quality metrics:
- Content length (should be 800-1500 words)
- Task success rates
- Tool reliability

## LangSmith Advanced Features

When `ENABLE_LANGSMITH=true`, you get:

1. **Visual Traces** - See execution flow in the LangSmith dashboard
2. **LLM Call Details** - Inspect every prompt and response
3. **Performance Comparison** - Compare runs side-by-side
4. **Debugging Tools** - Step through failed executions
5. **Team Collaboration** - Share traces with your team

### LangSmith Dashboard

Access at: https://smith.langchain.com

Features:
- View all your crew runs
- Filter by status, duration, cost
- Search through traces
- Create performance dashboards
- Set up alerts for failures

## Tips & Best Practices

### 1. Monitor Costs
```bash
# Set alerts when costs exceed threshold
if [ $(jq '.cost_estimate.estimated_cost_usd' metrics.json) > 1.0 ]; then
  echo "Warning: High API costs!"
fi
```

### 2. Track Trends
Keep historical metrics to identify patterns:
```bash
# Archive metrics by date
mkdir -p metrics/$(date +%Y-%m-%d)
mv crew_metrics_*.json metrics/$(date +%Y-%m-%d)/
```

### 3. Debug Production Issues
When users report issues:
1. Check the exported metrics JSON
2. Look at the event timeline
3. Review error messages
4. Check LangSmith traces if enabled

### 4. Optimize Performance
Use metrics to:
- Identify slow agents
- Reduce unnecessary tool calls
- Optimize prompts for faster responses
- Balance quality vs. speed

## Troubleshooting

### No Metrics Displayed
```bash
# Check if observability is enabled
grep ENABLE_OBSERVABILITY .env
# Should show: ENABLE_OBSERVABILITY=true
```

### LangSmith Not Working
```bash
# Verify API key
python -c "from config import LANGSMITH_API_KEY; print(bool(LANGSMITH_API_KEY))"
# Should print: True

# Check environment
echo $LANGCHAIN_TRACING_V2
# Should show: true
```

### Metrics File Not Created
```bash
# Check export setting
grep EXPORT_METRICS .env
# Should show: EXPORT_METRICS=true

# Check file permissions
ls -la crew_metrics_*.json
```

## API

### Programmatic Access

```python
from observability import CrewObserver
from crew_agent import BlogPostCrew

# Create crew with observability
crew = BlogPostCrew(enable_observability=True)

# Access observer directly
observer = crew.observer

# Track custom events
if observer:
    observer.log_event("custom_event", {"key": "value"})
    observer.track_tool_use("MyAgent", "my_tool")

# Get metrics
cost_info = observer.estimate_cost()
print(f"Estimated cost: ${cost_info['estimated_cost_usd']}")

# Export metrics
observer.export_metrics("my_metrics.json")
```

## Future Enhancements

Planned features:
- [ ] Real-time dashboard web UI
- [ ] Prometheus/Grafana integration
- [ ] Slack/Discord notifications
- [ ] Automated performance reports
- [ ] A/B testing framework
- [ ] Custom metric plugins

## Support

For issues or questions:
1. Check the exported metrics JSON
2. Review the event timeline
3. Check LangSmith traces (if enabled)
4. Open an issue with metrics attached
