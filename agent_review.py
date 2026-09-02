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

        # Prepare accurate specification context for the LLM
        context = f"""
Phone: {phone_name}

Display: {display}
Chipset: {chipset}
Main Camera: {camera}
Battery: {battery}
Charging: {charging}
"""

        prompt = f"""
Write a short and professional smartphone product review.

Use ONLY the specifications provided below.
Do not invent any specifications.
Do not change any numbers or technical details.

{context}

Write the review in this format:

Display:
Performance:
Camera:
Battery:
Charging:
Overall Review:

Keep the review concise and factual.
"""

        try:
            llm_review = generate_text(
                prompt,
                max_new_tokens=180
            ).strip()

            # Basic validation to avoid obviously bad LLM output
            if (
                llm_review
                and len(llm_review) > 80
                and phone_name.lower() not in llm_review.lower()
            ):
                return f"""
================================
AI Product Review
================================

Phone: {phone_name}

{llm_review}

================================
"""

        except Exception as e:
            print(f"LLM review generation failed: {e}")

        # Reliable fallback if the LLM produces poor output
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
