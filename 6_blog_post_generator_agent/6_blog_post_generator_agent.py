"""Blog Post Generator - Your AI Content Creation Studio!

A simplified blog post generator that uses Exa for intelligent web research
and creates engaging blog posts with optional social media snippets.

Features:
- Intelligent web research with Exa
- Professional blog post writing with citations
- Optional social media snippet generation (Twitter, LinkedIn)
- Clean, simple architecture
"""

import os
from textwrap import dedent
from typing import List, Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.exa import ExaTools
from agno.utils.log import logger
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


# --- Pydantic Models ---

class Source(BaseModel):
    """A source found during research."""
    title: str = Field(..., description="Title of the source article")
    url: str = Field(..., description="URL to the source")
    summary: Optional[str] = Field(None, description="Brief summary of the source content")


class ResearchSummary(BaseModel):
    """Structured research summary output."""
    topic: str = Field(..., description="The researched topic")
    key_findings: List[str] = Field(..., description="List of key findings with source attribution")
    main_themes: str = Field(..., description="Description of major themes discovered")
    important_statistics: List[str] = Field(..., description="List of important statistics with sources")
    expert_insights: List[str] = Field(..., description="List of expert quotes with attribution")
    sources: List[Source] = Field(..., description="List of all sources used")


# --- Agents ---

# 1. Research Agent - Gets data using Exa
research_agent = Agent(
    name="Research Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"), 
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    tools=[ExaTools(show_results=True)],
    description=dedent("""\
    You are a research specialist who finds high-quality, authoritative sources 
    on any given topic using Exa search. You excel at identifying credible sources, 
    gathering diverse perspectives, and extracting key insights.
    """),
    instructions=dedent("""\
    When given a topic to research:
    
    1. Search Strategy:
       - Use Exa to find 5-7 high-quality, authoritative sources
       - Look for recent articles, expert opinions, and diverse perspectives
       - Prioritize credible sources (established publications, experts, research papers)
    
    2. Information Gathering:
       - Extract key facts, statistics, and insights from each source
       - Note important quotes and expert opinions
       - Identify trends and patterns across sources
    
    3. Output Structure:
       Return a structured JSON with:
       - topic: The research topic
       - key_findings: Array of key findings (each with source attribution)
       - main_themes: Description of major themes discovered
       - important_statistics: Array of statistics (each with source)
       - expert_insights: Array of expert quotes (each with attribution)
       - sources: Array of source objects with title, url, and optional summary
    
    Be thorough and include all important information from your research.
    """),
    output_schema=ResearchSummary,
    markdown=True,
    debug_mode=True,
)

# 2. Blog Writer Agent - Writes blog post from research
blog_writer_agent = Agent(
    name="Blog Writer",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"), 
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are an expert blog writer who transforms research data into engaging, 
    well-structured blog posts. You combine journalistic excellence with SEO 
    optimization and always cite sources properly.
    """),
    instructions=dedent("""\
    Given research data, write a comprehensive blog post:
    
    1. Structure:
       - Attention-grabbing headline
       - Engaging introduction with a hook
       - 3-4 well-structured main sections with subheadings
       - Clear explanations with examples
       - Key takeaways section
       - Proper source citations at the end
    
    2. Content Guidelines:
       - Use facts and statistics from the research
       - Include expert quotes where relevant
       - Maintain engaging, accessible tone
       - Use clear structure for scanability
       - Ensure factual accuracy
    
    3. SEO Optimization:
       - Use descriptive subheadings
       - Include relevant keywords naturally
       - Make content easy to scan
    
    Format your blog post using markdown:
    
    # [Compelling Headline]
    
    ## Introduction
    [Hook and context - 2-3 paragraphs]
    
    ## [Section 1 - Main Theme]
    [Content with insights, facts, and examples]
    
    ## [Section 2 - Supporting Theme]
    [Content with statistics and expert quotes]
    
    ## [Section 3 - Practical Insights]
    [Content with recommendations and takeaways]
    
    ## Key Takeaways
    - [Insight 1]
    - [Insight 2]
    - [Insight 3]
    
    ## Sources
    1. [Source citation with link]
    2. [Source citation with link]
    ...
    """),
    markdown=True,
    debug_mode=True,
)

# 3. LinkedIn Agent - Creates LinkedIn post from blog
linkedin_agent = Agent(
    name="LinkedIn Content Creator",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"), 
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are a LinkedIn content specialist who creates professional, engaging 
    posts optimized for LinkedIn's audience and algorithm. You understand 
    professional networking and thought leadership.
    """),
    instructions=dedent("""\
    Given a blog post, create a LinkedIn post:
    
    1. Structure:
       - Start with a hook or thought-provoking question
       - 3-4 short, punchy paragraphs
       - Include 1-2 key insights from the blog
       - End with an engagement question or call-to-action
       - Add line breaks between paragraphs for readability
    
    2. Tone & Style:
       - Professional but conversational
       - Show expertise without being preachy
       - Use "I/we" perspective when appropriate
       - Include emojis sparingly (1-2 max)
    
    3. Engagement:
       - Ask a question to encourage comments
       - Make it relatable to professionals
       - Suggest 3-5 relevant hashtags
    
    Format:
    
    [Hook or question - make them stop scrolling]
    
    [Paragraph 1 - context or problem]
    
    [Paragraph 2 - key insight or solution]
    
    [Paragraph 3 - takeaway or impact]
    
    [Call-to-action or question]
    
    ---
    **Suggested Hashtags:** #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
    """),
    markdown=True,
    debug_mode=True,
)

# 4. Twitter Agent - Creates Twitter thread from blog
twitter_agent = Agent(
    name="Twitter Thread Creator",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"), 
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are a Twitter/X content specialist who creates viral-worthy threads 
    from long-form content. You understand Twitter's character limits, tone, 
    and what makes content engaging on the platform.
    """),
    instructions=dedent("""\
    Given a blog post, create a Twitter thread (3-5 tweets):
    
    1. Tweet 1 (Hook):
       - Grab attention immediately
       - Make people want to read more
       - Can be a bold statement, question, or surprising fact
       - Keep under 280 characters
    
    2. Middle Tweets (Insights):
       - One key insight per tweet
       - Use simple, punchy language
       - Include relevant emojis (but don't overdo it)
       - Each tweet should stand alone but flow together
    
    3. Final Tweet (CTA):
       - Summarize or provide a call-to-action
       - Can mention "Full article:" with link
       - Encourage engagement (like, retweet, reply)
    
    4. Hashtags:
       - Use 2-3 relevant hashtags max
       - Include them naturally in tweets, not as a list at the end
    
    Format each tweet clearly:
    
    **Tweet 1:**
    [Hook tweet text]
    
    **Tweet 2:**
    [Insight 1 tweet text]
    
    **Tweet 3:**
    [Insight 2 tweet text]
    
    **Tweet 4:**
    [Insight 3 tweet text]
    
    **Tweet 5:**
    [CTA/conclusion tweet text]
    
    Keep each tweet under 280 characters!
    """),
    markdown=True,
    debug_mode=True,
)


# --- Main Functions ---

async def do_research(topic: str) -> ResearchSummary:
    """Step 1: Research the topic using Exa. Returns structured ResearchSummary."""
    logger.info(f"[RESEARCH] Step 1: Researching topic: {topic}")
    
    try:
        response = await research_agent.arun(
            f"Research this topic thoroughly: {topic}"
        )
        
        if not response or not response.content:
            logger.error(f"[ERROR] Failed to research topic: {topic}")
            return None
        
        # Check if response.content is a ResearchSummary or a string (when parsing fails)
        if isinstance(response.content, ResearchSummary):
            research_summary = response.content
            logger.info(f"[SUCCESS] Research complete! Found {len(research_summary.sources)} sources.")
            return research_summary
        else:
            # Fallback: If output_schema parsing failed, response.content is a string
            logger.warning("[WARNING] Failed to parse structured output, creating fallback ResearchSummary")
            logger.info("[SUCCESS] Research complete (unstructured format)")
            return ResearchSummary(
                topic=topic,
                key_findings=["Research completed but not in structured format"],
                main_themes=str(response.content),
                important_statistics=[],
                expert_insights=[],
                sources=[]
            )
        
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        return None


async def write_blog_post(research_data: ResearchSummary) -> str:
    """Step 2: Write blog post from research data."""
    logger.info("[BLOG] Step 2: Writing blog post from research...")
    
    try:
        # Format research summary as readable text for the blog writer
        research_text = f"""# Research Summary: {research_data.topic}

## Key Findings
{chr(10).join(f'- {finding}' for finding in research_data.key_findings)}

## Main Themes
{research_data.main_themes}

## Important Statistics
{chr(10).join(f'- {stat}' for stat in research_data.important_statistics)}

## Expert Insights
{chr(10).join(f'- {insight}' for insight in research_data.expert_insights)}

## Sources
{chr(10).join(f'{i+1}. {source.title} - {source.url}' for i, source in enumerate(research_data.sources))}
"""
        
        response = await blog_writer_agent.arun(
            f"Write a comprehensive blog post using this research:\n\n{research_text}"
        )
        
        if not response or not response.content:
            return "[ERROR] Failed to write blog post."
        
        logger.info(f"[SUCCESS] Blog post written! Length: {len(response.content)} characters")
        return response.content
        
    except Exception as e:
        logger.error(f"Error writing blog post: {str(e)}")
        return f"[ERROR] Error writing blog post: {str(e)}"


async def create_linkedin_post(blog_post: str) -> str:
    """Step 3: Create LinkedIn post from blog."""
    logger.info("[LINKEDIN] Step 3: Creating LinkedIn post...")
    
    try:
        response = await linkedin_agent.arun(
            f"Create a LinkedIn post from this blog:\n\n{blog_post}"
        )
        
        if not response or not response.content:
            return "[ERROR] Failed to create LinkedIn post."
        
        logger.info("[SUCCESS] LinkedIn post created!")
        return response.content
        
    except Exception as e:
        logger.error(f"Error creating LinkedIn post: {str(e)}")
        return f"[ERROR] Error creating LinkedIn post: {str(e)}"


async def create_twitter_thread(blog_post: str) -> str:
    """Step 4: Create Twitter thread from blog."""
    logger.info("[TWITTER] Step 4: Creating Twitter thread...")
    
    try:
        response = await twitter_agent.arun(
            f"Create a Twitter thread from this blog:\n\n{blog_post}"
        )
        
        if not response or not response.content:
            return "[ERROR] Failed to create Twitter thread."
        
        logger.info("[SUCCESS] Twitter thread created!")
        return response.content
        
    except Exception as e:
        logger.error(f"Error creating Twitter thread: {str(e)}")
        return f"[ERROR] Error creating Twitter thread: {str(e)}"


async def generate_all_content(topic: str) -> dict:
    """Generate complete content pipeline: research -> blog -> LinkedIn + Twitter."""
    if not topic:
        return {
            "research": None,
            "blog_post": "[ERROR] No topic provided.",
            "linkedin": None,
            "twitter": None
        }
    
    logger.info(f"[PIPELINE] Starting content generation pipeline for: {topic}")
    logger.info("=" * 60)
    
    # Step 1: Research
    research_data = await do_research(topic)
    if research_data is None:
        return {
            "research": None,
            "blog_post": "[ERROR] Research failed.",
            "linkedin": None,
            "twitter": None
        }
    
    # Step 2: Write blog post
    blog_post = await write_blog_post(research_data)
    if blog_post.startswith("[ERROR]"):
        return {
            "research": research_data,
            "blog_post": blog_post,
            "linkedin": None,
            "twitter": None
        }
    
    # Step 3 & 4: Create social media content (in parallel)
    import asyncio
    linkedin_task = create_linkedin_post(blog_post)
    twitter_task = create_twitter_thread(blog_post)
    
    linkedin_post, twitter_thread = await asyncio.gather(linkedin_task, twitter_task)
    
    logger.info("=" * 60)
    logger.info("[SUCCESS] All content generated successfully!")
    
    return {
        "research": research_data,
        "blog_post": blog_post,
        "linkedin": linkedin_post,
        "twitter": twitter_thread
    }
