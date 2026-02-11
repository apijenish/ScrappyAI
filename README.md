# Scrappy Market: Agentic AI System

**Version 1.0** | February 10th, 2026

An intelligent, multi-agent AI system that empowers non-technical business leaders to query sales databases using natural language. Built for Cycle Craft Georgia to bridge the gap between business insights and data analysis.

---

## Table of Contents

- About Cycle Craft Georgia
- Business Challenges
- System Overview
- Features
- Architecture
- Installation
- Usage
- Technical Requirements
- Project Timeine
- Testing
- Future Enhancements

---

## About Cycle Craft Georgia
Cycle Craft Georgia is the premier, locally-owned bicycle retailer with multiple locations across Georgia, including flagship stores in Atlanta, Savannah, and Athens. We offer:

- High-quality bicycles for all disciplines and skill levels
- Expert repairs and custom bike fittings
- Comprehensive parts, accessories, and apparel
- Full-service cycling hub serving the entire Georgia cycling community
  
### Our Story 
Founded in 2008 by **Sarah Chen**, a former competitive cyclist, Cycle Craft Georgia started as a small brick-and-mortar shop in Roswell. The mission was simple: provide Georgians with the best-quality bikes and the knowledge to make cycling a core part of their lives.

Today, Cycle Craft Georgia operates multiple locations, each acting as a local gathering place for cyclists from historic Savannah to bustling Atlanta and the rolling hills of Athens.

## Business Challenge

### The Problem
Cycle Craft Georgia operates multiple stores, each with unique market dynamics. Regional managers need timely sales data to make strategic decisions, but they:

- Are not data analysts
- Lack technical skills to query databases directly
- Must submit requests to a small IT department
- Experience delays of several days for data analysis
- Miss opportunities due to slow, reactive data access

### Solution: Scrappy Market Agentic AI System
An intelligent system that translates natural-language business questions into SQL queries, automating the manual inspection of database tables and putting data insights directly into the hands of decision-makers.

### Use Case Scenario
A regional manager overseeing multiple stores needs to plan inventory and marketing for the ipdcoming quarter. Instead of emailing IT, the regional manager can log into the Scrappy Market system and ask: 
- **"Show me the total sales revenue for e-bikes at the Atlanta, Athens, and Savannah stores over the last 90 days."**

---

## System Overview 
The Scrappy Market Agentic AI System is a multi-agent framework that:

1. **Translates natural-language questions** into structured workflows
2. **Generates SQL queries** automatically based on database schema
3. **Executes queries** against the MySQL database
4. **Explains reasoning paths** so users understand how answers were derived
5. **Presents results** in intuitive formats (tables, charts, visualizations)

---

## Features 
### Core Capabilities
** Natural Lanaguage Processing**
- Accept business questions in plain English
- Interpre user intent and identify key metrics
- Maintain conversational context for follow-up questions
- Handle various phrasing and question formats

**Multi-Agent Orchestration**
- Inten Agent to analyzes requests and structures intent data
- Query Builder Agent to generates valid SQL queries from inten
- Structured communication via LangGraph
- Clear workflow management and error handling

**SQL Query Generation**
- Support for complex queries (joins, aggregations, subqueries)
- Syntax error prevention

**Database Integration**
- Secure MySQL database connection
- Real-time query execution
- Comprehensive error handling

**Reasoning Path**
- Transparent display of AI reasoning
- Step-by-step explanation of query generation
- Formatted SQL query display
- User-friendly interpretation of system logic

**Intuitive User Interface**
- Streamlit-based we interface
- Tabular results display with visualizations
- Session-based query history
- Clear error messaging
 
 ---

## Architecture
  
### Technology Stack

  - **Backend**: Python
  - **Agent Framework**: LangGraph
  - **Frontend**: Streamlit
  - **Database**: MySQL
  - **Version Control**: Github
 
---

## Installation

### Prerequisites
- Python 3.9 or higher
- MySQL 5.7 or higher
- Git
- pip (Python package manager)

### Quick Start

---

## Usage

### Starting a Query Session

---

## Technical Requirements

### Functional Requirements 
- Natural language input processing
- Intent recogniion and classification
- Multi-agent orchestration with LangGraph
- SQL Query generation with schema awareness
- MySQL database integration
- Reasoning path explanation and transparency
- Query results validation and accuracy
- Edge case handling

### Security 
- Database credentials stored in environment variables
- SQL queries restricted to SELECT statements only
- No INSERT, UPDATE, DELETE, or DROP operations permitted
- Query validation before execution

---

## Project Timeline 

### Milestone Schedule

| Milestone | Data | Deliverables |
| ** Milestone 1** | February 17, 2026| Requirements and design documentation |
| **Milestone 2** | March 17, 2026 | Core agent development and integration |
| **Milestone 3** | April 14, 2026 | Full system integraion and final documentation |

### Team Structure 
- 1 Project Manager
- 4 Development Engineers
- Bi-weekly mentor meeting for guidance
- Weekly team meeting

---

## Testing 

### Running Test

---

## Future Enhancements
We have the following features planned for future releases:
- **Query Optimization Agent** to improve SQL query performance
- **Data Visualization Agent** to automate chart and graph generation
- **User Authentixation** through role-based access control
- **Export Functionality** to options such as CSV, Excel, and PDF
- **Natural Language Insights** with auomated summaries and recommendations
- **Real-Time Data Integration** with live data source connections
- **Machine Learning** by learning from query patterns to improve accuracy
- **Scheduled Reports** by auomating query execution and email delivery
- **Mobile Interface** by developing a responsive design for tablets and phones
