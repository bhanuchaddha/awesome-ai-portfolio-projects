# Sample Resume Files

This directory contains sample PDF resume files for testing the Employee Recruiter Agent.

## Files

### 1. `john_smith_resume.pdf`
**Candidate Profile:** Backend Engineer with strong qualifications

**Key Highlights:**
- 5+ years of experience with Python and TypeScript
- Extensive AWS and Docker experience
- Infrastructure as Code (Terraform) expertise
- Active open-source contributor
- Microservices architecture experience

**Expected Score:** ~7.5/10 (Should be SELECTED)

**Why Selected:**
- Meets all core requirements for backend/systems engineer role
- Strong Python and cloud infrastructure background
- Demonstrates startup-friendly mindset through open-source work
- Has bonus skills (Terraform, infrastructure as code)

---

### 2. `sarah_johnson_resume.pdf`
**Candidate Profile:** Frontend Developer with limited backend experience

**Key Highlights:**
- 4 years of frontend development (React, JavaScript)
- Strong UI/UX skills
- Basic Node.js exposure
- Limited Python knowledge
- No AWS or Docker experience

**Expected Score:** ~3.5/10 (Should be REJECTED)

**Why Not Selected:**
- Primarily frontend-focused, lacks backend expertise
- No AWS or Docker experience
- Limited Python skills
- No evidence of infrastructure or systems work
- Does not meet core backend engineer requirements

---

## How to Use

### Testing the Agent

1. **Run the Streamlit app:**
   ```bash
   streamlit run 7_employee_recruiter_agent/streamlit_app.py
   ```

2. **Upload the resumes:**
   - Use the file uploader in the interface
   - Select both `john_smith_resume.pdf` and `sarah_johnson_resume.pdf`

3. **Enter job description:**
   ```
   We are hiring for backend and systems engineers!
   Join our team building the future of agentic software

   Requirements:
   - You know your way around Python, typescript, docker, and AWS.
   - Love to build in public and contribute to open source.
   - Are ok dealing with the pressure of an early-stage startup.
   - Want to be a part of the biggest technological shift since the internet.
   - Bonus: experience with infrastructure as code.
   - Bonus: starred Agno repo.
   ```

4. **Set threshold:** 5.0/10 (default)

5. **Click "Process Candidates"**

### Expected Results

- **Total Candidates:** 2
- **Selected:** 1 (John Smith)
- **Rejected:** 1 (Sarah Johnson)

John Smith should receive:
- High score (7-8/10 range)
- Interview scheduling
- Professional invitation email

Sarah Johnson should receive:
- Low score (3-4/10 range)
- Rejection with constructive feedback
- Clear explanation of skill gaps

---

## Regenerating Resumes

If you need to regenerate the PDF files or create variations:

```bash
cd 7_employee_recruiter_agent/sample_input
python3 generate_resumes.py
```

The `generate_resumes.py` script uses the `reportlab` library to create professional-looking PDF resumes. You can modify this script to:
- Add more candidates
- Adjust candidate qualifications
- Test different scoring scenarios
- Create resumes for different job roles

## Notes

- These resumes are fictional and created for testing purposes only
- The AI screening agent analyzes the actual PDF content
- Scores may vary slightly depending on the LLM model used
- The agent uses structured output for consistent evaluation

