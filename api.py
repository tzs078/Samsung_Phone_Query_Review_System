from fastapi import FastAPI
from pydantic import BaseModel

from agent_specs import SpecificationAgent
from agent_review import ReviewAgent


# Create FastAPI app
app = FastAPI(
    title="Samsung Phone Query and Review System",
    description="API for Samsung phone specifications and reviews",
    version="1.0"
)


# Initialize agents
spec_agent = SpecificationAgent()
review_agent = ReviewAgent()


# Request model
class PhoneRequest(BaseModel):
    phone_name: str


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Samsung Phone Query and Review API is running"
    }


# Get phone specifications
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


# Generate phone review
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
        "review": review
    }
