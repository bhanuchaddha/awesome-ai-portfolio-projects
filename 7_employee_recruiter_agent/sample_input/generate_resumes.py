"""
Generate sample PDF resumes for testing the Employee Recruiter Agent
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path


def create_john_smith_resume():
    """Create resume for John Smith - Backend Engineer (Should score ~7.5/10)"""
    
    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / "john_smith_resume.pdf"
    
    doc = SimpleDocTemplate(str(filename), pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        spaceBefore=12
    )
    
    # Header
    story.append(Paragraph("John Smith", title_style))
    story.append(Paragraph("Backend Engineer", styles['Normal']))
    story.append(Paragraph("Email: john.smith@example.com | Phone: +1 (555) 123-4567", styles['Normal']))
    story.append(Paragraph("GitHub: github.com/johnsmith | LinkedIn: linkedin.com/in/johnsmith", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(
        "Experienced Backend Engineer with 5+ years building scalable microservices and "
        "distributed systems. Proven expertise in Python, TypeScript, AWS, and Docker. "
        "Passionate about open-source contributions and infrastructure as code. "
        "Strong track record of delivering high-performance backend solutions in fast-paced environments.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Technical Skills
    story.append(Paragraph("Technical Skills", heading_style))
    skills_data = [
        ["Languages:", "Python, TypeScript, JavaScript, Go"],
        ["Cloud & DevOps:", "AWS (EC2, Lambda, S3, RDS, CloudFormation), Docker, Kubernetes"],
        ["Infrastructure:", "Terraform, Ansible, CI/CD (GitHub Actions, Jenkins)"],
        ["Databases:", "PostgreSQL, MongoDB, Redis, DynamoDB"],
        ["Frameworks:", "FastAPI, Django, Express.js, Node.js"],
        ["Other:", "Microservices, RESTful APIs, GraphQL, Message Queues (RabbitMQ, SQS)"]
    ]
    
    skills_table = Table(skills_data, colWidths=[1.5*inch, 4.5*inch])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 0.1*inch))
    
    # Work Experience
    story.append(Paragraph("Work Experience", heading_style))
    
    story.append(Paragraph("<b>Senior Backend Engineer</b> | TechCorp Inc. | 2021 - Present", styles['Normal']))
    story.append(Paragraph(
        "• Architected and deployed Python microservices handling 10M+ daily requests using FastAPI and AWS Lambda<br/>"
        "• Reduced infrastructure costs by 40% through optimization of AWS resources and containerization with Docker<br/>"
        "• Implemented Infrastructure as Code using Terraform, managing 50+ AWS resources across multiple environments<br/>"
        "• Led migration from monolith to microservices architecture, improving deployment frequency by 300%<br/>"
        "• Mentored junior developers and contributed to open-source projects (3 major PRs accepted)",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Backend Developer</b> | DataFlow Systems | 2019 - 2021", styles['Normal']))
    story.append(Paragraph(
        "• Developed RESTful APIs using Django and PostgreSQL serving 1M+ users<br/>"
        "• Implemented real-time data processing pipelines using AWS Kinesis and Lambda<br/>"
        "• Set up CI/CD pipelines with GitHub Actions, reducing deployment time by 60%<br/>"
        "• Integrated third-party services and managed Docker containerization<br/>"
        "• Collaborated with frontend team using TypeScript and Node.js for BFF layer",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Education
    story.append(Paragraph("Education", heading_style))
    story.append(Paragraph(
        "<b>Bachelor of Science in Computer Science</b><br/>"
        "University of California, Berkeley | 2015 - 2019<br/>"
        "GPA: 3.7/4.0",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Open Source & Community
    story.append(Paragraph("Open Source & Community", heading_style))
    story.append(Paragraph(
        "• Active contributor to popular Python packages (FastAPI, SQLAlchemy)<br/>"
        "• Maintainer of docker-compose-automation tool (500+ GitHub stars)<br/>"
        "• Speaker at PyCon 2023: 'Building Scalable Microservices with Python'<br/>"
        "• Regular contributor to AWS CDK documentation",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(story)
    print(f"Created: {filename}")


def create_sarah_johnson_resume():
    """Create resume for Sarah Johnson - Frontend Developer (Should score ~3.5/10)"""
    
    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / "sarah_johnson_resume.pdf"
    
    doc = SimpleDocTemplate(str(filename), pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        spaceBefore=12
    )
    
    # Header
    story.append(Paragraph("Sarah Johnson", title_style))
    story.append(Paragraph("Frontend Developer", styles['Normal']))
    story.append(Paragraph("Email: sarah.j@example.com | Phone: +1 (555) 987-6543", styles['Normal']))
    story.append(Paragraph("Portfolio: sarahjohnson.dev | LinkedIn: linkedin.com/in/sarahjohnson", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(
        "Creative Frontend Developer with 4 years of experience building beautiful, responsive "
        "user interfaces. Expert in React, JavaScript, and modern CSS. Passionate about UX/UI "
        "design and creating intuitive user experiences. Strong collaboration skills and "
        "experience working with design teams.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Technical Skills
    story.append(Paragraph("Technical Skills", heading_style))
    skills_data = [
        ["Languages:", "JavaScript, TypeScript, HTML5, CSS3"],
        ["Frameworks:", "React, Next.js, Vue.js, Redux, React Query"],
        ["Styling:", "Tailwind CSS, Material-UI, Styled Components, SASS"],
        ["Tools:", "Git, Webpack, Vite, npm, Figma"],
        ["Testing:", "Jest, React Testing Library, Cypress"],
        ["Backend (Basic):", "Node.js, Express, REST APIs"]
    ]
    
    skills_table = Table(skills_data, colWidths=[1.5*inch, 4.5*inch])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 0.1*inch))
    
    # Work Experience
    story.append(Paragraph("Work Experience", heading_style))
    
    story.append(Paragraph("<b>Senior Frontend Developer</b> | DesignCo Studios | 2022 - Present", styles['Normal']))
    story.append(Paragraph(
        "• Built responsive web applications using React and TypeScript for 50+ clients<br/>"
        "• Implemented pixel-perfect designs from Figma mockups with 99% accuracy<br/>"
        "• Optimized application performance, achieving 95+ Lighthouse scores<br/>"
        "• Collaborated with UX designers to improve user flows and accessibility<br/>"
        "• Mentored 2 junior developers in React best practices",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Frontend Developer</b> | WebSolutions Inc. | 2020 - 2022", styles['Normal']))
    story.append(Paragraph(
        "• Developed interactive dashboards using React and Material-UI<br/>"
        "• Integrated RESTful APIs with frontend applications<br/>"
        "• Implemented state management using Redux and Context API<br/>"
        "• Created reusable component library used across 5 projects<br/>"
        "• Basic Node.js backend work for simple CRUD operations",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Education
    story.append(Paragraph("Education", heading_style))
    story.append(Paragraph(
        "<b>Bachelor of Arts in Digital Media</b><br/>"
        "New York University | 2016 - 2020<br/>"
        "Minor in Computer Science",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Certifications & Courses
    story.append(Paragraph("Certifications & Courses", heading_style))
    story.append(Paragraph(
        "• Meta Frontend Developer Professional Certificate (2023)<br/>"
        "• Advanced React Patterns Course (2022)<br/>"
        "• Introduction to Python Programming (Coursera, 2021)<br/>"
        "• UX Design Fundamentals (2020)",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # Projects
    story.append(Paragraph("Notable Projects", heading_style))
    story.append(Paragraph(
        "• <b>E-commerce Platform:</b> Built complete frontend using Next.js and Stripe integration<br/>"
        "• <b>Dashboard Application:</b> Real-time data visualization with Chart.js and React<br/>"
        "• <b>Portfolio Generator:</b> SaaS tool for creating developer portfolios (React + Firebase)",
        styles['Normal']
    ))
    
    # Build PDF
    doc.build(story)
    print(f"Created: {filename}")


if __name__ == "__main__":
    print("Generating sample resumes...")
    create_john_smith_resume()
    create_sarah_johnson_resume()
    print("\nResumes generated successfully!")
    print("\nThese resumes can be used to test the Employee Recruiter Agent.")
    print("John Smith should score ~7.5/10 (selected for backend role)")
    print("Sarah Johnson should score ~3.5/10 (not selected - frontend focus)")

