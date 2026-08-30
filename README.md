# 📱 Samsung Phone Query & Review System

> An intelligent Samsung smartphone information and review system powered by **Web Scraping, PostgreSQL, RAG, Semantic Search, Multi-Agent Architecture, and FastAPI**.

The **Samsung Phone Query & Review System** is a complete AI-assisted product information platform that collects Samsung smartphone specifications from GSMArena, stores and processes the data, retrieves relevant information using semantic search, and generates structured product reviews through a multi-agent workflow.

The system provides both a **REST API** and a **web-based interface** so users can search for Samsung phones, explore their specifications, and receive AI-assisted product reviews.

---

## ✨ Features

* 🔎 Samsung smartphone specification scraping
* 📱 Supports multiple Samsung Galaxy models
* 🗄️ PostgreSQL database integration
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔤 Semantic search using Sentence Transformers
* 🤖 Multi-Agent architecture
* 📋 Dedicated Specification Agent
* ✍️ Dedicated Review Agent
* ⚡ FastAPI REST API
* 🌐 Interactive web frontend
* 📊 Structured phone specification display
* ⭐ Product review generation
* ❌ User-friendly error handling
* 🔄 Modular and extensible architecture

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      GSMArena       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Web Scraper       │
                         │ Requests + BS4      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   PostgreSQL DB     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   RAG Retrieval     │
                         │ SentenceTransformer │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                ┌─────────────────┐   ┌─────────────────┐
                │ Specification   │   │   Review Agent  │
                │     Agent       │──▶│                 │
                └─────────────────┘   └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │  Product Review │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │    FastAPI      │
                                      │   REST API      │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │  Web Frontend   │
                                      └─────────────────┘
```

---

## 🔄 How It Works

### 1. Data Collection

The scraper collects Samsung smartphone specifications from GSMArena using:

* `Requests`
* `BeautifulSoup4`

The collected data includes:

* Network
* Display
* Resolution
* Processor
* GPU
* RAM & Storage
* Camera
* Selfie Camera
* Battery
* Charging
* Operating System
* Connectivity
* Price
* Dimensions
* Weight
* Other specifications

The collected information is processed and stored for later retrieval.

---

### 2. PostgreSQL Database

The scraped phone information is stored in **PostgreSQL**.

Database storage provides a structured and scalable way to manage the collected smartphone information.

Example database:

```text
Database: samsung_phone_db
```

---

### 3. RAG-Based Retrieval

The system uses **Retrieval-Augmented Generation (RAG)** principles to find the most relevant information for a user's query.

Phone specifications are converted into text representations and encoded into vector embeddings using:

```text
all-MiniLM-L6-v2
```

When a user asks a question, the question is also converted into an embedding.

The system calculates semantic similarity and retrieves the most relevant phone information.

Example:

```text
User:
What is the processor of Samsung Galaxy S24?

        ↓

Semantic Search

        ↓

Samsung Galaxy S24

        ↓

Relevant Processor Information
```

---

## 🤖 Multi-Agent Architecture

The project uses a simple and modular multi-agent workflow.

### Agent 1 — Specification Agent

The Specification Agent is responsible for retrieving the important specifications of the requested Samsung phone.

It focuses on information such as:

* Display
* Processor
* Camera
* Battery
* Charging

Example:

```text
Phone: Samsung Galaxy S23

Display:
6.1 inches

Processor:
Snapdragon 8 Gen 2

Battery:
Active use score 11:27h

Camera:
50 MP + 10 MP Telephoto + 12 MP Ultrawide
```

---

### Agent 2 — Review Agent

The Review Agent receives the relevant specifications from the Specification Agent and generates a structured product review.

The review considers:

* Display quality
* Performance
* Camera capability
* Battery experience
* Charging features

Example:

```text
Overall Review:

The Samsung Galaxy S23 offers a strong overall smartphone
experience with capable performance, a high-quality camera
system, a compact display, and useful charging features.

It is a balanced choice for users looking for performance,
camera quality, and everyday usability.
```

---

## 🔗 Complete Multi-Agent Workflow

```text
User
 │
 ▼
Phone Search
 │
 ▼
Specification Agent
 │
 ├── Display
 ├── Processor
 ├── Camera
 ├── Battery
 └── Charging
 │
 ▼
Review Agent
 │
 ▼
Generated Product Review
```

This architecture keeps the responsibilities of each component separate and makes the system easier to maintain and extend.

---

# 🌐 FastAPI

The backend is built using **FastAPI**.

It exposes the product review functionality through a REST API.

### Start the backend

```bash
uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Swagger API Documentation

FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoint

### Generate Product Review

```http
POST /review
```

### Request

```json
{
    "phone_name": "Samsung Galaxy S23"
}
```

### Response

```json
{
    "success": true,
    "phone": "Samsung Galaxy S23",
    "review": "Product Review..."
}
```

The API connects the multi-agent backend with the frontend application.

---

# 🖥️ Frontend

The frontend provides a simple user-friendly interface where users can:

* Search for Samsung phones
* Select a phone model
* View specifications
* Ask product-related questions
* Generate product reviews
* View review results in a structured format

The frontend communicates with the FastAPI backend through REST API requests.

```text
Frontend
    │
    │ HTTP Request
    ▼
FastAPI
    │
    ▼
Multi-Agent System
    │
    ▼
Review
    │
    ▼
Frontend Display
```

---

# 📂 Project Structure

```text
Samsung_Phone_Query_Review_System/
│
├── scraper.py
│
├── chatbot.py
│
├── agent_specs.py
│
├── agent_review.py
│
├── multi_agent.py
│
├── api.py
│
├── samsung_phones.json
│
├── frontend/
│   ├── ...
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

---

# 🛠️ Technologies Used

| Technology              | Purpose               |
| ----------------------- | --------------------- |
| Python                  | Core development      |
| Requests                | HTTP requests         |
| BeautifulSoup4          | Web scraping          |
| PostgreSQL              | Database              |
| Sentence Transformers   | Text embeddings       |
| all-MiniLM-L6-v2        | Semantic similarity   |
| RAG                     | Information retrieval |
| FastAPI                 | REST API              |
| Uvicorn                 | API server            |
| HTML / CSS / JavaScript | Frontend              |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

```bash
cd Samsung_Phone_Query_Review_System
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install requests beautifulsoup4
pip install sentence-transformers
pip install fastapi uvicorn
```

---

# 🗄️ PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create the database:

```sql
CREATE DATABASE samsung_phone_db;
```

Update the database configuration according to your local PostgreSQL setup.

Example:

```text
Host: localhost
Port: 5432
Database: samsung_phone_db
Username: postgres
Password: your_password
```

> Database credentials should not be committed to GitHub. Use environment variables for sensitive configuration.

---

# 🕷️ Run the Scraper

To collect Samsung phone information:

```bash
python scraper.py
```

The scraper retrieves the selected Samsung phone specifications and prepares them for storage and retrieval.

---

# 🧠 Run the RAG Chatbot

```bash
python chatbot.py
```

Example:

```text
Ask a question about Samsung phones:
What is the camera specification of Samsung Galaxy S23?
```

The system retrieves the relevant information from the collected phone data.

---

# 🤖 Run the Multi-Agent System

```bash
python multi_agent.py
```

Example:

```text
Enter Samsung phone name:
Samsung Galaxy S23
```

The system then executes:

```text
Specification Agent
        ↓
Review Agent
        ↓
Final Product Review
```

---

# 🚀 Run FastAPI

Start the backend:

```bash
uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

You can test the `/review` endpoint directly from Swagger UI.

---

# 💡 Example Queries

The system can handle queries such as:

```text
What is the camera specification of Samsung Galaxy S23?

What is the battery life of Samsung Galaxy S23?

What is the processor of Samsung Galaxy S24?

What is the screen size of Samsung Galaxy S22?

What is the price of Samsung Galaxy S25?

Which processor does Samsung Galaxy S25 Ultra use?
```

---

# 📊 Example Output

```text
================================
Product Review
================================

Phone: Samsung Galaxy S23

Display:
6.1 inches

Performance:
Snapdragon 8 Gen 2

Camera:
50 MP + 10 MP Telephoto + 12 MP Ultrawide

Battery:
Active use score 11:27h

Charging:
25W wired + 15W wireless

Overall Review:
The Samsung Galaxy S23 offers a strong overall
smartphone experience with balanced performance,
camera quality, display and charging features.
```

---

# 🔐 Security

Sensitive information such as:

* Database passwords
* API keys
* Access tokens
* Environment variables

should never be committed to the repository.

A `.gitignore` file should include:

```text
venv/
.env
__pycache__/
*.pyc
```

---

# 🧪 Testing

The system can be tested at different levels:

### Scraper Test

```bash
python scraper.py
```

Verify that phone information is collected successfully.

### RAG Test

```bash
python chatbot.py
```

Test different Samsung phone-related questions.

### Agent Test

```bash
python multi_agent.py
```

Verify that the Specification Agent and Review Agent work together.

### API Test

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

```text
POST /review
```

with different Samsung phone names.

---

# 📈 Future Improvements

The system can be extended with:

* More Samsung smartphone models
* Comparison between multiple phones
* User accounts and saved reviews
* Advanced recommendation system
* Review scoring and rating
* More sophisticated agent collaboration
* Conversation history
* Better natural-language generation
* Automated scheduled data updates
* Cloud deployment
* Production database configuration
* Monitoring and logging

---

# 🎯 Project Objectives

The project demonstrates the practical integration of several modern software and AI concepts:

* Web scraping
* Data processing
* Database management
* Semantic search
* Vector embeddings
* Retrieval-Augmented Generation
* Multi-Agent systems
* REST API development
* Frontend-backend integration

The main objective is to build a practical system that can transform raw smartphone data into useful, searchable and understandable product information.

---

# 📌 Disclaimer

The smartphone specifications used by this project are collected from publicly available online sources. The project is intended for educational, research and demonstration purposes.

---

# 👩‍💻 Author

**Tasnim Zaman**

Computer Science & Engineering

---

## ⭐ Project Highlights

```text
Web Scraping
     +
PostgreSQL
     +
Semantic Search
     +
RAG
     +
Multi-Agent System
     +
FastAPI
     +
Frontend
     =
Samsung Phone Query & Review System
```

⭐ If you find this project useful, consider giving the repository a star.
