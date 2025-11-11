# Employee Recruiter Agent

An automated AI-powered recruitment system that streamlines the hiring process from resume screening to interview scheduling and email communications.

## Architecture

The system uses **4 specialized agents** working in a coordinated workflow:

### 1. Screening Agent
- Analyzes PDF resumes against job requirements
- Scores candidates from 0-10 based on job fit
- Provides detailed feedback on strengths and concerns
- Extracts candidate name and email
- **Output**: Structured screening results with scores and feedback

### 2. Scheduler Agent
- Creates interview appointments for qualified candidates
- Schedules meetings between 10am-6pm IST on weekdays
- Generates Zoom meeting links (simulated)
- **Output**: Interview details with date, time, and meeting URL

### 3. Email Writer Agent
- Composes professional interview invitation emails
- Includes congratulations, interview details, and next steps
- Maintains warm, professional tone
- **Output**: Email subject and body content

### 4. Email Sender Agent
- Sends invitation emails to selected candidates (simulated)
- Confirms successful delivery with details
- **Output**: Delivery confirmation

## Workflow Pipeline

```
Uploaded PDF Files + Job Description
         ↓
Phase 1: CANDIDATE SCREENING
         ├─→ Extract PDF text from uploaded files
         ├─→ Analyze against job requirements
         ├─→ Score (0-10) and provide feedback
         └─→ Filter by minimum score (default: 5.0)
         ↓
Phase 2: SELECTED CANDIDATES
         ├─→ Schedule Zoom interviews
         ├─→ Generate invitation emails
         └─→ Send emails (simulated)
         ↓
Complete Results Report
```

## Features

- **PDF Resume Processing**: Extracts text from uploaded PDF resume files
- **Intelligent Screening**: AI-powered candidate evaluation with detailed feedback
- **Automated Scheduling**: Creates interview appointments with realistic time slots
- **Professional Communications**: Generates and sends interview invitation emails
- **Multi-Agent Architecture**: Specialized agents for different recruitment tasks
- **Simulated Tools**: Demo Zoom scheduling and email sending (can be replaced with real tools)
- **Configurable Threshold**: Set minimum score for candidate selection
- **User-Friendly Interface**: Upload multiple PDF files through web interface

## How to Run

1. **Install dependencies**:
   ```bash
   cd 7_employee_recruiter_agent
   uv pip install -e .
   ```

2. **Set up your environment variables**:
   Create a `.env` file in the root of the project and add your API key:
   ```
   OPENROUTER_API_KEY="your-openrouter-api-key"
   OPENROUTER_MODEL_ID="minimax/minimax-m2:free"  # Optional, defaults to minimax/minimax-m2:free
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run 7_employee_recruiter_agent/streamlit_app.py
   ```

4. **Use the interface**:
   - Enter the job description
   - Upload PDF resume files (supports multiple files)
   - Set minimum score threshold (default: 5.0)
   - Click "Process Candidates"

5. **Test with sample resumes** (optional):
   - Sample PDF resumes are available in `sample_input/` directory
   - `john_smith_resume.pdf` - Backend engineer (should score ~7.5/10)
   - `sarah_johnson_resume.pdf` - Frontend developer (should score ~3.5/10)
   - See `sample_input/README.md` for details

## Input Format

### Resume Files
- PDF files uploaded through the web interface
- Supports multiple file uploads
- Files are temporarily stored in `tmp/uploads/`

### Job Description
- Complete job posting with requirements
- Include skills, experience, and qualifications
- The more detailed, the better the screening

### Minimum Score
- Range: 0.0 to 10.0
- Default: 5.0
- Candidates scoring below this threshold will not be selected

## Output

The system provides a comprehensive report including:

- **Summary**: Total candidates processed and selected
- **Candidate Details**: For each candidate:
  - Name and email
  - Screening score (0-10)
  - Detailed feedback
  - Selection status
  - Interview details (if selected)
  - Meeting URL (if scheduled)
  - Email status (if sent)
- **Selected Candidates Summary**: Quick list of all selected candidates

## Simulated vs Real Tools

This implementation uses **simulated** Zoom scheduling and email sending for demonstration purposes:

- **Zoom Scheduling**: Generates fake meeting URLs and times
- **Email Sending**: Logs email details without actual delivery

To use **real tools** in production:
1. Replace `simulate_zoom_scheduling` with actual Zoom API integration
2. Replace `simulate_email_sending` with SMTP or email service API
3. Add appropriate authentication and configuration

## Dependencies

- `agno>=2.2.6` - Agent framework
- `openrouter>=0.1.0` - LLM model provider
- `python-dotenv>=1.0.0` - Environment variable management
- `streamlit>=1.28.0` - Web UI framework
- `pypdf>=4.0.0` - PDF text extraction
- `requests>=2.31.0` - HTTP requests for PDF downloads

## Notes

- Resume processing is cached to avoid re-downloading
- All agents use structured output with Pydantic models
- Logging provides detailed progress tracking
- Error handling at each pipeline stage
- Async/await for efficient concurrent processing

