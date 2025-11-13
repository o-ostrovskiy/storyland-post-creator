#!/usr/bin/env python3
"""Example usage of the blog post creator agent."""
from config import validate_config
from agent import SimpleResearchWriter, BlogPostAgent
from crew_agent import BlogPostCrew


def example_with_simple_writer():
    """Example using the simple step-by-step writer."""
    print("Example: Using SimpleResearchWriter (LangChain)\n")

    # Validate configuration
    validate_config()

    # Create the writer
    writer = SimpleResearchWriter()

    # Example topic
    topic = """Write a blog post about the latest trends in AI agents and autonomous systems.
    Focus on practical applications in business and how companies are adopting these technologies."""

    # Create and publish the post
    result = writer.create_and_publish_post(topic)

    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)


def example_with_full_agent():
    """Example using the full agent implementation."""
    print("Example: Using Full Agent (LangChain)\n")

    # Validate configuration
    validate_config()

    # Create the agent
    agent = BlogPostAgent()

    # Example topic
    topic = """Create a blog post about sustainable living practices for urban dwellers.
    Include practical tips and recent statistics about environmental impact."""

    # Create and publish the post
    result = agent.create_and_publish_post(topic)

    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)


def example_with_crewai():
    """Example using the CrewAI multi-agent implementation."""
    print("Example: Using CrewAI Multi-Agent System\n")

    # Validate configuration
    validate_config()

    # Create the crew
    crew = BlogPostCrew()

    # Example topic
    topic = """Write a blog post about hidden bookshops and literary cafes in Istanbul.
    Include recommendations for book lovers visiting the city."""

    # Create and publish the post
    result = crew.create_and_publish_post(topic)

    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)


def example_short_topics():
    """Examples with short topic descriptions."""
    print("Example: Short Topic Descriptions\n")

    validate_config()
    writer = SimpleResearchWriter()

    # Example 1: Very brief topic
    topic1 = "The future of remote work post-pandemic"
    print(f"\nTopic 1: {topic1}")
    result1 = writer.create_and_publish_post(topic1)
    print(f"Result: {result1}\n")

    # Example 2: Another brief topic
    topic2 = "Benefits of meditation for busy professionals"
    print(f"\nTopic 2: {topic2}")
    result2 = writer.create_and_publish_post(topic2)
    print(f"Result: {result2}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_type = sys.argv[1]
    else:
        print("Available examples:")
        print("1. crewai   - CrewAI Multi-Agent System (recommended)")
        print("2. simple   - SimpleResearchWriter (LangChain)")
        print("3. agent    - Full Agent (LangChain)")
        print("4. short    - Short topic descriptions")
        print()
        example_type = input("Choose example (1-4, default: 1): ").strip() or "1"

    try:
        if example_type in ["1", "crewai"]:
            example_with_crewai()
        elif example_type in ["2", "simple"]:
            example_with_simple_writer()
        elif example_type in ["3", "agent"]:
            example_with_full_agent()
        elif example_type in ["4", "short"]:
            example_short_topics()
        else:
            print(f"Unknown example type: {example_type}")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
