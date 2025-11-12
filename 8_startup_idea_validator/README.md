# Startup Idea Validator 🚀

An AI-powered validation system that helps entrepreneurs validate their startup ideas through comprehensive analysis including idea clarification, market research, competitive analysis, and strategic recommendations.

## Architecture

The system uses **4 specialized AI agents** working in a sequential validation pipeline:

### 1. 💡 Idea Clarifier Agent
- Evaluates originality of the concept
- Defines clear mission statement
- Sets specific, measurable objectives (SMART goals)
- Provides insights to strengthen the core concept
- **Output**: Structured idea clarification

### 2. 📊 Market Research Agent
- Estimates Total Addressable Market (TAM)
- Calculates Serviceable Available Market (SAM)
- Projects Serviceable Obtainable Market (SOM)
- Defines target customer segments
- Uses Exa for web research and data
- **Output**: Comprehensive market analysis

### 3. 🏢 Competitor Analysis Agent
- Identifies direct and indirect competitors
- Performs SWOT analysis for major players
- Assesses competitive positioning opportunities
- Identifies market gaps
- Uses Exa for competitive intelligence
- **Output**: Competitive landscape report

### 4. 📋 Report Generator Agent
- Synthesizes all research and analysis
- Creates executive summary
- Provides strategic recommendations
- Defines specific next steps
- **Output**: Comprehensive validation report

## Validation Pipeline

```
Startup Idea Input
         ↓
Phase 1: IDEA CLARIFICATION
         ├─→ Evaluate originality
         ├─→ Define mission
         └─→ Set objectives
         ↓
Phase 2: MARKET RESEARCH
         ├─→ Calculate TAM/SAM/SOM
         ├─→ Research with Exa
         └─→ Define target segments
         ↓
Phase 3: COMPETITOR ANALYSIS
         ├─→ Identify competitors
         ├─→ SWOT analysis
         └─→ Positioning assessment
         ↓
Phase 4: VALIDATION REPORT
         ├─→ Executive summary
         ├─→ Strategic recommendations
         └─→ Next steps
         ↓
Comprehensive Validation Report
```

## Features

- **AI-Powered Analysis**: Uses OpenRouter models for intelligent analysis
- **Web Research**: Leverages Exa for current market data and competitor intelligence
- **Comprehensive Reports**: Multi-phase validation with detailed insights
- **Strategic Recommendations**: Actionable advice for entrepreneurs
- **Fallback Parsing**: Robust error handling for free LLM models
- **Interactive UI**: User-friendly Streamlit interface
- **Example Ideas**: Quick-start with pre-loaded examples

## How to Run

1. **Install dependencies**:
   ```bash
   cd 8_startup_idea_validator
   uv pip install -e .
   ```

2. **Set up your environment variables**:
   Create a `.env` file in the root of the project and add your API keys:
   ```
   OPENROUTER_API_KEY="your-openrouter-api-key"
   OPENROUTER_MODEL_ID="minimax/minimax-m2:free"  # Optional, defaults to minimax/minimax-m2:free
   EXA_API_KEY="your-exa-api-key"
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run 8_startup_idea_validator/streamlit_app.py
   ```

4. **Use the interface**:
   - Enter your startup idea description
   - Click "Validate My Idea"
   - Review comprehensive validation report
   - Or use example ideas from the sidebar

## Input Guidelines

### Good Startup Idea Descriptions

Include these elements:
- **Problem**: What problem are you solving?
- **Solution**: How does your product/service solve it?
- **Target Market**: Who are your customers?
- **Unique Value**: What makes you different?

### Example Format

```
A B2B SaaS platform that helps small e-commerce businesses 
optimize their inventory management using AI predictions. 

Target customers: Online retailers with $100K-$5M annual revenue 
who struggle with stockouts and overstock situations.

Unique approach: Real-time demand forecasting with 90%+ accuracy 
using machine learning trained on industry-specific data.
```

## Output

The validation report includes:

### 1. Executive Summary
- High-level assessment
- Key findings
- Go/No-Go recommendation

### 2. Idea Assessment
- Originality evaluation
- Mission statement
- Measurable objectives
- Strengths and weaknesses

### 3. Market Opportunity
- TAM/SAM/SOM estimates
- Target customer segments
- Market size and growth potential
- Industry trends

### 4. Competitive Landscape
- Direct and indirect competitors
- SWOT analysis
- Competitive positioning
- Market gaps and opportunities

### 5. Strategic Recommendations
- 3-5 specific actionable recommendations
- Risk mitigation strategies
- Differentiation opportunities
- Resource requirements

### 6. Next Steps
- Specific action items
- Validation experiments
- Milestone suggestions
- Resource recommendations

## Use Cases

### For Entrepreneurs
- Validate ideas before investing resources
- Understand market opportunity
- Identify competitive advantages
- Get objective feedback

### For Product Managers
- Assess new product opportunities
- Conduct market research
- Analyze competitive positioning
- Support business cases

### For Investors
- Initial startup screening
- Market opportunity assessment
- Competitive analysis
- Due diligence support

### For Innovation Teams
- Evaluate new initiatives
- Market validation
- Strategic planning
- Risk assessment

## Models Used

- **OpenRouter**: For flexible LLM access
  - Default: `minimax/minimax-m2:free`
  - Configurable via `OPENROUTER_MODEL_ID`
  - Supports any OpenRouter-compatible model

- **Exa**: For intelligent web search
  - Market data research
  - Competitor intelligence
  - Industry trends
  - Real-time information

## Fallback Handling

The system includes robust fallback parsing for when free LLM models don't return properly structured JSON:

- Text pattern extraction for key information
- Graceful degradation
- Always returns results
- Detailed error logging

## Dependencies

- `agno>=2.2.6` - Agent framework
- `openrouter>=0.1.0` - LLM model provider
- `python-dotenv>=1.0.0` - Environment variable management
- `streamlit>=1.28.0` - Web UI framework
- `exa-py>=2.0.0` - Web search tool

## Notes

- Validation takes 2-5 minutes depending on complexity
- Uses web search for current market data
- Results are for informational purposes only
- Conduct additional due diligence before major decisions
- Free models may have limitations on structured output
- Consider upgrading to paid models for better results

## Disclaimer

This validation tool provides analysis based on AI research and should not be the sole basis for business decisions. Always conduct thorough market research, customer validation, and due diligence before launching a startup or making significant investments.

