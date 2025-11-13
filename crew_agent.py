"""CrewAI-based multi-agent system for blog post creation."""
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from crew_tools import TavilySearchTool, GhostPublishTool
from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    ENABLE_OBSERVABILITY,
    LANGSMITH_API_KEY,
    LANGSMITH_PROJECT,
    ENABLE_LANGSMITH,
    EXPORT_METRICS,
    ENABLE_EVALUATION,
    EXPORT_EVALUATION,
    MIN_QUALITY_SCORE
)
from observability import CrewObserver
from evaluation import ContentEvaluator, AgentEvaluator, EvaluationReporter


class BlogPostCrew:
    """Multi-agent crew for creating and publishing blog posts."""

    def __init__(self, llm_provider: str = None, enable_observability: bool = None, enable_evaluation: bool = None):
        """Initialize the blog post crew."""
        self.llm_provider = llm_provider or LLM_PROVIDER
        self.enable_observability = enable_observability if enable_observability is not None else ENABLE_OBSERVABILITY
        self.enable_evaluation = enable_evaluation if enable_evaluation is not None else ENABLE_EVALUATION

        # Initialize observability
        self.observer = CrewObserver(enable_langsmith=ENABLE_LANGSMITH) if self.enable_observability else None

        # Initialize evaluation
        self.content_evaluator = ContentEvaluator() if self.enable_evaluation else None
        self.agent_evaluator = AgentEvaluator() if self.enable_evaluation else None

        # Setup LangSmith if enabled
        if ENABLE_LANGSMITH and LANGSMITH_API_KEY:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
            os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
            if self.observer:
                print(f"✓ LangSmith tracing enabled - Project: {LANGSMITH_PROJECT}")

        # Initialize the LLM
        if self.llm_provider == "openai":
            self.llm = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.7,
                api_key=OPENAI_API_KEY,
            )
        elif self.llm_provider == "anthropic":
            self.llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0.7,
                api_key=ANTHROPIC_API_KEY,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

        # Initialize tools
        self.search_tool = TavilySearchTool()
        self.publish_tool = GhostPublishTool()

        # Create agents
        self.researcher = self._create_researcher()
        self.writer = self._create_writer()
        self.publisher = self._create_publisher()

    def _create_researcher(self) -> Agent:
        """Create the research agent."""
        return Agent(
            role="Content Researcher",
            goal="Find comprehensive, accurate, and current information on the given topic",
            backstory=(
                "You are an expert researcher with years of experience in finding "
                "reliable sources and extracting key insights. You excel at gathering "
                "facts, statistics, trends, and expert opinions from the web. "
                "You always verify information from multiple sources and provide "
                "well-organized research summaries."
            ),
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def _create_writer(self) -> Agent:
        """Create the writing agent."""
        return Agent(
            role="Blog Content Writer",
            goal="Create engaging, well-structured, and informative blog posts",
            backstory=(
                "You are a professional blog writer with expertise in creating "
                "compelling content that engages readers. You excel at taking research "
                "and transforming it into clear, accessible, and entertaining articles. "
                "You understand SEO best practices and know how to structure content "
                "with proper headings, paragraphs, and formatting. You write in HTML "
                "format with proper tags (h2, h3, p, ul, ol, strong, em)."
            ),
            tools=[],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def _create_publisher(self) -> Agent:
        """Create the publishing agent."""
        return Agent(
            role="Content Publisher",
            goal="Publish blog posts to Ghost CMS with proper formatting and metadata",
            backstory=(
                "You are a publishing specialist who ensures content is properly "
                "formatted and published with appropriate metadata. You create relevant "
                "tags, ensure all technical requirements are met, and publish content "
                "to the CMS successfully."
            ),
            tools=[self.publish_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def create_tasks(self, topic_description: str) -> list[Task]:
        """Create the tasks for the crew."""

        # Task 1: Research
        research_task = Task(
            description=(
                f"Research the following topic thoroughly:\n\n{topic_description}\n\n"
                "Your research should include:\n"
                "- Current trends and developments\n"
                "- Key facts and statistics\n"
                "- Expert opinions and insights\n"
                "- Relevant examples and case studies\n"
                "- Any recent news or updates\n\n"
                "Provide a comprehensive research summary with all key findings."
            ),
            expected_output=(
                "A detailed research summary containing facts, statistics, trends, "
                "and insights about the topic, organized in a clear structure."
            ),
            agent=self.researcher,
        )

        # Task 2: Generate Title
        title_task = Task(
            description=(
                f"Based on the research findings and the topic: {topic_description}\n\n"
                "Create a compelling, SEO-friendly blog post title.\n"
                "The title should be:\n"
                "- Engaging and attention-grabbing\n"
                "- Clear about the content\n"
                "- 50-70 characters long\n"
                "- Include relevant keywords\n\n"
                "Output ONLY the title text, nothing else."
            ),
            expected_output="A single compelling blog post title (just the title text).",
            agent=self.writer,
            context=[research_task],
        )

        # Task 3: Write Content
        content_task = Task(
            description=(
                f"Write a comprehensive blog post about: {topic_description}\n\n"
                "Use the research findings to create informative content.\n\n"
                "Requirements:\n"
                "- Write 800-1500 words\n"
                "- Use proper HTML formatting (h2, h3, p, ul, ol, strong, em tags)\n"
                "- Start with an engaging introduction paragraph (NO title H1 tag)\n"
                "- Use H2 tags for main sections\n"
                "- Use H3 tags for subsections\n"
                "- Include specific facts and statistics from the research\n"
                "- Write in a clear, accessible style\n"
                "- End with a conclusion or call-to-action\n\n"
                "Output ONLY the HTML content body. Do NOT include:\n"
                "- The title as an H1 tag\n"
                "- Code block markers (```)\n"
                "- Explanations or meta-text\n"
                "Just return clean HTML starting with <p> or <h2>."
            ),
            expected_output=(
                "Clean HTML content (800-1500 words) with proper structure: "
                "introduction paragraphs, multiple H2/H3 sections, lists where appropriate, "
                "and a conclusion. Just the HTML tags, no markdown or code blocks."
            ),
            agent=self.writer,
            context=[research_task],
        )

        # Task 4: Generate Tags
        tags_task = Task(
            description=(
                "Based on the blog post title and content, generate 3-5 relevant tags.\n"
                "Tags should be:\n"
                "- Relevant to the content\n"
                "- Single words or short phrases\n"
                "- Useful for categorization\n\n"
                "Output ONLY comma-separated tags, nothing else.\n"
                "Example format: technology, AI, machine learning, innovation"
            ),
            expected_output="Comma-separated tags (e.g., 'tag1, tag2, tag3')",
            agent=self.writer,
            context=[title_task, content_task],
        )

        # Task 5: Publish
        publish_task = Task(
            description=(
                "Publish the blog post to Ghost CMS.\n\n"
                "Use the publish_to_ghost tool with:\n"
                "- title: from the title task\n"
                "- content: from the content task (the HTML)\n"
                "- tags: from the tags task\n"
                "- featured: false\n\n"
                "Return the confirmation message with the post URL."
            ),
            expected_output=(
                "Confirmation message with the published post URL from Ghost CMS."
            ),
            agent=self.publisher,
            context=[title_task, content_task, tags_task],
        )

        return [research_task, title_task, content_task, tags_task, publish_task]

    def create_and_publish_post(self, topic_description: str) -> str:
        """
        Create and publish a blog post using the crew.

        Args:
            topic_description: Description of what the blog post should be about

        Returns:
            Result message with post URL
        """
        print("\n" + "=" * 60)
        print("Starting CrewAI Blog Post Creation Process")
        print("=" * 60 + "\n")

        # Track overall execution
        if self.observer:
            self.observer.log_event("crew_start", {"topic": topic_description})

        # Create tasks
        tasks = self.create_tasks(topic_description)

        # Track task creation
        if self.observer:
            for i, task in enumerate(tasks):
                agent_name = task.agent.role if hasattr(task.agent, 'role') else "Unknown"
                task_id = f"task_{i+1}"
                self.observer.start_task(
                    task_id=task_id,
                    task_description=task.description[:100],
                    agent_name=agent_name
                )

        # Create the crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.publisher],
            tasks=tasks,
            process=Process.sequential,  # Tasks run one after another
            verbose=True,
        )

        # Execute the crew
        try:
            result = crew.kickoff()

            # Extract task outputs for evaluation
            title = str(tasks[1].output) if len(tasks) > 1 and tasks[1].output else ""
            content = str(tasks[2].output) if len(tasks) > 2 and tasks[2].output else ""
            tags = str(tasks[3].output) if len(tasks) > 3 and tasks[3].output else ""

            # Mark tasks as completed
            if self.observer:
                for i in range(len(tasks)):
                    output = str(tasks[i].output) if tasks[i].output else str(result)
                    self.observer.end_task(f"task_{i+1}", status="completed", output=output)

                self.observer.log_event("crew_end", {"status": "success"})

            # Perform evaluation
            content_eval = None
            agent_eval = None

            if self.enable_evaluation and title and content and tags:
                print(f"\n{'='*60}")
                print("Running Quality Evaluation...")
                print(f"{'='*60}\n")

                # Evaluate content quality
                content_eval = self.content_evaluator.evaluate_content(
                    title=title,
                    content=content,
                    tags=tags
                )

                # Evaluate agent performance
                if self.observer:
                    agent_eval = self.agent_evaluator.evaluate_agent_performance(
                        agent_metrics=self.observer.agent_metrics,
                        task_metrics=[task.to_dict() for task in self.observer.task_metrics],
                        total_duration=self.observer.end_time - self.observer.start_time if self.observer.end_time else 0
                    )

                # Print evaluation results
                EvaluationReporter.print_content_evaluation(content_eval)
                if agent_eval:
                    EvaluationReporter.print_agent_evaluation(agent_eval)

                # Export evaluation if enabled
                if EXPORT_EVALUATION and agent_eval:
                    EvaluationReporter.export_evaluation(
                        content_eval,
                        agent_eval,
                        f"evaluation_{int(self.observer.start_time)}.json"
                    )

                # Check if quality meets minimum threshold
                if content_eval.overall_score < MIN_QUALITY_SCORE:
                    print(f"\n⚠️  Warning: Content quality score ({content_eval.overall_score}) is below minimum threshold ({MIN_QUALITY_SCORE})")
                    print("Consider regenerating or improving the content before publishing.\n")

            # Print observability summary
            if self.observer:
                self.observer.print_summary()

                # Export metrics if enabled
                if EXPORT_METRICS:
                    self.observer.export_metrics(f"crew_metrics_{int(self.observer.start_time)}.json")

            return str(result)
        except Exception as e:
            if self.observer:
                self.observer.track_error("Crew", str(e))
                self.observer.log_event("crew_end", {"status": "error", "error": str(e)})
                self.observer.print_summary()

            return f"Error creating blog post: {str(e)}"


# Convenience function for backwards compatibility
def create_blog_post_crew(llm_provider: str = None) -> BlogPostCrew:
    """Create and return a BlogPostCrew instance."""
    return BlogPostCrew(llm_provider=llm_provider)
