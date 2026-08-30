import json


class SpecificationAgent:

    def __init__(self):
        with open("samsung_phones.json", "r", encoding="utf-8") as file:
            self.phones = json.load(file)

    def get_phone_specs(self, phone_name):

        phone_name = phone_name.lower()

        for phone in self.phones:

            if phone_name in phone["name"].lower():

                return {
                    "name": phone["name"],
                    "specifications": phone["specifications"]
                }

        return None


# Test Agent 1
if __name__ == "__main__":

    agent = SpecificationAgent()

    result = agent.get_phone_specs("Samsung Galaxy S23")

    if result:
        print("================================")
        print("Specification Agent")
        print("================================")
        print("Phone:", result["name"])
        print("Chipset:", result["specifications"].get("Chipset"))
        print("Display:", result["specifications"].get("Size"))
        print("Battery:", result["specifications"].get("Battery"))
        print("Camera:", result["specifications"].get("Main Camera"))
    else:
        print("Phone not found.")