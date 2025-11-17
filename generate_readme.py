#!/usr/bin/env python3
"""
Auto-generate README.md from agent display-info.json files.

This script scans all agent directories for documentation/display-info.json files
and generates a beautiful navigation hub README with card-based grid layout.

Usage:
    python generate_readme.py
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def find_agent_configs(root_dir: Path) -> List[Dict[str, Any]]:
    """Find and load all display-info.json files from agent directories."""
    configs = []
    
    # Look for all directories that might contain agents
    for item in root_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['common', 'local', 'assets']:
            config_path = item / "documentation" / "display-info.json"
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        configs.append(config)
                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse {config_path}: {e}")
                except Exception as e:
                    print(f"Warning: Error reading {config_path}: {e}")
    
    # Sort by order field, then by name
    configs.sort(key=lambda x: (x.get('order', 999), x.get('name', '')))
    
    # Filter only active agents
    return [c for c in configs if c.get('active', True)]


def generate_badge(label: str, message: str, color: str = "blue") -> str:
    """Generate a shields.io badge markdown."""
    return f"![{label}](https://img.shields.io/badge/{label.replace(' ', '%20')}-{message.replace(' ', '%20')}-{color})"


def find_demo_image(agent: Dict[str, Any], root_dir: Path) -> str:
    """
    Find the demo image file for an agent.
    Checks for demo.png, demo.gif, demo.jpg, or demo.jpeg in the assets directory.
    
    Returns the path to the image if found, or empty string if not found.
    """
    folder = agent.get('folder', '')
    if not folder:
        return ''
    
    # Construct the assets directory path
    assets_dir = root_dir / folder / "documentation" / "assets"
    
    # Check for supported image formats in order of preference
    image_extensions = ['.png', '.gif', '.jpg', '.jpeg']
    for ext in image_extensions:
        demo_file = assets_dir / f"demo{ext}"
        if demo_file.exists():
            # Return relative path from repo root
            return str(demo_file.relative_to(root_dir))
    
    return ''


def generate_agent_card_html(agent: Dict[str, Any], root_dir: Path) -> str:
    """Generate HTML card for a single agent."""
    name = agent.get('name', 'Unnamed Agent')
    emoji = agent.get('emoji', '🤖')
    description = agent.get('description', '')
    folder = agent.get('folder', '')
    deployed_url = agent.get('deployedUrl', '')
    technologies = agent.get('technologies', [])
    category = agent.get('category', 'Other')
    business_impact = agent.get('businessImpact', {})
    
    # Find demo image (supports .png, .gif, .jpg, .jpeg)
    demo_image_path = find_demo_image(agent, root_dir)
    
    # Build the card HTML
    card_html = f'''<div align="center" style="margin: 20px;">
  <h3>{emoji} {name}</h3>
'''
    
    # Add demo image or placeholder
    if demo_image_path and os.path.exists(demo_image_path):
        if deployed_url:
            card_html += f'  <a href="{deployed_url}" target="_blank">\n'
            card_html += f'    <img src="{demo_image_path}" alt="{name} Demo" width="100%" style="border-radius: 8px; border: 1px solid #ddd;"/>\n'
            card_html += f'  </a>\n'
        else:
            card_html += f'  <img src="{demo_image_path}" alt="{name} Demo" width="100%" style="border-radius: 8px; border: 1px solid #ddd;"/>\n'
    else:
        # Placeholder when no demo image exists
        card_html += f'  <img src="https://via.placeholder.com/400x300/1e293b/f8fafc?text={name.replace(" ", "+")}" alt="{name} Placeholder" width="100%" style="border-radius: 8px;"/>\n'
    
    card_html += f'''  
  <p align="left"><strong>{description}</strong></p>
  
  <p align="left">
    <strong>Category:</strong> {category}<br/>
'''
    
    # Add business impact if available
    if business_impact:
        time_saved = business_impact.get('timeSaved', '')
        if time_saved:
            card_html += f'    <strong>Impact:</strong> {time_saved}<br/>\n'
    
    card_html += '  </p>\n  \n'
    
    # Add technology badges (max 3 for compact display)
    if technologies:
        card_html += '  <p align="left">\n'
        for tech in technologies[:3]:
            tech_clean = tech.replace(' ', '%20').replace('+', '%2B')
            card_html += f'    <img src="https://img.shields.io/badge/-{tech_clean}-informational?style=flat&logo=python&logoColor=white" alt="{tech}"/>\n'
        if len(technologies) > 3:
            card_html += f'    <img src="https://img.shields.io/badge/-+{len(technologies)-3}%20more-lightgrey?style=flat" alt="More technologies"/>\n'
        card_html += '  </p>\n  \n'
    
    # Add action buttons
    card_html += '  <p align="center">\n'
    
    if deployed_url:
        card_html += f'    <a href="{deployed_url}" target="_blank">\n'
        card_html += f'      <img src="https://img.shields.io/badge/Try%20Live%20Demo-00C7B7?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo"/>\n'
        card_html += f'    </a>\n'
    
    if folder:
        readme_path = f"{folder}/README.md"
        card_html += f'    <a href="{readme_path}">\n'
        card_html += f'      <img src="https://img.shields.io/badge/Documentation-0066FF?style=for-the-badge&logo=read-the-docs&logoColor=white" alt="Documentation"/>\n'
        card_html += f'    </a>\n'
        card_html += f'    <a href="{folder}">\n'
        card_html += f'      <img src="https://img.shields.io/badge/Source%20Code-181717?style=for-the-badge&logo=github&logoColor=white" alt="Source Code"/>\n'
        card_html += f'    </a>\n'
    
    card_html += '  </p>\n</div>'
    
    return card_html


def generate_readme(agents: List[Dict[str, Any]], root_dir: Path) -> str:
    """Generate the complete README.md content."""
    
    readme_content = f'''# Enterprise AI Agents 🤖

<div align="center">

![AI Agents](https://img.shields.io/badge/AI%20Agents-{len(agents)}-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Last Updated](https://img.shields.io/badge/Last%20Updated-{datetime.now().strftime('%B%20%Y')}-orange?style=for-the-badge)

**Production-ready AI agents for enterprise automation** • Built with modern AI frameworks • Deployed on Streamlit

[Explore Agents](#-ai-agent-showcase) • [Quick Start](#-quick-start) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [All Agents (Quick View)](#-all-agents-quick-view)
- [AI Agent Showcase](#-ai-agent-showcase)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [Contact](#-contact)
- [License](#-license)

---

## 🎯 Overview

This repository is a comprehensive collection of **{len(agents)} production-ready AI agents** designed to solve real-world enterprise problems. Each agent is a fully functional, deployable application built with cutting-edge AI frameworks and best practices.

### Key Highlights

- **Multi-Agent Systems**: Specialized agents working together to solve complex tasks
- **Real-World Applications**: From customer support to competitive analysis
- **Production Ready**: Deployed applications with live demos
- **Modern Stack**: Built with Agno, LangGraph, OpenAI, and more
- **Open Source**: MIT licensed, ready to customize and deploy

### Categories

'''
    
    # Generate category summary
    categories = {}
    for agent in agents:
        cat = agent.get('category', 'Other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(agent)
    
    for category, agent_list in sorted(categories.items()):
        readme_content += f"- **{category}** ({len(agent_list)} agents)\n"
    
    readme_content += "\n---\n\n"
    readme_content += "## 🔍 All Agents (Quick View)\n\n"
    readme_content += "<div align=\"center\">\n\n"
    readme_content += "| # | Agent | Category | Status | Quick Links |\n"
    readme_content += "|---|-------|----------|--------|-------------|\n"
    
    for idx, agent in enumerate(agents, 1):
        name = agent.get('name', 'Unknown')
        emoji = agent.get('emoji', '🤖')
        category = agent.get('category', 'Other')
        deployed_url = agent.get('deployedUrl', '')
        folder = agent.get('folder', '')
        
        # Status badge
        if deployed_url:
            status = "🟢 Live"
        else:
            status = "🔵 Local"
        
        # Quick links
        links = []
        if deployed_url:
            links.append(f"[Demo]({deployed_url})")
        if folder:
            links.append(f"[Docs]({folder}/README.md)")
            links.append(f"[Code]({folder})")
        quick_links = " • ".join(links) if links else "N/A"
        
        readme_content += f"| {idx} | {emoji} **{name}** | {category} | {status} | {quick_links} |\n"
    
    readme_content += "\n</div>\n"
    
    readme_content += "\n---\n\n"
    readme_content += "## 🚀 AI Agent Showcase\n\n"
    readme_content += "<div align=\"center\">\n\n"
    readme_content += "**Click on any card to explore the live demo or dive into the source code!**\n\n"
    readme_content += "</div>\n\n"
    
    # Generate agent cards in a 3-column grid using HTML table
    readme_content += "<table>\n"
    
    for i in range(0, len(agents), 3):
        readme_content += "  <tr>\n"
        
        # Get up to 3 agents for this row
        row_agents = agents[i:i+3]
        
        for agent in row_agents:
            readme_content += "    <td width=\"33%\" valign=\"top\">\n"
            readme_content += generate_agent_card_html(agent, root_dir)
            readme_content += "\n    </td>\n"
        
        # Fill empty cells if row has less than 3 agents
        for _ in range(3 - len(row_agents)):
            readme_content += "    <td width=\"33%\"></td>\n"
        
        readme_content += "  </tr>\n"
    
    readme_content += "</table>\n\n"
    
    readme_content += '''---

## 🏁 Quick Start

### Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- API keys for respective services (OpenAI, OpenRouter, etc.)

### Running an Agent

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bhanuchaddha/enterprise-ai-agents.git
   cd enterprise-ai-agents
   ```

2. **Navigate to an agent directory:**
   ```bash
   cd <agent_folder_name>
   ```

3. **Install dependencies:**
   ```bash
   uv sync  # or: pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file with required API keys (see agent's README for specifics)

5. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 📁 Project Structure

```
enterprise-ai-agents/
├── 1_deep_knowledge_agent/
│   ├── documentation/
│   │   ├── assets/
│   │   │   └── demo.png (or .gif, .jpg, .jpeg)
│   │   └── display-info.json
│   ├── streamlit_app.py
│   ├── README.md
│   └── pyproject.toml
├── 2_airbnb_listing_finder_agent/
│   └── ...
├── common/
│   └── shared utilities
├── generate_readme.py
└── README.md (this file)
```

Each agent directory contains:
- **documentation/**: Agent metadata and demo assets
  - **display-info.json**: Configuration for README generation
  - **assets/demo.png** (or .gif, .jpg, .jpeg): Demo image for showcase
- **streamlit_app.py**: Web UI application
- **README.md**: Detailed agent documentation
- **pyproject.toml**: Python dependencies

---

## 🛠 Technologies Used

This project leverages cutting-edge AI and development tools:

### AI Frameworks
- **Agno**: Multi-agent orchestration framework
- **LangGraph**: Graph-based agent workflows
- **LangChain**: LLM application development

### LLM Providers
- **OpenAI**: GPT-4, GPT-3.5, embeddings
- **OpenRouter**: Multi-model access (Claude, Gemini, Llama, etc.)

### Tools & Services
- **Streamlit**: Interactive web applications
- **LanceDB**: Vector database for embeddings
- **Exa API**: Advanced web search and research
- **MCP (Model Context Protocol)**: Tool integration

### Infrastructure
- **Python 3.9+**: Core programming language
- **uv**: Fast Python package manager
- **SQLite**: Local data persistence

---

## 🤝 Contributing

We welcome contributions! Here's how to add a new agent:

### Adding a New Agent

1. **Create agent directory:**
   ```bash
   mkdir <your_agent_name>
   cd <your_agent_name>
   ```

2. **Create directory structure:**
   ```bash
   mkdir -p documentation/assets
   ```

3. **Add your demo image:**
   - Place your demo image at `documentation/assets/demo.png` (or `.gif`, `.jpg`, `.jpeg`)
   - Supported formats: PNG, GIF, JPG, JPEG
   - Recommended: 800x600 or 1024x768, < 5MB

4. **Create display-info.json:**
   ```bash
   cp ../display-info-schema.json documentation/display-info.json
   ```
   Fill in your agent's details (see schema for required fields)

5. **Implement your agent:**
   - Add your agent code
   - Create `streamlit_app.py` for UI
   - Write detailed `README.md`

6. **Regenerate main README:**
   ```bash
   python generate_readme.py
   ```

7. **Submit a pull request!**

### Contribution Guidelines

- Follow existing code structure and naming conventions
- Include comprehensive documentation
- Add demo GIF or video
- Test your agent thoroughly
- Update display-info.json with accurate information

---

## 👤 Contact

**Bhanu Chaddha**

- LinkedIn: [linkedin.com/in/bhanu-chaddha](https://www.linkedin.com/in/bhanu-chaddha/)
- GitHub: [@bhanuchaddha](https://github.com/bhanuchaddha)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ by [Bhanu Chaddha](https://www.linkedin.com/in/bhanu-chaddha/)

</div>
'''
    
    return readme_content


def main():
    """Main execution function."""
    # Get the repository root directory
    script_dir = Path(__file__).parent
    root_dir = script_dir
    
    print(f"Scanning for agent configurations in: {root_dir}")
    
    # Find all agent configurations
    agents = find_agent_configs(root_dir)
    
    if not agents:
        print("No agent configurations found!")
        return
    
    print(f"Found {len(agents)} active agents:")
    for agent in agents:
        print(f"  - {agent.get('name', 'Unknown')} ({agent.get('folder', 'N/A')})")
    
    # Generate README content
    print("\nGenerating README.md...")
    readme_content = generate_readme(agents, root_dir)
    
    # Write to README.md
    readme_path = root_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\nREADME.md successfully generated at: {readme_path}")
    print(f"Total agents included: {len(agents)}")
    print("\nNext steps:")
    print("1. Add demo images (demo.png, demo.gif, demo.jpg, or demo.jpeg) to each agent's documentation/assets/ directory")
    print("2. Review the generated README.md")
    print("3. Commit your changes")


if __name__ == "__main__":
    main()

