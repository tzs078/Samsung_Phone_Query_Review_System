# Samsung Phone Query and Review System

An AI-powered Samsung Phone Query and Review System that combines web scraping, PostgreSQL, RAG-based semantic search, an open-source LLM, a multi-agent architecture, and FastAPI.

The system collects Samsung smartphone specifications from GSMArena, stores the data in PostgreSQL, retrieves relevant information using semantic search, generates AI-assisted responses and product reviews, and provides API endpoints for interacting with the system.

---

## Features

* Scrapes Samsung smartphone specifications from GSMArena
* Collects data for 10 Samsung Galaxy smartphones
* Stores scraped data in PostgreSQL
* Uses JSONB for structured specification storage
* Semantic search using Sentence Transformers
* RAG-based question answering
* Open-source LLM using FLAN-T5
* Multi-Agent architecture
* Specification Agent for retrieving phone information
* Review Agent for generating product reviews
* FastAPI REST API
* Interactive Swagger API documentation
* Supports multiple phone-related queries
* Simple frontend interface

---

## System Architecture

```text
GSMArena
    │
    ▼
Web Scraper
    │
    ▼
samsung_phones.json
    │
    ▼
PostgreSQL Database
    │
    ├───────────────┐
    │               │
    ▼               ▼
Specification   RAG Chatbot
   Agent             │
    │                ▼
    │            FLAN-T5 LLM
    │
    ▼
Review Agent
    │
    ▼
Product Review

             ▼
          FastAPI
             │
             ▼
          Frontend
```

---

## Technologies Used

* **Python**
* **BeautifulSoup**
* **Requests**
* **PostgreSQL**
* **psycopg2**
* **Sentence Transformers**
* **FLAN-T5**
* **Hugging Face Transformers**
* **PyTorch**
* **FastAPI**
* **Uvicorn**
* **HTML/CSS/JavaScript**

---

## Samsung Phones Included

The system currently contains 10 Samsung smartphones:

1. Samsung Galaxy S21 5G
2. Samsung Galaxy S22 5G
3. Samsung Galaxy S23
4. Samsung Galaxy S24
5. Samsung Galaxy S25
6. Samsung Galaxy S21 Ultra 5G
7. Samsung Galaxy S22 Ultra 5G
8. Samsung Galaxy S23 Ultra
9. Samsung Galaxy S24 Ultra
10. Samsung Galaxy S25 Ultra

---

# Project Structure

```text
Samsung_Phone_Query_Review_System/
│
├── agent_review.py
├── agent_specs.py
├── api.py
├── chatbot.py
├── database.py
├── llm.py
├── multi_agent.py
├── scraper.py
├── samsung_phones.json
├── requirements.txt
├── README.md
├── .gitignore
│
├── frontend/
│   └── ...
│
└── venv/
```

---

# How the System Works

## 1. Web Scraping

The `scraper.py` file collects Samsung smartphone specifications from GSMArena using:

* Requests
* BeautifulSoup

The scraper extracts information such as:

* Display
* Size
* Resolution
* Camera
* Battery
* Chipset
* CPU
* GPU
* Operating System
* Memory
* Storage
* Price
* Connectivity
* Other available specifications

The collected data is stored in:

```text
samsung_phones.json
```

Run:

```bash
python scraper.py
```

---

# 2. PostgreSQL Database

The scraped phone data is stored in PostgreSQL.

Database name:

```text
samsung_phone_db
```

Main table:

```text
phones
```

The table contains:

* `id`
* `name`
* `url`
* `specifications`

The specifications are stored using PostgreSQL's `JSONB` data type.

Run:

```bash
python database.py
```

Before running the database script, make sure PostgreSQL is installed and the database exists.

---

# 3. RAG Chatbot

The chatbot uses a Retrieval-Augmented Generation approach.

The system first converts the phone information into embeddings using:

```text
all-MiniLM-L6-v2
```

When a user asks a question:

```text
User Query
     ↓
Semantic Search
     ↓
Relevant Phone
     ↓
Relevant Specifications
     ↓
LLM / Factual Response
```

This helps the chatbot retrieve information from the available Samsung phone dataset instead of generating answers only from general model knowledge.

Example queries:

```text
What is the camera of Samsung Galaxy S23?
```

```text
What is the battery capacity of Samsung Galaxy S24?
```

```text
What chipset does Samsung Galaxy S25 use?
```

```text
Tell me about the display of Samsung Galaxy S23 Ultra.
```

Run:

```bash
python chatbot.py
```

---

# 4. Open-Source LLM

The project uses Google's open-source:

```text
google/flan-t5-small
```

The model is loaded using Hugging Face Transformers.

The LLM is used for generating natural-language responses and AI-assisted product reviews.

The model is loaded in:

```text
llm.py
```

---

# 5. Multi-Agent System

The project uses a simple multi-agent architecture with two specialized agents.

## Agent 1 — Specification Agent

File:

```text
agent_specs.py
```

Responsibilities:

* Find the requested Samsung phone
* Retrieve its specifications
* Provide structured phone information

---

## Agent 2 — Review Agent

File:

```text
agent_review.py
```

Responsibilities:

* Receive phone specifications from Agent 1
* Generate an AI-assisted product review
* Use the available specifications as the review context
* Provide a reliable specification-based fallback when necessary

---

## Multi-Agent Workflow

```text
User
 │
 ▼
Specification Agent
 │
 ▼
Phone Specifications
 │
 ▼
Review Agent
 │
 ▼
AI Product Review
```

Run:

```bash
python multi_agent.py
```

Then enter a phone name, for example:

```text
Samsung Galaxy S23
```

To stop the program:

```text
exit
```

---

# 6. FastAPI

The project provides a REST API using FastAPI.

Start the server:

```bash
uvicorn api:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## GET `/`

Checks whether the API is running.

Example response:

```json
{
    "message": "Samsung Phone Query and Review API is running"
}
```

---

## GET `/phones`

Returns all available Samsung phones and their specifications.

---

## POST `/specifications`

Retrieves detailed specifications for a requested Samsung phone.

Example request:

```json
{
    "phone_name": "Samsung Galaxy S23"
}
```

---

## POST `/review`

Generates an AI-assisted product review for a Samsung phone.

Example request:

```json
{
    "phone_name": "Samsung Galaxy S23"
}
```

---

## POST `/chat`

Answers a natural-language question using the RAG chatbot.

Example request:

```json
{
    "query": "What is the camera of Samsung Galaxy S23?"
}
```

Example response:

```json
{
    "success": true,
    "query": "What is the camera of Samsung Galaxy S23?",
    "phone": "Samsung Galaxy S23",
    "answer": "The Samsung Galaxy S23 has a 50 MP..."
}
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/tzs078/Samsung_Phone_Query_Review_System.git
```

Move into the project directory:

```bash
cd Samsung_Phone_Query_Review_System
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create a database named:

```text
samsung_phone_db
```

Configure the PostgreSQL connection according to your local environment.

Do not commit database passwords or other private credentials to GitHub.

---

# Running the Complete Project

## Step 1 — Scrape Data

```bash
python scraper.py
```

This generates:

```text
samsung_phones.json
```

---

## Step 2 — Store Data in PostgreSQL

```bash
python database.py
```

---

## Step 3 — Test the RAG Chatbot

```bash
python chatbot.py
```

---

## Step 4 — Test Multi-Agent System

bash
python multi_agent.py


---

## Step 5 — Start FastAPI

bash
uvicorn api:app --reload

Open:
http://127.0.0.1:8000/docs

---

# Example Questions

The chatbot can handle questions such as:
What is the camera of Samsung Galaxy S23?
What is the battery of Samsung Galaxy S24?
What processor does Samsung Galaxy S25 use?
Tell me about the display of Samsung Galaxy S23 Ultra


What is the price of Samsung Galaxy S24?

The system retrieves relevant information from the collected Samsung phone dataset and generates a response.

---

# Testing

The following components have been tested:

* GSMArena scraping
* JSON data generation
* PostgreSQL data insertion
* Semantic retrieval
* RAG chatbot
* FLAN-T5 model loading
* Specification Agent
* Review Agent
* Multi-Agent workflow
* FastAPI server
* `/phones` endpoint
* `/specifications` endpoint
* `/review` endpoint
* `/chat` endpoint
* Swagger API documentation

---

# Security

Sensitive configuration such as database passwords should be stored using environment variables or a local `.env` file.

The following files should not be committed to GitHub:

.env
venv/
__pycache__/
*.pyc
---

# Future Improvements

Possible future improvements include:

* Add more Samsung phone models
* Add separate database tables for specifications and prices
* Add real-time pricing
* Improve RAG retrieval
* Use a larger open-source LLM
* Add conversation memory
* Improve multi-agent orchestration using CrewAI or LangChain
* Add phone comparison functionality
* Add automated testing
* Improve frontend UI
* Deploy the API to a cloud platform

---

# Project Objectives

The main objectives of this project are:

1. Collect structured Samsung phone data through web scraping.
2. Store the collected information in PostgreSQL.
3. Implement semantic retrieval using embeddings.
4. Build an RAG-based conversational chatbot.
5. Integrate an open-source LLM.
6. Implement a multi-agent workflow.
7. Provide REST API endpoints using FastAPI.
8. Allow users to query Samsung phone specifications and generate product reviews.

---

# Disclaimer

The phone specifications used in this project are collected from GSMArena for educational and project demonstration purposes.

This project is developed as part of a technical assignment and is not affiliated with Samsung Electronics or GSMArena.

---

# Author

**Tasnim Zaman**

CSE Graduate
Bangladesh

GitHub:
https://github.com/tzs078/Samsung_Phone_Query_Review_System
