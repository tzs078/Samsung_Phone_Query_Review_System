from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_specs import SpecificationAgent
from agent_review import ReviewAgent


app = FastAPI(
    title="Samsung Phone Query & Review System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Initialize Agents
# ==========================================

spec_agent = SpecificationAgent()
review_agent = ReviewAgent()


# ==========================================
# Request Model
# ==========================================

class PhoneRequest(BaseModel):
    phone_name: str


# ==========================================
# Home Endpoint
# ==========================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Samsung Phone Query & Review API is running"
    }


# ==========================================
# Specification Endpoint
# ==========================================

@app.post("/specifications")
def get_specifications(request: PhoneRequest):

    phone_data = spec_agent.get_phone_specs(request.phone_name)

    if phone_data is None:
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
# Review Endpoint
# ==========================================

@app.post("/review")
def get_review(request: PhoneRequest):

    phone_data = spec_agent.get_phone_specs(request.phone_name)

    if phone_data is None:
        return {
            "success": False,
            "message": "Phone not found"
        }

    review = review_agent.generate_review(phone_data)

    return {
        "success": True,
        "phone": phone_data["name"],
        "review": review
    }