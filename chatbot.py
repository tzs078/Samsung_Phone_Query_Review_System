import json
from sentence_transformers import SentenceTransformer, util
from llm import generate_text


# ==========================================
# Load Samsung phone data
# ==========================================

with open("samsung_phones.json", "r", encoding="utf-8") as file:
    phones = json.load(file)


# ==========================================
# RAG Embedding Model
# ==========================================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================
# Create searchable documents
# ==========================================

documents = []

for phone in phones:

    text = f"Phone: {phone['name']}\n"

    for key, value in phone["specifications"].items():
        text += f"{key}: {value}\n"

    documents.append(text)


document_embeddings = embedding_model.encode(
    documents,
    convert_to_tensor=True
)


# ==========================================
# Retrieve relevant specifications
# ==========================================

def get_relevant_info(phone_data, question):

    specs = phone_data["specifications"]
    question_lower = question.lower()

    if any(word in question_lower for word in [
        "camera", "photo", "rear camera", "main camera"
    ]):
        keys = ["Main Camera", "Selfie camera"]

    elif any(word in question_lower for word in [
        "battery", "charging", "charge"
    ]):
        keys = ["Battery", "Battery (old)", "Charging"]

    elif any(word in question_lower for word in [
        "display", "screen", "resolution", "size"
    ]):
        keys = ["Display", "Size", "Resolution", "Protection"]

    elif any(word in question_lower for word in [
        "processor", "cpu", "performance", "chipset", "gpu"
    ]):
        keys = ["Chipset", "CPU", "GPU", "Our Tests"]

    elif any(word in question_lower for word in [
        "price", "cost", "expensive", "cheap"
    ]):
        keys = ["Price", "128GB 8GB RAM", "256GB 8GB RAM"]

    elif any(word in question_lower for word in [
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

    return [
        (key, specs[key])
        for key in keys
        if key in specs
    ]


# ==========================================
# LLM Answer Generation
# ==========================================
def generate_llm_answer(phone_name, question, relevant_info):

    question_lower = question.lower()

    # Exact factual retrieval
    for key, value in relevant_info:

        if "camera" in question_lower and key == "Main Camera":
            return f"The {phone_name} has a {value}."

        if "selfie" in question_lower and key == "Selfie camera":
            return f"The {phone_name} has a {value}."

        if "battery" in question_lower and key == "Battery":
            return f"The {phone_name} has a {value}."

        if "display" in question_lower and key in ["Display", "Size"]:
            return f"The {phone_name} has a {value}."

        if any(word in question_lower for word in ["processor", "chipset", "cpu"]) and key == "Chipset":
            return f"The {phone_name} uses {value}."

    # LLM for general questions
    context = "\n".join(
        f"{key}: {value}"
        for key, value in relevant_info
    )

    prompt = f"""
Answer using only these specifications.

Phone: {phone_name}

Specifications:
{context}

Question: {question}

Answer:
"""

    return generate_text(prompt, max_new_tokens=80)



# ==========================================
# Chatbot
# ==========================================

def ask_question(question):

    question_embedding = embedding_model.encode(
        question,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        question_embedding,
        document_embeddings
    )[0]

    best_index = scores.argmax().item()

    phone_data = phones[best_index]

    relevant_info = get_relevant_info(
        phone_data,
        question
    )

    if not relevant_info:
        return {
            "phone": phone_data["name"],
            "answer": "Sorry, relevant information was not found."
        }

    answer = generate_llm_answer(
        phone_data["name"],
        question,
        relevant_info
    )

    return {
        "phone": phone_data["name"],
        "answer": answer
    }


# ==========================================
# Run chatbot
# ==========================================

if __name__ == "__main__":

    print("================================")
    print(" Samsung Phone RAG + LLM Chatbot")
    print("================================")
    print("RAG + FLAN-T5 LLM ready!")
    print("Type 'exit' to stop.\n")

    while True:

        question = input(
            "Ask a question about Samsung phones: "
        )

        if question.lower().strip() == "exit":
            print("Goodbye!")
            break

        result = ask_question(question)

        print("\n--------------------------------")
        print(f"{result['phone']}:")
        print(result["answer"])
        print("--------------------------------\n")