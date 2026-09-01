const API_URL = "http://127.0.0.1:8000";

const phoneInput = document.getElementById("phoneInput");
const reviewButton = document.getElementById("searchBtn");
const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const resultSection = document.getElementById("resultSection");
const phoneName = document.getElementById("phoneName");
const reviewText = document.getElementById("reviewText");

reviewButton.addEventListener("click", async () => {

const phone = phoneInput.value.trim();

// Check empty input
if (!phone) {
    showError("Please enter a Samsung phone name.");
    return;
}

// Reset previous result
hideError();
resultSection.classList.add("hidden");
loading.classList.remove("hidden");
reviewButton.disabled = true;

try {

    const response = await fetch(`${API_URL}/review`, {
        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },

        body: JSON.stringify({
            phone_name: phone
        })
    });

    if (!response.ok) {
        throw new Error("Server returned an error.");
    }

    const data = await response.json();

    if (!data.success) {
        showError(data.message || "Phone not found.");
        return;
    }

    // Display result
    phoneName.textContent = data.phone;
    reviewText.textContent = data.review;

    resultSection.classList.remove("hidden");

} catch (error) {

    console.error("Error:", error);

    showError(
        "Unable to connect to the server. Make sure FastAPI is running."
    );

} finally {

    loading.classList.add("hidden");
    reviewButton.disabled = false;

}

});

function showError(message) {

errorMessage.textContent = message;
errorMessage.classList.remove("hidden");


}

function hideError() {

errorMessage.textContent = "";
errorMessage.classList.add("hidden");

}

// Press Enter to search
phoneInput.addEventListener("keypress", (event) => {

if (event.key === "Enter") {
    reviewButton.click();
}

});
