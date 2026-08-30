from agent_specs import SpecificationAgent
from agent_review import ReviewAgent


class MultiAgentSystem:

    def __init__(self):
        # Initialize both agents
        self.spec_agent = SpecificationAgent()
        self.review_agent = ReviewAgent()

    def process_phone(self, phone_name):

        print("\n================================")
        print(" Multi-Agent Samsung System")
        print("================================")

        # -----------------------------
        # Agent 1: Specification Agent
        # -----------------------------
        print("\n[Agent 1] Retrieving phone specifications...")

        phone_data = self.spec_agent.get_phone_specs(phone_name)

        if not phone_data:
            print("Phone not found.")
            return

        print(f"[Agent 1] Found: {phone_data['name']}")

        # -----------------------------
        # Agent 2: Review Agent
        # -----------------------------
        print("\n[Agent 2] Generating product review...")

        review = self.review_agent.generate_review(phone_data)

        # -----------------------------
        # Final Result
        # -----------------------------
        print("\n[Final Result]")
        print(review)


# Run Multi-Agent System
if __name__ == "__main__":

    system = MultiAgentSystem()

    while True:

        phone_name = input(
            "\nEnter Samsung phone name (or 'exit'): "
        )

        if phone_name.lower().strip() == "exit":
            print("\nMulti-Agent System stopped.")
            break

        system.process_phone(phone_name)

