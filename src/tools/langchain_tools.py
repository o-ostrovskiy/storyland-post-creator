"""Custom tools for the blog post creation agent."""
import json
import jwt
import requests
from datetime import datetime as date
from typing import Optional, Type
from langchain_core.tools import BaseTool
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from src.utils.config import TAVILY_API_KEY, GHOST_URL, GHOST_ADMIN_API_KEY


class TavilySearchTool:
    """Wrapper for Tavily search tool."""

    @staticmethod
    def create():
        """Create and return a Tavily search tool."""
        return TavilySearch(
            api_key=TAVILY_API_KEY,
            max_results=5,
        )


class GhostPublishInput(BaseModel):
    """Input schema for Ghost publishing tool."""

    title: str = Field(description="The title of the blog post")
    content: str = Field(description="The HTML or Markdown content of the blog post")
    tags: Optional[str] = Field(
        default="", description="Comma-separated tags for the post"
    )
    featured: bool = Field(default=False, description="Whether the post should be featured")


class GhostPublishTool(BaseTool):
    """Tool for publishing blog posts to Ghost CMS."""

    name: str = "publish_to_ghost"
    description: str = """Use this tool to publish a blog post to Ghost CMS.
    Input should include:
    - title: The blog post title
    - content: The full blog post content in HTML or Markdown format
    - tags: Optional comma-separated tags (e.g., 'technology,AI,blogging')
    - featured: Whether to mark the post as featured (true/false)

    Returns confirmation of publication with the post URL."""
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

            token = jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)

            # Prepare the post data
            tag_list = [{"name": tag.strip()} for tag in tags.split(",") if tag.strip()]

            # Ghost Admin API - use 'html' field with ?source=html parameter
            # The 'html' field alone is read-only, but with source=html, Ghost converts it to lexical
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

            # Make the API request with ?source=html to tell Ghost to convert HTML to lexical
            url = f"{GHOST_URL.rstrip('/')}/ghost/api/admin/posts/?source=html"
            headers = {"Authorization": f"Ghost {token}", "Content-Type": "application/json"}

            print(f"DEBUG: Sending {len(content)} characters of content to Ghost...")
            print(f"DEBUG: Content preview: {content[:200]}...")

            response = requests.post(url, headers=headers, json=post_data)
            response.raise_for_status()

            result = response.json()
            post_url = result["posts"][0]["url"]

            print(f"DEBUG: Ghost response - Post created with ID: {result['posts'][0].get('id')}")

            return f"Successfully published blog post!\nTitle: {title}\nURL: {post_url}"

        except Exception as e:
            return f"Error publishing to Ghost: {str(e)}"

    async def _arun(self, *args, **kwargs):
        """Async implementation."""
        raise NotImplementedError("Async not supported for this tool")


def get_all_tools():
    """Return all available tools for the agent."""
    return [
        TavilySearchTool.create(),
        GhostPublishTool(),
    ]
