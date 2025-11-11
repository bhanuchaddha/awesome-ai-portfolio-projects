"""
Streamlit App for Employee Recruiter Agent

Run with: streamlit run streamlit_app.py
"""
import streamlit as st
from pathlib import Path
import sys
import asyncio
import os
from importlib.util import spec_from_file_location, module_from_spec

# Get the root directory and add it to the Python path to enable imports
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import the agent's functions
agent_module_name = "7_employee_recruiter_agent.7_employee_recruiter_agent"
agent_file_path = Path(__file__).resolve().parent / "7_employee_recruiter_agent.py"
spec = spec_from_file_location(agent_module_name, agent_file_path)
agent_module = module_from_spec(spec)
spec.loader.exec_module(agent_module)
process_candidates = agent_module.process_candidates


# Page config
st.set_page_config(
    page_title="Employee Recruiter Agent",
    page_icon="👔",
    layout="wide"
)

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = None
if "processing" not in st.session_state:
    st.session_state.processing = False


def check_api_keys():
    """Check if required API keys are set."""
    required_keys = ["OPENROUTER_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if key not in st.session_state:
            if key in os.environ:
                st.session_state[key] = os.environ[key]
            else:
                missing_keys.append(key)
    
    return missing_keys


def display_results(result, min_score):
    """Display the recruitment results."""
    if "error" in result:
        st.error(result['error'])
        return
    
    # Summary
    st.markdown("# Recruitment Pipeline Results")
    st.markdown("## Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Candidates", len(result['all_candidates']))
    with col2:
        st.metric("Selected", len(result['selected_candidates']))
    with col3:
        st.metric("Threshold", f"{min_score}/10")
    
    st.markdown("---")
    
    # Detailed results for each candidate
    if result['results']:
        st.markdown("## Detailed Candidate Reviews")
        
        for i, candidate in enumerate(result['results'], 1):
            # Determine if selected or rejected
            is_selected = candidate.status in ["email_sent", "scheduled", "selected"]
            
            # Status indicator
            if is_selected:
                status_badge = "SELECTED"
                status_emoji = ":white_check_mark:"
            else:
                status_badge = "NOT SELECTED"
                status_emoji = ":x:"
            
            # Candidate header
            st.markdown(f"### {i}. {candidate.name} {status_emoji}")
            st.markdown(f"**Status:** {status_badge}")
            st.markdown(f"**Email:** {candidate.email}")
            st.markdown(f"**Score:** {candidate.score}/10 {'(Meets threshold)' if candidate.score >= min_score else '(Below threshold)'}")
            
            # Screening Feedback
            st.markdown("#### Screening Feedback")
            st.info(candidate.feedback)
            
            # Why selected or not selected
            if is_selected:
                st.markdown("#### Why Selected?")
                st.markdown(f"- Score of **{candidate.score}/10** exceeds the minimum threshold of **{min_score}/10**")
                st.markdown(f"- Demonstrates strong alignment with job requirements")
                st.markdown(f"- Profile shows relevant skills and experience")
            else:
                st.markdown("#### Why Not Selected?")
                st.markdown(f"- Score of **{candidate.score}/10** is below the minimum threshold of **{min_score}/10**")
                st.markdown(f"- See screening feedback above for specific gaps or concerns")
            
            # Interview & Email details (if selected)
            if is_selected and candidate.interview_time:
                st.markdown("#### Interview Details")
                st.markdown(f"- **Date & Time:** {candidate.interview_time}")
                st.markdown(f"- **Meeting Link:** [{candidate.meeting_url}]({candidate.meeting_url})")
                
                # Show email content if available
                if 'email_contents' in result and candidate.email in result['email_contents']:
                    email_data = result['email_contents'][candidate.email]
                    st.markdown("#### Interview Invitation Email")
                    st.markdown(f"**Subject:** {email_data.get('subject', 'N/A')}")
                    st.markdown("**Body:**")
                    st.code(email_data.get('body', 'N/A'), language="text")
                    st.info("Copy the email content above to send to the candidate")
            
            st.markdown("---")
    
    # Final summary
    st.markdown("## Next Steps")
    
    if result['selected_candidates']:
        st.markdown(f"**{len(result['selected_candidates'])} candidate(s) selected for interviews:**")
        
        for idx, candidate in enumerate(result['selected_candidates'], 1):
            st.markdown(f"{idx}. **{candidate.name}** ({candidate.email}) - Score: {candidate.score}/10")
        
        st.markdown("\n**Action Items:**")
        st.markdown("- Review the interview schedules above")
        st.markdown("- Send the invitation emails to selected candidates")
        st.markdown("- Prepare interview materials based on candidate profiles")
    else:
        st.markdown(f"**No candidates met the minimum score threshold of {min_score}/10.**")
        st.markdown("**Suggestions:**")
        st.markdown("- Consider lowering the score threshold")
        st.markdown("- Review additional candidates")
        st.markdown("- Adjust job requirements if needed")


# Main app
def main():
    st.title("👔 Employee Recruiter Agent")
    st.markdown("Automated AI-powered recruitment system for screening candidates and scheduling interviews")
    
    # Sidebar for API keys
    with st.sidebar:
        st.header("Configuration")
        
        missing_keys = check_api_keys()
        
        if missing_keys:
            st.warning("Please provide your API key")
            for key in missing_keys:
                api_key = st.text_input(
                    f"Enter your {key}",
                    type="password",
                    key=f"input_{key}"
                )
                if api_key:
                    st.session_state[key] = api_key
                    os.environ[key] = api_key
                    st.rerun()
        else:
            st.success("API keys configured")
            if st.button("Reset API Keys"):
                for key in ["OPENROUTER_API_KEY"]:
                    if key in st.session_state:
                        del st.session_state[key]
                    if key in os.environ:
                        del os.environ[key]
                st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This agent screens candidate resumes, schedules interviews, "
            "and generates invitation emails using AI."
        )
    
    # Main content area
    if missing_keys:
        st.info("👈 Please configure your API keys in the sidebar to get started")
        return
    
    st.markdown("### Recruitment Configuration")
    
    # Job Description
    st.markdown("#### 1. Enter Job Description")
    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="""Enter the job description here...

Example:
We are hiring for backend and systems engineers!
Join our team building the future of agentic software

Requirements:
- You know your way around Python, typescript, docker, and AWS.
- Love to build in public and contribute to open source.
- Are ok dealing with the pressure of an early-stage startup.
""",
        help="Enter the complete job description with requirements and qualifications",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Candidate Resumes Section
    st.markdown("#### 2. Upload Candidate Resumes")
    
    st.markdown("**Upload PDF Resume Files**")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF resume files",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        for file in uploaded_files:
            st.text(f"- {file.name}")
    
    st.markdown("---")
    
    # Minimum score threshold
    st.markdown("#### 3. Set Selection Criteria")
    min_score = st.slider(
        "Minimum Score Threshold",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="Candidates scoring below this will not be selected for interviews"
    )
    
    st.caption(f"Candidates must score at least {min_score}/10 to be selected for interviews")
    
    st.markdown("---")
    
    # Process button
    if st.button("Process Candidates", type="primary", use_container_width=True):
        if not job_description:
            st.error("Please provide a job description")
            return
        
        if not uploaded_files:
            st.error("Please upload at least one PDF resume file")
            return
        
        # Prepare resume sources
        resume_sources = []
        
        # Process uploaded files
        upload_dir = Path("tmp/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for uploaded_file in uploaded_files:
            # Save the file
            file_path = upload_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            resume_sources.append(str(file_path.absolute()))
        
        # Process candidates
        with st.spinner("Processing candidates... This may take a few minutes."):
            try:
                result = asyncio.run(process_recruitment(
                    resume_sources=resume_sources,
                    job_description=job_description,
                    min_score=min_score
                ))
                st.session_state.results = result
                st.session_state.min_score = min_score
                st.success("Processing complete!")
                st.rerun()
            except Exception as e:
                st.error(f"Error processing candidates: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    # Display results if available
    if st.session_state.results:
        st.markdown("---")
        display_results(st.session_state.results, st.session_state.get("min_score", 5.0))


async def process_recruitment(resume_sources, job_description, min_score):
    """Process candidates and return results."""
    result = await process_candidates(
        candidate_resume_paths=resume_sources,
        job_description=job_description,
        min_score=min_score
    )
    return result


if __name__ == "__main__":
    main()
