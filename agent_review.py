from agent_specs import SpecificationAgent
from llm import generate_text



class ReviewAgent:

    def generate_review(self, phone_data):

        if not phone_data:
            return "Phone information not found."

        phone_name = phone_data["name"]
        specs = phone_data["specifications"]

        display = specs.get("Size", "Not available")
        chipset = specs.get("Chipset", "Not available")
        camera = specs.get("Main Camera", "Not available")
        battery = specs.get("Battery", "Not available")
        charging = specs.get("Charging", "Not available")

        # Reliable specification summary
        return f"""
    ================================
    Product Review
    ================================

    Phone: {phone_name}

    Display:
    {display}

    Performance:
    {chipset}

    Camera:
    {camera}

    Battery:
    {battery}

    Charging:
    {charging}

    Overall Review:
    The {phone_name} offers a balanced smartphone experience based
    on its available specifications. It features a capable chipset,
    a versatile camera system, a quality display, and a substantial
    battery. These specifications make it suitable for everyday use,
    photography, multimedia and general performance.

    ================================
    """

# Test Agent 2
if __name__ == "__main__":

    spec_agent = SpecificationAgent()

    phone_data = spec_agent.get_phone_specs(
        "Samsung Galaxy S23"
    )

    review_agent = ReviewAgent()

    review = review_agent.generate_review(
        phone_data
    )

    print(review)