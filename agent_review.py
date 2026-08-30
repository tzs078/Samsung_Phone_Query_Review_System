from agent_specs import SpecificationAgent


class ReviewAgent:

    def generate_review(self, phone_data):

        if not phone_data:
            return "Phone information not found."

        phone_name = phone_data["name"]
        specs = phone_data["specifications"]

        chipset = specs.get("Chipset", "Not available")
        display = specs.get("Size", "Not available")
        battery = specs.get("Battery", "Not available")
        camera = specs.get("Main Camera", "Not available")
        charging = specs.get("Charging", "Not available")

        review = f"""
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
The {phone_name} offers a strong overall smartphone experience.
It has a capable processor, a high-quality camera system,
a good display, and useful charging features.

Based on the available specifications, it is a good choice
for users who want balanced performance, camera quality,
and everyday usability.

================================
"""

        return review


# Test Agent 2
if __name__ == "__main__":

    # Agent 1
    spec_agent = SpecificationAgent()

    # Get phone information
    phone_data = spec_agent.get_phone_specs("Samsung Galaxy S23")

    # Agent 2
    review_agent = ReviewAgent()

    # Generate review
    review = review_agent.generate_review(phone_data)

    print(review)