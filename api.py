from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_specs import SpecificationAgent
from agent_review import ReviewAgent
from chatbot import ask_question


app = FastAPI(
    title="Samsung Phone Query and Review System",
    description="AI-powered Samsung phone specification, RAG chatbot and review API",
    version="1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Agents
# ==========================================

spec_agent = SpecificationAgent()
review_agent = ReviewAgent()


# ==========================================
# Request Models
# ==========================================

class PhoneRequest(BaseModel):
    phone_name: str


class ChatRequest(BaseModel):
    query: str


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Samsung Phone Query and Review API is running"
    }


# ==========================================
# Get all phones
# ==========================================

@app.get("/phones")
def get_phones():

    phones = []

    for phone in spec_agent.phones:

        phones.append({
            "name": phone["name"],
            "specifications": phone["specifications"]
        })

    return {
        "success": True,
        "phones": phones
    }


# ==========================================
# Specifications API
# ==========================================

@app.post("/specifications")
def get_specifications(request: PhoneRequest):

    phone_data = spec_agent.get_phone_specs(
        request.phone_name
    )

    if not phone_data:

        return {
            "success": False,
            "message": "Phone not found"
        }

    return {
        "success": True,
        "phone": phone_data["name"],
        "specifications": phone_data["specifications"]
    }


# ==========================================
# Review API
# ==========================================

@app.post("/review")
def get_review(request: PhoneRequest):

    phone_data = spec_agent.get_phone_specs(
        request.phone_name
    )

    if not phone_data:

        return {
            "success": False,
            "message": "Phone not found"
        }

    review = review_agent.generate_review(
        phone_data
    )

    return {
        "success": True,
        "phone": phone_data["name"],
        "specifications": phone_data["specifications"],
        "review": review
    }


# ==========================================
# RAG + LLM Chat API
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    result = ask_question(request.query)

    return {
        "success": True,
        "query": request.query,
        "phone": result["phone"],
        "answer": result["answer"]
    }