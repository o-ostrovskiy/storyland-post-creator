"""Multi-agent system for creating and publishing blog posts."""
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from src.tools.langchain_tools import get_all_tools, TavilySearchTool
from src.utils.config import LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY


class BlogPostAgent:
    """Main agent for creating and publishing blog posts."""

    def __init__(self, llm_provider: str = None):
        """Initialize the blog post agent."""
        self.llm_provider = llm_provider or LLM_PROVIDER

        # Initialize the LLM based on provider
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
        self.tools = get_all_tools()

        # Create the agent
        self.agent = self._create_agent()

    def _create_agent(self):
        """Create the LangChain agent with tools."""
        # Define the prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert blog post creator and publisher. Your job is to:
1. Research the given topic thoroughly using web search
2. Create an engaging, well-structured blog post with:
   - A compelling title
   - Well-researched content with facts and insights
   - Proper formatting (headings, paragraphs, lists)
   - SEO-friendly structure
3. Publish the post to Ghost CMS

When researching:
- Use the tavily_search_results_json tool to gather current information
- Look for recent trends, statistics, and expert opinions
- Gather enough context to write an informative post

When writing:
- Create engaging, original content
- Use HTML formatting for structure (h2, h3, p, ul, ol, strong, em tags)
- Write in a clear, accessible style
- Include specific examples and data from your research

When publishing:
- Create appropriate tags based on the content (2-5 tags)
- Use the publish_to_ghost tool with properly formatted HTML content

Always complete all steps: research, write, and publish.""",
                ),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create the agent based on LLM provider
        if self.llm_provider == "openai":
            agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        else:  # anthropic
            agent = create_tool_calling_agent(self.llm, self.tools, prompt)

        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True,
        )

        return agent_executor

    def create_and_publish_post(self, topic_description: str) -> str:
        """
        Research, create, and publish a blog post based on the topic description.

        Args:
            topic_description: A few sentences describing what the blog post should be about

        Returns:
            A message with the result of the operation
        """
        prompt = f"""Create and publish a blog post based on this description:

{topic_description}

Steps to follow:
1. First, use the search tool to research this topic and gather current, relevant information
2. Based on your research, write a comprehensive blog post (800-1500 words) with:
   - An engaging title
   - Well-structured HTML content with proper headings and formatting
   - Evidence-based insights from your research
3. Publish the post to Ghost CMS with appropriate tags

Begin now!"""

        try:
            result = self.agent.invoke({"input": prompt})
            return result["output"]
        except Exception as e:
            return f"Error creating blog post: {str(e)}"


class SimpleResearchWriter:
    """Simpler implementation using chain-of-thought without full agent framework."""

    def __init__(self, llm_provider: str = None):
        """Initialize the research writer."""
        self.llm_provider = llm_provider or LLM_PROVIDER

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

        # Initialize tools
        self.search_tool = TavilySearchTool.create()
        from tools import GhostPublishTool
        self.publish_tool = GhostPublishTool()

    def create_and_publish_post(self, topic_description: str) -> str:
        """Create and publish a blog post using a step-by-step approach."""
        try:
            # Step 1: Research
            print("\n🔍 Step 1: Researching the topic...")
            research_prompt = f"Generate 2-3 specific search queries to research this topic: {topic_description}"
            research_response = self.llm.invoke([HumanMessage(content=research_prompt)])

            # Perform searches
            search_results = self.search_tool.invoke({"query": topic_description})
            print(f"✓ Found research material\n")

            # Step 2: Generate title
            print("📝 Step 2: Creating blog post title...")
            title_prompt = f"""Based on this topic: {topic_description}

And this research: {search_results}

Create a compelling, SEO-friendly blog post title. Respond with ONLY the title, nothing else."""

            title_response = self.llm.invoke([HumanMessage(content=title_prompt)])
            title = title_response.content.strip().strip('"').strip("'")
            print(f"✓ Title: {title}\n")

            # Step 3: Generate content
            print("✍️  Step 3: Writing blog post content...")
            content_prompt = f"""Write a comprehensive blog post (800-1500 words) about: {topic_description}

Title: {title}

Research materials: {search_results}

Requirements:
- Write the COMPLETE blog post body content (do NOT include the title as an H1 tag - the title is separate)
- Start with an engaging introductory paragraph (<p> tags)
- Use H2 tags for main section headings
- Use H3 tags for subsections
- Include multiple paragraphs with substantive content
- Include specific facts, statistics, or insights from the research
- Use lists (ul/ol) where appropriate
- Write in a clear, accessible style
- Conclude with a summary or call-to-action
- The blog post should be 800-1500 words minimum

Format: Return ONLY the HTML content body (starting with <p> or <h2>). Do not include any markdown, explanations, or the title. Just the raw HTML content.

Example structure:
<p>Introduction paragraph...</p>
<h2>First Main Section</h2>
<p>Content...</p>
<h3>Subsection</h3>
<p>More content...</p>
<ul>
<li>Point 1</li>
<li>Point 2</li>
</ul>
<h2>Second Main Section</h2>
<p>Content...</p>
<p>Conclusion...</p>"""

            content_response = self.llm.invoke([HumanMessage(content=content_prompt)])
            content = content_response.content.strip()

            # Clean up any markdown code blocks if present
            if content.startswith('```html'):
                content = content.replace('```html', '', 1)
            if content.startswith('```'):
                content = content.replace('```', '', 1)
            if content.endswith('```'):
                content = content.rsplit('```', 1)[0]
            content = content.strip()

            # Validate content is substantial
            if len(content) < 500:
                raise ValueError(f"Generated content is too short ({len(content)} characters). Expected at least 500 characters.")

            # Check that it's not just a single header
            if content.count('<p>') < 3:
                raise ValueError("Generated content appears incomplete - not enough paragraph tags. Expected at least 3 paragraphs.")

            print(f"✓ Content created ({len(content)} characters, {content.count('<p>')} paragraphs)\n")

            # Step 4: Generate tags
            print("🏷️  Step 4: Generating tags...")
            tags_prompt = f"""Based on this blog post title: {title}

And topic: {topic_description}

Generate 3-5 relevant tags for this blog post. Respond with ONLY comma-separated tags, nothing else.
Example: technology, AI, machine learning"""

            tags_response = self.llm.invoke([HumanMessage(content=tags_prompt)])
            tags = tags_response.content.strip()
            print(f"✓ Tags: {tags}\n")

            # Step 5: Publish to Ghost
            print("🚀 Step 5: Publishing to Ghost CMS...")
            result = self.publish_tool._run(
                title=title,
                content=content,
                tags=tags,
                featured=False,
            )
            print(f"✓ {result}\n")

            return result

        except Exception as e:
            return f"Error creating blog post: {str(e)}"
