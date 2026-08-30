import json
from sentence_transformers import SentenceTransformer, util

# Load phone data
with open("samsung_phones.json", "r", encoding="utf-8") as file:
    phones = json.load(file)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create searchable documents
documents = []

for phone in phones:
    text = f"Phone: {phone['name']}\n"

    for key, value in phone["specifications"].items():
        text += f"{key}: {value}\n"

    documents.append(text)

# Create embeddings
document_embeddings = model.encode(
    documents,
    convert_to_tensor=True
)

print("================================")
print(" Samsung Phone RAG Chatbot")
print("================================")
print("RAG system ready!")
print("Type 'exit' to stop.\n")


def get_relevant_info(phone_data, question):
    """Select relevant specifications based on the question."""

    specs = phone_data["specifications"]
    question = question.lower()

    if any(word in question for word in [
        "camera", "photo", "rear camera", "main camera"
    ]):
        keys = ["Main Camera", "Selfie camera", "Video"]

    elif any(word in question for word in [
        "battery", "charging", "charge"
    ]):
        keys = ["Battery", "Battery (old)", "Charging"]

    elif any(word in question for word in [
        "display", "screen", "resolution", "size"
    ]):
        keys = ["Display", "Size", "Resolution", "Protection"]

    elif any(word in question for word in [
        "processor", "cpu", "performance", "chipset", "gpu"
    ]):
        keys = ["Chipset", "CPU", "GPU", "Our Tests"]

    elif any(word in question for word in [
        "price", "cost", "expensive", "cheap"
    ]):
        keys = ["Price", "128GB 8GB RAM", "256GB 8GB RAM"]

    elif any(word in question for word in [
        "android", "software", "one ui", "os"
    ]):
        keys = ["Platform"]

    else:
        keys = [
            "Display",
            "Chipset",
            "Main Camera",
            "Battery",
            "Price"
        ]

    result = []

    for key in keys:
        if key in specs:
            result.append((key, specs[key]))

    return result


def generate_answer(phone_name, question, relevant_info):
    """Generate a clean answer from retrieved specifications."""

    question = question.lower()

    # Camera answer
    if any(word in question for word in [
        "camera", "photo", "rear camera"
    ]):

        answer = f"\n{phone_name} Camera:\n"

        for key, value in relevant_info:

            if key == "Main Camera":
                answer += f"• Rear Camera: {value}\n"

            elif key == "Selfie camera":
                answer += f"• Selfie Camera: {value}\n"

            elif key == "Video":
                answer += f"• Video: {value}\n"

        return answer

    # Battery answer
    elif any(word in question for word in [
        "battery", "charging", "charge"
    ]):

        answer = f"\n{phone_name} Battery:\n"

        for key, value in relevant_info:
            answer += f"• {key}: {value}\n"

        return answer

    # Display answer
    elif any(word in question for word in [
        "display", "screen", "resolution", "size"
    ]):

        answer = f"\n{phone_name} Display:\n"

        for key, value in relevant_info:
            answer += f"• {key}: {value}\n"

        return answer

    # Performance answer
    elif any(word in question for word in [
        "processor", "cpu", "performance", "chipset", "gpu"
    ]):

        answer = f"\n{phone_name} Performance:\n"

        for key, value in relevant_info:
            answer += f"• {key}: {value}\n"

        return answer

    # Price answer
    elif any(word in question for word in [
        "price", "cost", "expensive", "cheap"
    ]):

        answer = f"\n{phone_name} Pricing:\n"

        for key, value in relevant_info:
            answer += f"• {key}: {value}\n"

        return answer

    # General answer
    else:

        answer = f"\n{phone_name} Information:\n"

        for key, value in relevant_info:
            answer += f"• {key}: {value}\n"

        return answer


# Chat loop
while True:

    question = input("Ask a question about Samsung phones: ")

    if question.lower().strip() == "exit":
        print("Goodbye!")
        break

    # Convert question into embedding
    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    # Find most relevant phone
    scores = util.cos_sim(
        question_embedding,
        document_embeddings
    )[0]

    best_index = scores.argmax().item()

    phone_data = phones[best_index]
    phone_name = phone_data["name"]

    # Get relevant specifications
    relevant_info = get_relevant_info(
        phone_data,
        question
    )

    print("\n--------------------------------")

    if relevant_info:
        answer = generate_answer(
            phone_name,
            question,
            relevant_info
        )

        print(answer)

    else:
        print("\nSorry, I could not find relevant information.")

    print("--------------------------------\n")

