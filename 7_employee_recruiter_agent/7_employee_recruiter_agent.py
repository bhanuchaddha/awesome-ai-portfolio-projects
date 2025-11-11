"""Employee Recruiter Agent - Your AI Hiring Assistant!

An automated recruitment system that screens candidates, schedules interviews,
and sends professional email communications.

Features:
- PDF resume analysis from URLs
- Intelligent candidate screening with scoring
- Automated interview scheduling (simulated)
- Professional email generation and sending (simulated)
- Multi-agent architecture for specialized tasks
"""

import asyncio
import io
import os
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent
from typing import Any, List, Optional

import requests
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.utils.log import logger
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pypdf import PdfReader

# Load environment variables from .env file
load_dotenv()


# --- Pydantic Models ---

class ScreeningResult(BaseModel):
    """Results from candidate screening."""
    name: str = Field(..., description="Candidate's name")
    email: str = Field(..., description="Candidate's email address")
    score: float = Field(..., description="Screening score from 0-10")
    feedback: str = Field(..., description="Detailed feedback on the candidate")


class ScheduledCall(BaseModel):
    """Scheduled interview details."""
    name: str = Field(..., description="Candidate's name")
    email: str = Field(..., description="Candidate's email address")
    call_time: str = Field(..., description="Scheduled interview time")
    url: str = Field(..., description="Meeting URL")


class EmailContent(BaseModel):
    """Email content structure."""
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")


class CandidateResult(BaseModel):
    """Complete result for a single candidate."""
    name: str
    email: str
    score: float
    feedback: str
    status: str  # "selected", "rejected", "scheduled", "email_sent"
    interview_time: Optional[str] = None
    meeting_url: Optional[str] = None
    email_subject: Optional[str] = None


# --- PDF Utility Functions ---

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a local PDF file.
    
    Args:
        file_path: Local path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        logger.info(f"[PDF] Extracting text from: {file_path}")
        
        # Read local file
        with open(file_path, 'rb') as f:
            pdf_content = io.BytesIO(f.read())
        
        # Extract text from PDF
        reader = PdfReader(pdf_content)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        logger.info(f"[PDF] Extracted {len(text)} characters")
        return text
    except Exception as e:
        logger.error(f"[ERROR] Failed to extract PDF from {file_path}: {e}")
        return ""


# --- Simulated Tools ---

def simulate_zoom_scheduling(agent: Agent, candidate_name: str, candidate_email: str) -> str:
    """Simulate Zoom call scheduling."""
    # Generate a future time slot (1-7 days from now, between 10am-6pm)
    base_time = datetime.now() + timedelta(days=random.randint(1, 7))
    hour = random.randint(10, 17)  # 10am to 5pm
    scheduled_time = base_time.replace(hour=hour, minute=0, second=0, microsecond=0)

    # Generate fake Zoom URL
    meeting_id = random.randint(100000000, 999999999)
    zoom_url = f"https://zoom.us/j/{meeting_id}"

    result = "[OK] Zoom call scheduled successfully!\n"
    result += f"Time: {scheduled_time.strftime('%Y-%m-%d %H:%M')} IST\n"
    result += f"Meeting URL: {zoom_url}\n"
    result += f"Participant: {candidate_name} ({candidate_email})"

    logger.info(f"[ZOOM] Scheduled interview for {candidate_name} at {scheduled_time}")
    return result


def simulate_email_sending(agent: Agent, to_email: str, subject: str, body: str) -> str:
    """Simulate email sending."""
    result = "[OK] Email sent successfully!\n"
    result += f"To: {to_email}\n"
    result += f"Subject: {subject}\n"
    result += f"Body length: {len(body)} characters\n"
    result += f"Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    logger.info(f"[EMAIL] Sent email to {to_email}")
    return result


# --- Agents ---

screening_agent = Agent(
    name="Screening Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are an expert HR specialist who screens candidates for job positions.
    You analyze resumes against job requirements and provide detailed assessments.
    """),
    instructions=dedent("""\
    Screen candidates based on their resume and job description:
    
    1. Analysis Points:
       - Relevant work experience and skills
       - Educational background
       - Technical competencies
       - Cultural fit indicators
       - Career progression
    
    2. Scoring (0-10):
       - 8-10: Excellent match, strong candidate
       - 5-7: Good match, worth interviewing
       - 3-4: Moderate match, possible backup
       - 0-2: Poor match, not suitable
    
    3. Feedback:
       - List key strengths
       - Note any concerns or gaps
       - Mention specific relevant experience
       - Be constructive and professional
    
    4. Extract Information:
       - Find candidate's name from resume
       - Extract email address
       - If not found, use placeholder values
    
    Always be thorough, fair, and professional in your assessment.
    """),
    output_schema=ScreeningResult,
    markdown=True,
    debug_mode=True,
)

scheduler_agent = Agent(
    name="Scheduler Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are an interview scheduling specialist who coordinates meeting times
    and creates calendar invites for candidate interviews.
    """),
    instructions=dedent(f"""\
    Schedule interview calls for candidates:
    
    Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST
    
    1. Scheduling Guidelines:
       - Schedule between 10am-6pm IST on weekdays
       - Use the simulate_zoom_scheduling tool
       - Provide realistic future dates (1-7 days out)
       - Include all meeting details
    
    2. Meeting Details:
       - Candidate name and email
       - Interview date and time
       - Zoom meeting URL
       - Duration: 1 hour
    
    3. Output:
       Return structured data with name, email, call_time, and url.
    """),
    tools=[simulate_zoom_scheduling],
    output_schema=ScheduledCall,
    markdown=True,
    debug_mode=True,
)

email_writer_agent = Agent(
    name="Email Writer Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are a professional email writer who creates warm, engaging
    interview invitation emails for candidates.
    """),
    instructions=dedent("""\
    Write professional interview invitation emails:
    
    1. Structure:
       - Congratulatory opening
       - Interview details (date, time, meeting link)
       - What to expect in the interview
       - Next steps and contact information
       - Professional closing
    
    2. Tone:
       - Professional but warm
       - Enthusiastic about the candidate
       - Clear and concise
       - Encouraging
    
    3. Include:
       - Specific interview date and time
       - Zoom meeting link
       - Interview duration (1 hour)
       - Interviewer name and role
       - Company excitement about candidate
    
    4. Sign-off:
       Sign emails as 'John Doe, Senior Software Engineer'
       Email: john@agno.com
    
    Keep emails concise (200-300 words) but warm and welcoming.
    """),
    output_schema=EmailContent,
    markdown=True,
    debug_mode=True,
)

email_sender_agent = Agent(
    name="Email Sender Agent",
    model=OpenRouter(
        id=os.getenv("OPENROUTER_MODEL_ID", "minimax/minimax-m2:free"),
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    description=dedent("""\
    You are an email delivery specialist who sends emails using
    the email sending tool and confirms successful delivery.
    """),
    instructions=dedent("""\
    Send emails using the simulate_email_sending tool:
    
    1. Use the tool with exact parameters provided
    2. Confirm successful delivery
    3. Report any issues
    
    Always confirm the email was sent with details.
    """),
    tools=[simulate_email_sending],
    markdown=True,
    debug_mode=True,
)


# --- Main Recruitment Functions ---

async def screen_candidate(resume_path: str, job_description: str, resume_cache: dict) -> Optional[ScreeningResult]:
    """Screen a single candidate from their resume file."""
    logger.info(f"[SCREEN] Processing candidate from: {Path(resume_path).name}")
    
    # Extract resume text (with caching)
    if resume_path not in resume_cache:
        resume_text = extract_text_from_pdf(resume_path)
        if not resume_text:
            logger.error(f"[ERROR] Could not extract text from resume: {resume_path}")
            return None
        resume_cache[resume_path] = resume_text
    else:
        logger.info("[CACHE] Using cached resume content")
    
    resume_text = resume_cache[resume_path]
    
    # Screen the candidate
    screening_prompt = f"""
    Please screen this candidate for the job position.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Evaluate how well this candidate matches the job requirements and provide a score from 0-10.
    """
    
    try:
        response = await screening_agent.arun(screening_prompt)
        
        if not response or not response.content:
            logger.error("[ERROR] Failed to screen candidate")
            return None
        
        if isinstance(response.content, ScreeningResult):
            result = response.content
            logger.info(f"[SCREEN] {result.name} scored {result.score}/10")
            return result
        else:
            # Fallback: Try to parse text response manually
            logger.warning("[WARNING] Screening result not in expected format, attempting fallback parsing")
            text_content = str(response.content)
            logger.debug(f"[DEBUG] Raw response content: {text_content[:500]}...")
            
            # Extract name (look for common patterns)
            name = "Unknown Candidate"
            if "name:" in text_content.lower():
                lines = text_content.split('\n')
                for line in lines:
                    if "name:" in line.lower():
                        name = line.split(':', 1)[1].strip()
                        break
            
            # Extract email
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text_content)
            email = email_match.group(0) if email_match else f"{name.replace(' ', '.').lower()}@example.com"
            
            # Extract score (look for X/10 or score: X patterns)
            score = 5.0  # default
            score_patterns = [
                r'score[:\s]+(\d+\.?\d*)',
                r'(\d+\.?\d*)/10',
                r'rating[:\s]+(\d+\.?\d*)'
            ]
            for pattern in score_patterns:
                score_match = re.search(pattern, text_content.lower())
                if score_match:
                    try:
                        score = float(score_match.group(1))
                        if score > 10:  # normalize if needed
                            score = score / 10
                        break
                    except:
                        pass
            
            # Use the full text as feedback
            feedback = text_content[:1000]  # limit to 1000 chars
            
            result = ScreeningResult(
                name=name,
                email=email,
                score=score,
                feedback=feedback
            )
            logger.info(f"[SCREEN] {result.name} scored {result.score}/10 (fallback parsing)")
            return result
            
    except Exception as e:
        logger.error(f"[ERROR] Screening failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None


async def schedule_interview(candidate: ScreeningResult) -> Optional[ScheduledCall]:
    """Schedule an interview for a candidate."""
    logger.info(f"[SCHEDULE] Scheduling interview for {candidate.name}")
    
    schedule_prompt = f"""
    Schedule a 1-hour interview call for:
    - Candidate: {candidate.name}
    - Email: {candidate.email}
    - Interviewer: Dirk Brand (dirk@phidata.com)
    
    Use the simulate_zoom_scheduling tool to create the meeting.
    """
    
    try:
        response = await scheduler_agent.arun(schedule_prompt)
        
        if not response or not response.content:
            logger.error("[ERROR] Failed to schedule interview")
            return None
        
        if isinstance(response.content, ScheduledCall):
            result = response.content
            logger.info(f"[SCHEDULE] Interview scheduled for {result.call_time}")
            return result
        else:
            # Fallback: Parse text response or use simulated scheduling directly
            logger.warning("[WARNING] Scheduling result not in expected format, using fallback")
            
            # Generate a simulated schedule
            base_time = datetime.now() + timedelta(days=random.randint(1, 7))
            hour = random.randint(10, 17)
            scheduled_time = base_time.replace(hour=hour, minute=0, second=0, microsecond=0)
            meeting_id = random.randint(100000000, 999999999)
            zoom_url = f"https://zoom.us/j/{meeting_id}"
            
            result = ScheduledCall(
                name=candidate.name,
                email=candidate.email,
                call_time=scheduled_time.strftime('%Y-%m-%d %H:%M IST'),
                url=zoom_url
            )
            logger.info(f"[SCHEDULE] Interview scheduled for {result.call_time} (fallback)")
            return result
            
    except Exception as e:
        logger.error(f"[ERROR] Scheduling failed: {str(e)}")
        return None


async def send_interview_invitation(candidate: ScreeningResult, scheduled_call: ScheduledCall) -> Optional[EmailContent]:
    """Generate and send interview invitation email."""
    logger.info(f"[EMAIL] Generating invitation for {candidate.name}")
    
    # Generate email content
    email_prompt = f"""
    Write a professional interview invitation email for:
    - Candidate: {candidate.name} ({candidate.email})
    - Interview time: {scheduled_call.call_time}
    - Meeting URL: {scheduled_call.url}
    
    Congratulate them on being selected and include all necessary details.
    """
    
    try:
        response = await email_writer_agent.arun(email_prompt)
        
        if not response or not response.content:
            logger.error("[ERROR] Failed to generate email")
            return None
        
        if isinstance(response.content, EmailContent):
            email_content = response.content
            logger.info(f"[EMAIL] Generated email: {email_content.subject}")
            
            # Send the email
            send_prompt = f"""
            Send the interview invitation email:
            - To: {candidate.email}
            - Subject: {email_content.subject}
            - Body: {email_content.body}
            
            Use the simulate_email_sending tool.
            """
            
            send_response = await email_sender_agent.arun(send_prompt)
            
            if send_response:
                logger.info(f"[EMAIL] Successfully sent to {candidate.email}")
                return email_content
            else:
                logger.error("[ERROR] Failed to send email")
                return None
        else:
            # Fallback: Generate a simple email from text response
            logger.warning("[WARNING] Email content not in expected format, using fallback")
            
            text_content = str(response.content)
            subject = f"Interview Invitation - Backend Engineer Position"
            
            # Try to extract subject if mentioned
            subject_match = re.search(r'subject[:\s]+(.*?)[\n\r]', text_content, re.IGNORECASE)
            if subject_match:
                subject = subject_match.group(1).strip()
            
            # Use full text as body, or generate a template
            if len(text_content) > 50:
                body = text_content
            else:
                body = f"""Dear {candidate.name},

Congratulations! We are excited to inform you that you have been selected to move forward in the hiring process.

Interview Details:
- Date & Time: {scheduled_call.call_time}
- Duration: 1 hour
- Meeting Link: {scheduled_call.url}

Please confirm your availability for this time slot by replying to this email.

We look forward to speaking with you!

Best regards,
John Doe
Senior Software Engineer
john@agno.com"""
            
            email_content = EmailContent(subject=subject, body=body)
            logger.info(f"[EMAIL] Generated email: {email_content.subject} (fallback)")
            return email_content
            
    except Exception as e:
        logger.error(f"[ERROR] Email generation/sending failed: {str(e)}")
        return None


async def process_candidates(
    candidate_resume_paths: List[str],
    job_description: str,
    min_score: float = 5.0
) -> dict:
    """
    Process all candidates through the complete recruitment workflow.
    
    Returns a dictionary with:
    - all_candidates: List of all screened candidates
    - selected_candidates: List of candidates who passed screening
    - results: Complete results for each candidate
    - email_contents: Dict mapping email to email content (subject, body)
    """
    if not candidate_resume_paths:
        logger.error("[ERROR] No candidate resume files provided")
        return {
            "all_candidates": [],
            "selected_candidates": [],
            "results": [],
            "email_contents": {},
            "error": "No candidate resume files provided"
        }
    
    if not job_description:
        logger.error("[ERROR] No job description provided")
        return {
            "all_candidates": [],
            "selected_candidates": [],
            "results": [],
            "email_contents": {},
            "error": "No job description provided"
        }
    
    logger.info(f"[PIPELINE] Starting recruitment process for {len(candidate_resume_paths)} candidates")
    logger.info("=" * 60)
    
    resume_cache = {}
    all_candidates = []
    selected_candidates = []
    results = []
    email_contents = {}  # Store email contents for UI display
    
    # Phase 1: Candidate Screening
    logger.info("[PHASE 1] CANDIDATE SCREENING")
    logger.info("-" * 60)
    
    for i, file_path in enumerate(candidate_resume_paths, 1):
        logger.info(f"[CANDIDATE {i}/{len(candidate_resume_paths)}] Processing...")
        
        screening_result = await screen_candidate(file_path, job_description, resume_cache)
        
        if screening_result:
            all_candidates.append(screening_result)
            
            candidate_result = CandidateResult(
                name=screening_result.name,
                email=screening_result.email,
                score=screening_result.score,
                feedback=screening_result.feedback,
                status="rejected" if screening_result.score < min_score else "selected"
            )
            
            if screening_result.score >= min_score:
                selected_candidates.append(screening_result)
                logger.info(f"[SELECTED] {screening_result.name} - Score: {screening_result.score}/10")
            else:
                logger.info(f"[REJECTED] {screening_result.name} - Score: {screening_result.score}/10 (below {min_score})")
            
            results.append(candidate_result)
        else:
            logger.error(f"[ERROR] Failed to process candidate from {file_path}")
    
    # Phase 2: Interview Scheduling & Email Communication
    if selected_candidates:
        logger.info(f"\n[PHASE 2] INTERVIEW SCHEDULING ({len(selected_candidates)} candidates)")
        logger.info("-" * 60)
        
        for i, candidate in enumerate(selected_candidates, 1):
            logger.info(f"[INTERVIEW {i}/{len(selected_candidates)}] Processing {candidate.name}...")
            
            # Schedule interview
            scheduled_call = await schedule_interview(candidate)
            
            if scheduled_call:
                # Send invitation email
                email_content = await send_interview_invitation(candidate, scheduled_call)
                
                # Update results and store email content
                for result in results:
                    if result.email == candidate.email:
                        result.interview_time = scheduled_call.call_time
                        result.meeting_url = scheduled_call.url
                        if email_content:
                            result.email_subject = email_content.subject
                            result.status = "email_sent"
                            # Store email content for UI
                            email_contents[candidate.email] = {
                                "subject": email_content.subject,
                                "body": email_content.body
                            }
                        else:
                            result.status = "scheduled"
                        break
            else:
                logger.error(f"[ERROR] Failed to schedule interview for {candidate.name}")
    else:
        logger.info("\n[PHASE 2] No candidates selected for interviews")
    
    logger.info("=" * 60)
    logger.info(f"[COMPLETE] Processed {len(all_candidates)} candidates, {len(selected_candidates)} selected")
    
    return {
        "all_candidates": all_candidates,
        "selected_candidates": selected_candidates,
        "results": results,
        "email_contents": email_contents
    }

