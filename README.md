# RIVO - Flow of Money

## Description

RIVO (Flow of Money) is an AI-powered financial intelligence agent that works as a personal financial analyst.

It allows users to ask questions about stocks, financial markets, companies, economic conditions, and investment-related topics through a conversational interface.

Instead of depending on only one source of information, RIVO follows an agentic AI approach where it understands the question, decides what data is required, collects information from multiple financial sources, and generates a complete analysis.

RIVO combines:

- Global stock market data
- Indian stock market data
- Company financial information
- Market news
- Web-based financial research
- Prediction market insights
- Historical financial documents
- Economic information

The objective is to convert scattered financial information into a structured intelligence report.

---

# How RIVO is Built

RIVO is built using an Agentic AI architecture.

The system does not directly send user questions to an LLM. Instead, the request passes through multiple intelligent stages where different agents perform specific tasks.

Complete architecture:

```text
User Question
      |
      v
Open WebUI Chat Interface
      |
      v
FastAPI Backend Server
      |
      v
LangGraph Agent Workflow
      |
      v
Researcher Agent
      |
      v
Financial Tools + External APIs
      |
      v
Collected Market Context
      |
      v
Critic Analysis Agent
      |
      v
LLM Financial Reasoning
      |
      v
Final Financial Report
      |
      v
User Response
```

---

# Core Components

## FastAPI Backend

FastAPI is the backend communication layer of RIVO.

Responsibilities:

- Handles requests from Open WebUI
- Receives user financial questions
- Sends data into the agent workflow
- Handles communication between UI and AI system
- Returns generated analysis

FastAPI provides a fast asynchronous backend suitable for AI applications.

---

## LangGraph Workflow

LangGraph controls the complete agent execution process.

It manages:

- Agent execution order
- State transfer between agents
- Data flow
- Multi-step reasoning

Workflow:

```text
LangGraph
    |
    v
Researcher Agent
    |
    v
Critic Agent
    |
    v
Final Response
```

---

# Agents

## Researcher Agent

The Researcher Agent is responsible for information gathering.

Main tasks:

- Understands user intent
- Detects financial requirements
- Identifies required market data
- Selects necessary tools
- Collects information from multiple sources
- Creates complete financial context

The Researcher Agent decides what information is needed before generating an answer.

---

## Critic Analysis Agent

The Critic Agent performs final financial reasoning.

Main tasks:

- Receives collected research data
- Studies market information
- Understands positive and negative factors
- Evaluates risks
- Generates structured financial analysis

The Critic Agent transforms raw data into useful financial insights.

---

# Complete Working Flow

Example:

User asks:

```text
"What is the outlook for Apple stock?"
```

Execution:

```text
User enters message
        |
        v
Open WebUI sends request
        |
        v
FastAPI receives request
        |
        v
LangGraph starts workflow
        |
        v
Researcher Agent analyzes requirement
        |
        v
Relevant finance tools are selected
        |
        v
Stock, news and market data collected
        |
        v
Data is combined into context
        |
        v
Critic Agent receives information
        |
        v
LLM performs financial reasoning
        |
        v
Detailed report generated
        |
        v
Response displayed to user
```

---

# Tools and Technologies Used

## FastAPI

High performance Python backend framework.

Used for:

- Backend APIs
- User request handling
- Communication with Open WebUI

---

## Uvicorn

Server used to run FastAPI applications.

Used for:

- Starting backend server
- Handling web requests

---

## LangGraph

Agent workflow framework.

Used for:

- Building agent pipelines
- Managing Researcher and Critic agents
- Maintaining workflow state

---

## LangChain OpenAI

Used for:

- Connecting language models
- Managing AI communication
- OpenAI-compatible model support

---

## Groq API

Used for high-speed LLM inference.

Advantages:

- Faster responses
- Low latency generation
- Efficient AI reasoning

---

## yfinance

Used for:

- Global stock prices
- Indian stock market information
- Company market data

---

## Alpha Vantage

Used for:

- Detailed US market data
- Financial indicators
- Stock information

---

## DuckDuckGo Search

Used for:

- Latest market news
- Online financial information
- Current events

---

## Pandas

Used for:

- Financial data processing
- Data formatting
- Analysis preparation

---

## Pydantic Settings

Used for:

- Configuration management
- Environment handling

---

## Python Dotenv

Used for:

- Loading API keys
- Managing environment variables

---

# Output Generated

RIVO generates a complete financial intelligence report.

Example output structure:

```text
COMPANY STOCK ANALYSIS

Market Overview:
- Current market information
- Stock movement

Technical View:
- Price performance
- Trends

News Analysis:
- Latest events
- Market sentiment

Risk Factors:
- Business risks
- Market risks

Final Outlook:
- Overall view
- Explanation
```

The final answer is generated using combined financial data rather than a single source.

---

# Performance and Latency

RIVO performs multiple steps before generating an answer.

Approximate latency:

```text
Receiving user request
< 0.1 seconds

Intent analysis
0.5 - 1 second

Fetching financial data
1 - 3 seconds

News and web search
1 - 3 seconds

LLM analysis generation
1 - 2 seconds

Response formatting
< 0.1 seconds
```

Average total response:

```text
4 - 8 seconds
```

Latency depends on:

- Number of APIs called
- External API speed
- Internet connection
- LLM response time
- Amount of requested data

---

# Limitations

## API Rate Limits

External financial APIs have usage restrictions.

Possible issues:

- Daily request limits
- API key exhaustion
- Temporary service blocking

When API limits are reached, some live information may not be available.

---

## External Data Dependency

RIVO depends on third-party providers.

Limitations:

- API downtime
- Delayed updates
- Missing information

---

## Financial Prediction Limitations

Market movement cannot be guaranteed.

RIVO provides:

- Research
- Analysis
- Data-driven insights

It does not guarantee future prices.

---

## AI Limitations

LLM quality depends on:

- Input data quality
- Available context
- Model reasoning capability

---

# Future Improvements

## More Market Data Sources

Add:

- Options chain analysis
- Earnings calendars
- Analyst ratings
- Insider trading information
- Institutional investor data

---

## Advanced Quantitative Analysis

Add:

- Stock prediction models
- Portfolio optimization
- Risk scoring models
- Volatility prediction

---

## More Agent System

Future architecture:

```text
User
 |
 v
Research Agent
 |
 v
Risk Analysis Agent
 |
 v
Portfolio Agent
 |
 v
Prediction Agent
 |
 v
Advisor Agent
 |
 v
Final Report
```

---

# Installation and Running Instructions

## 1. Clone Repository

```bash
git clone <repository-url>

cd <project-folder>
```

---

# Backend Setup

Create environment:

```bash
conda create -n finance python=3.12
```

Activate environment:

```bash
conda activate finance
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

Add required API keys:

```env
GROQ_API_KEY=your_api_key

ALPHA_VANTAGE_API_KEY=your_api_key
```

---

# Start Backend Server

Run:

```bash
python -m backend.server
```

or:

```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs on:

```text
http://localhost:8000
```

Keep this terminal running.

---

# Open WebUI Setup

Open another terminal.

Activate environment:

```bash
conda activate finance
```

Install Open WebUI:

```bash
pip install open-webui
```

Start:

```bash
open-webui serve
```

Open:

```text
http://localhost:8080
```

---

# Connect RIVO with Open WebUI

Open WebUI:

```text
Settings

        |
        v

Admin Settings

        |
        v

Connections

        |
        v

Add OpenAI Compatible Connection
```

Base URL:

```text
http://localhost:8000/v1
```

API Key:

```text
Any value
```

Save connection.

Refresh Open WebUI.

Select RIVO model.

---

# Final System Architecture

```text
                 User
                  |
                  v
             Open WebUI
                  |
                  v
            FastAPI Server
                  |
                  v
          LangGraph Workflow
                  |
                  v
          Researcher Agent
                  |
                  v
        Financial Data Tools
                  |
                  v
        Aggregated Market Data
                  |
                  v
        Critic Analysis Agent
                  |
                  v
            LLM Reasoning
                  |
                  v
       Financial Intelligence Report
                  |
                  v
                 User
```

RIVO combines financial data, agent workflows, and AI reasoning to provide intelligent market analysis through a conversational interface.