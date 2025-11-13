"""CrewAI-compatible tools for blog post creation."""
from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import json
import jwt
import requests
from datetime import datetime as date
from tavily import TavilyClient
from config import TAVILY_API_KEY, GHOST_URL, GHOST_ADMIN_API_KEY


class TavilySearchInput(BaseModel):
    """Input schema for Tavily search tool."""
    query: str = Field(description="The search query to find information about")


class TavilySearchTool(BaseTool):
    """Tool for searching the web using Tavily API."""

    name: str = "search_web"
    description: str = (
        "Search the web for current information on any topic. "
        "Input should be a search query string. "
        "Returns relevant articles, facts, and information from the web."
    )
    args_schema: Type[BaseModel] = TavilySearchInput

    def _run(self, query: str) -> str:
        """Search the web using Tavily."""
        try:
            client = TavilyClient(api_key=TAVILY_API_KEY)
            results = client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
                include_answer=True,
            )

            # Format results
            output = []
            if results.get('answer'):
                output.append(f"Answer: {results['answer']}\n")

            output.append("Relevant Sources:")
            for i, result in enumerate(results.get('results', []), 1):
                output.append(f"\n{i}. {result.get('title', 'N/A')}")
                output.append(f"   {result.get('content', 'N/A')}")
                output.append(f"   URL: {result.get('url', 'N/A')}")

            return "\n".join(output)
        except Exception as e:
            return f"Error performing search: {str(e)}"


class GhostPublishInput(BaseModel):
    """Input schema for Ghost publishing tool."""

    title: str = Field(description="The title of the blog post")
    content: str = Field(description="The HTML content of the blog post")
    tags: str = Field(
        default="",
        description="Comma-separated tags for the post (e.g., 'technology,AI,blogging')"
    )
    featured: bool = Field(
        default=False,
        description="Whether the post should be featured"
    )


class GhostPublishTool(BaseTool):
    """Tool for publishing blog posts to Ghost CMS."""

    name: str = "publish_to_ghost"
    description: str = (
        "Publish a blog post to Ghost CMS. "
        "Requires: title (string), content (HTML string), "
        "tags (comma-separated string), featured (boolean). "
        "Returns confirmation with the published post URL."
    )
    args_schema: Type[BaseModel] = GhostPublishInput

    def _run(
        self,
        title: str,
        content: str,
        tags: str = "",
        featured: bool = False,
    ) -> str:
        """Publish a post to Ghost CMS."""
        try:
            # Create JWT token for Ghost Admin API
            id, secret = GHOST_ADMIN_API_KEY.split(":")
            iat = int(date.now().timestamp())

            header = {"alg": "HS256", "typ": "JWT", "kid": id}
            payload = {
                "iat": iat,
                "exp": iat + 5 * 60,
                "aud": "/admin/",
            }

            token = jwt.encode(
                payload,
                bytes.fromhex(secret),
                algorithm="HS256",
                headers=header
            )

            # Prepare the post data
            tag_list = [{"name": tag.strip()} for tag in tags.split(",") if tag.strip()]

            post_data = {
                "posts": [
                    {
                        "title": title,
                        "html": content,
                        "tags": tag_list,
                        "featured": featured,
                        "status": "published",
                    }
                ]
            }

            # Make the API request with ?source=html to convert HTML to lexical
            url = f"{GHOST_URL.rstrip('/')}/ghost/api/admin/posts/?source=html"
            headers = {
                "Authorization": f"Ghost {token}",
                "Content-Type": "application/json"
            }

            response = requests.post(url, headers=headers, json=post_data)
            response.raise_for_status()

            result = response.json()
            post_url = result["posts"][0]["url"]

            return f"✓ Successfully published!\nTitle: {title}\nURL: {post_url}"

        except Exception as e:
            return f"Error publishing to Ghost: {str(e)}"
