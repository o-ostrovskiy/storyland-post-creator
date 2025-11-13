# Agent Evaluation System

Comprehensive evaluation framework for assessing blog post content quality and agent performance.

## Overview

The evaluation system provides automated quality assessment for:
- **Content Quality** - Readability, structure, SEO, and completeness
- **Agent Performance** - Efficiency, reliability, and output quality

## Features

### 1. Content Quality Evaluation

#### Metrics Assessed:

**Readability Score (0-100)**
- Flesch Reading Ease
- Flesch-Kincaid Grade Level
- Average sentence length
- Vocabulary complexity

**Structure Score (0-100)**
- Heading hierarchy (H2, H3 tags)
- Paragraph count and distribution
- List usage (ul/ol)
- HTML formatting quality
- Use of emphasis (strong/em tags)

**SEO Score (0-100)**
- Title length (50-70 characters optimal)
- Keyword density
- Tag count (3-5 optimal)
- Word count (800-1500 target)
- Meta information

**Completeness Score (0-100)**
- Introduction quality
- Conclusion presence
- Content depth per section
- No placeholder text
- Minimum viable length

### 2. Agent Performance Evaluation

#### Metrics Assessed:

**Efficiency Score (0-100)**
- Total execution time
- Tool usage patterns
- Task completion speed
- Resource utilization

**Reliability Score (0-100)**
- Error rates
- Task completion rates
- Consistency across tasks
- Failure recovery

**Quality Score (0-100)**
- Output substantiveness
- Content length appropriateness
- Task output quality

## Configuration

### Environment Variables

Add to your `.env`:

```env
# Evaluation Settings (enabled by default)
ENABLE_EVALUATION=true
EXPORT_EVALUATION=true
MIN_QUALITY_SCORE=70  # Minimum acceptable score (0-100)
```

### Adjusting Thresholds

Edit `evaluation.py` to customize:

```python
# In ContentEvaluator.__init__
self.min_word_count = 800  # Minimum words
self.max_word_count = 1500  # Maximum words
self.target_reading_ease = 60  # Flesch Reading Ease target
```

## Output

### During Execution

After content generation, you'll see:

```
============================================================
Running Quality Evaluation...
============================================================
```

### Content Quality Report

```
======================================================================
📝 CONTENT QUALITY EVALUATION
======================================================================

Overall Score: 87.50/100 (Grade: B)

Detailed Scores:
  • Readability: 85/100
  • Structure: 90/100
  • SEO: 88/100
  • Completeness: 87/100

⚠️  Issues Found (2):
  • Title too long (75 chars). May be truncated
  • Content is quite long - consider breaking into series

💡 Recommendations (3):
  • Shorten title to 50-70 characters
  • Consider adding subsections with H3 headings
  • Add emphasis to key points using bold/italic

======================================================================
```

### Agent Performance Report

```
======================================================================
🤖 AGENT PERFORMANCE EVALUATION
======================================================================

Overall Score: 92.33/100 (Grade: A)

Detailed Scores:
  • Efficiency: 90/100
  • Reliability: 95/100
  • Quality: 92/100

✓ Strengths (3):
  • Very fast execution (28.5s)
  • Zero errors during execution
  • All tasks completed successfully

✗ Areas for Improvement (1):
  • Execution time above target

======================================================================
```

### Quality Warnings

If content quality is below threshold:

```
⚠️  Warning: Content quality score (65.5) is below minimum threshold (70)
Consider regenerating or improving the content before publishing.
```

## Exported Evaluation Report

Automatically saved as `evaluation_[timestamp].json`:

```json
{
  "content_quality": {
    "readability_score": 85.0,
    "structure_score": 90.0,
    "seo_score": 88.0,
    "completeness_score": 87.0,
    "overall_score": 87.5,
    "grade": "B",
    "issues": [
      "Title too long (75 chars). May be truncated"
    ],
    "recommendations": [
      "Shorten title to 50-70 characters",
      "Add emphasis to key points"
    ]
  },
  "agent_performance": {
    "efficiency_score": 90.0,
    "reliability_score": 95.0,
    "quality_score": 92.0,
    "overall_score": 92.33,
    "grade": "A",
    "strengths": [
      "Very fast execution",
      "Zero errors"
    ],
    "weaknesses": []
  },
  "timestamp": "2025-01-12T15:30:45.123456"
}
```

## Grading System

| Grade | Score Range | Quality Level |
|-------|-------------|---------------|
| A     | 90-100      | Excellent     |
| B     | 80-89       | Good          |
| C     | 70-79       | Acceptable    |
| D     | 60-69       | Needs Work    |
| F     | 0-59        | Unacceptable  |

## Use Cases

### 1. Quality Assurance

Ensure all published content meets standards:

```bash
# Set high quality threshold
echo "MIN_QUALITY_SCORE=85" >> .env
python main.py
```

### 2. Performance Monitoring

Track agent performance over time:

```bash
# Analyze all evaluation reports
jq '.agent_performance.overall_score' evaluation_*.json
```

### 3. A/B Testing

Compare different approaches:

```bash
# Test with different prompts
python main.py "topic with detailed instructions"
python main.py "simple topic"

# Compare evaluation scores
```

### 4. Content Improvement

Identify common issues:

```bash
# Extract all recommendations
jq '.content_quality.recommendations[]' evaluation_*.json | sort | uniq -c
```

## Metrics Breakdown

### Readability Metrics

**Flesch Reading Ease** (0-100, higher = easier):
- 90-100: 5th grade
- 80-90: 6th grade
- 70-80: 7th grade
- 60-70: 8th-9th grade (target)
- 50-60: 10th-12th grade
- 30-50: College
- 0-30: Graduate level

**Flesch-Kincaid Grade**:
- Target: 8-10th grade
- Measures years of education needed

### Structure Quality

**Optimal Structure**:
- 3-8 H2 headings (main sections)
- 1-3 H3 headings per H2
- 5+ paragraphs
- 1-3 lists (ul/ol)
- Use of strong/em for emphasis

### SEO Best Practices

**Title**:
- Length: 50-70 characters
- Include primary keyword
- Engaging and descriptive

**Content**:
- Length: 800-1500 words
- Keyword density: Natural
- Proper heading structure
- Internal/external links (future)

**Tags**:
- Count: 3-5 tags
- Relevant to content
- Mix of broad and specific

## Troubleshooting

### Low Readability Scores

**Issue**: Reading ease < 50
**Solutions**:
- Shorten sentences
- Use simpler words
- Break up complex ideas
- Add examples

### Poor Structure Scores

**Issue**: Few headings/paragraphs
**Solutions**:
- Add more H2 sections
- Break long paragraphs
- Use bullet lists
- Add subheadings (H3)

### SEO Issues

**Issue**: Low SEO score
**Solutions**:
- Adjust title length
- Add more relevant tags
- Expand/reduce content length
- Include keywords naturally

### Failed Evaluations

**Issue**: Evaluation crashes
**Check**:
```bash
# Verify dependencies
pip install textstat beautifulsoup4

# Check content format
# Ensure content is valid HTML
```

## Customization

### Custom Evaluation Criteria

Edit `evaluation.py`:

```python
class ContentEvaluator:
    def evaluate_content(self, title, content, tags):
        # Add custom checks
        if "your_keyword" not in content.lower():
            issues.append("Missing required keyword")
            score -= 10

        return ContentQualityScore(...)
```

### Custom Scoring Weights

Adjust importance of different metrics:

```python
# In evaluate_content method
overall_score = (
    readability_score * 0.30 +  # More weight on readability
    structure_score * 0.20 +
    seo_score * 0.30 +  # More weight on SEO
    completeness_score * 0.20
)
```

### Additional Metrics

Add your own metrics:

```python
def _evaluate_custom(self, content, issues, recommendations) -> float:
    score = 100.0

    # Your custom logic
    if some_condition:
        issues.append("Custom issue")
        score -= 15

    return score
```

## Integration with CI/CD

### Automated Quality Gates

```bash
#!/bin/bash
# quality_gate.sh

python main.py "$1"

# Extract score
SCORE=$(jq '.content_quality.overall_score' evaluation_*.json | tail -1)

if (( $(echo "$SCORE < 70" | bc -l) )); then
    echo "Quality check failed: Score $SCORE < 70"
    exit 1
fi

echo "Quality check passed: Score $SCORE"
```

### GitHub Actions

```yaml
name: Content Quality Check

on: [push]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run evaluation
        run: |
          pip install -r requirements.txt
          python main.py "${{ github.event.head_commit.message }}"
      - name: Check score
        run: |
          SCORE=$(jq '.content_quality.overall_score' evaluation_*.json)
          if [ $SCORE -lt 70 ]; then exit 1; fi
```

## Best Practices

### 1. Set Realistic Thresholds

```env
# Start lower, increase gradually
MIN_QUALITY_SCORE=60  # Initial
# After improvements
MIN_QUALITY_SCORE=70  # Standard
# For premium content
MIN_QUALITY_SCORE=85  # High quality
```

### 2. Review Evaluation Reports

```bash
# Weekly review
cat evaluation_*.json | jq '.content_quality.issues[]' | sort | uniq -c

# Identify patterns
cat evaluation_*.json | jq '.content_quality.overall_score' | \
  awk '{sum+=$1; count++} END {print "Average:", sum/count}'
```

### 3. Iterate Based on Feedback

Use recommendations to improve:
1. Note common issues
2. Adjust prompts/instructions
3. Regenerate content
4. Compare scores

### 4. Combine with Human Review

Evaluation is a tool, not a replacement:
- Use for initial screening
- Human review for final approval
- Focus on high-impact issues
- Consider context and audience

## Future Enhancements

Planned features:
- [ ] Plagiarism detection
- [ ] Sentiment analysis
- [ ] Tone consistency
- [ ] Image/media quality
- [ ] Link quality analysis
- [ ] Competitive analysis
- [ ] Historical trend tracking
- [ ] ML-based quality prediction

## API Reference

### ContentEvaluator

```python
from evaluation import ContentEvaluator

evaluator = ContentEvaluator()
score = evaluator.evaluate_content(
    title="My Blog Title",
    content="<p>HTML content...</p>",
    tags="tag1, tag2, tag3"
)

print(f"Score: {score.overall_score}/100")
print(f"Grade: {score.grade}")
print(f"Issues: {score.issues}")
```

### AgentEvaluator

```python
from evaluation import AgentEvaluator

evaluator = AgentEvaluator()
score = evaluator.evaluate_agent_performance(
    agent_metrics=metrics_dict,
    task_metrics=task_list,
    total_duration=45.67
)

print(f"Performance: {score.overall_score}/100")
print(f"Strengths: {score.strengths}")
```

### EvaluationReporter

```python
from evaluation import EvaluationReporter

# Print reports
EvaluationReporter.print_content_evaluation(content_score)
EvaluationReporter.print_agent_evaluation(agent_score)

# Export to file
EvaluationReporter.export_evaluation(
    content_score,
    agent_score,
    "my_evaluation.json"
)
```

## Support

For evaluation issues:
1. Check the exported JSON reports
2. Review metric thresholds
3. Verify content format (valid HTML)
4. Check dependencies are installed
