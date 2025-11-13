#!/usr/bin/env python3
"""Main entry point for the blog post creator agent."""
import sys
from config import validate_config
from agent import BlogPostAgent, SimpleResearchWriter
from crew_agent import BlogPostCrew


def main():
    """Main function to run the blog post creator."""
    print("=" * 60)
    print("Blog Post Creator Agent")
    print("=" * 60)
    print()

    # Validate configuration
    try:
        validate_config()
        print("✓ Configuration validated\n")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        print("See .env.example for reference.")
        sys.exit(1)

    # Get topic from command line or prompt user
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        print("What should the blog post be about?")
        print("Enter a few sentences describing the topic:")
        print()
        topic = input("> ").strip()

        if not topic:
            print("❌ No topic provided. Exiting.")
            sys.exit(1)

    print()
    print("=" * 60)
    print(f"Topic: {topic}")
    print("=" * 60)
    print()

    # Choose implementation
    print("Choose implementation:")
    print("1. Full Agent (LangChain - more autonomous)")
    print("2. Simple Chain (LangChain - step-by-step)")
    print("3. CrewAI Multi-Agent (Recommended - structured workflow)")
    print()
    choice = input("Enter choice (1, 2, or 3, default: 3): ").strip() or "3"

    print()
    print("=" * 60)
    print("Starting blog post creation process...")
    print("=" * 60)
    print()

    try:
        if choice == "1":
            # Use the full LangChain agent implementation
            agent = BlogPostAgent()
            result = agent.create_and_publish_post(topic)
        elif choice == "2":
            # Use the simpler LangChain step-by-step implementation
            writer = SimpleResearchWriter()
            result = writer.create_and_publish_post(topic)
        else:
            # Use the CrewAI multi-agent implementation
            crew = BlogPostCrew()
            result = crew.create_and_publish_post(topic)

        print()
        print("=" * 60)
        print("Result:")
        print("=" * 60)
        print(result)
        print()

    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
