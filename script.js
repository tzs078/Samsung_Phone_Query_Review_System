const API_URL = "http://127.0.0.1:8000";

// ==============================
// DOM Elements
// ==============================

const phoneInput = document.getElementById("phoneInput");
const searchBtn = document.getElementById("searchBtn");
const suggestions = document.getElementById("suggestions");
const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const resultSection = document.getElementById("resultSection");

const phoneName = document.getElementById("phoneName");
const displaySpec = document.getElementById("displaySpec");
const performanceSpec = document.getElementById("performanceSpec");
const cameraSpec = document.getElementById("cameraSpec");
const batterySpec = document.getElementById("batterySpec");
const chargingSpec = document.getElementById("chargingSpec");
const reviewText = document.getElementById("reviewText");

// ==============================
// Comparison DOM Elements
// ==============================

const phone1Select = document.getElementById("phone1Select");
const phone2Select = document.getElementById("phone2Select");
const compareBtn = document.getElementById("compareBtn");
const compareResult = document.getElementById("compareResult");

const comparisonVerdict =
    document.getElementById("comparisonVerdict");

const winnerPhone =
    document.getElementById("winnerPhone");

const verdictText =
    document.getElementById("verdictText");

// ==============================
// Variables
// ==============================

let phoneList = [];
let phoneDataList = [];
let filteredPhones = [];
let activeSuggestionIndex = -1;

// ==============================
// Load Phones
// ==============================

async function loadPhones() {

    try {

        const response =
            await fetch(`${API_URL}/phones`);

        if (!response.ok) {
            throw new Error("Unable to load phone list.");
        }

        const data =
            await response.json();

        if (data.success) {

            phoneDataList = data.phones;

            phoneList =
                data.phones.map(phone => phone.name);

            loadComparePhones();
        }

    } catch (error) {

        console.error(
            "Phone list error:",
            error
        );
    }
}

// Load phone list when page opens
loadPhones();

// ==============================
// Normalize Search Text
// ==============================

function normalizeText(text) {

    return text
        .toLowerCase()
        .replace(/samsung/g, "")
        .replace(/galaxy/g, "")
        .replace(/\s+/g, " ")
        .trim();
}

// ==============================
// Smart Search
// ==============================

function getSmartMatches(query) {

    const normalizedQuery =
        normalizeText(query);

    if (!normalizedQuery) {
        return [];
    }

    const queryWords =
        normalizedQuery.split(" ");

    const matches =
        phoneList
            .map(phone => {

                const normalizedPhone =
                    normalizeText(phone);

                let score = 0;

                if (
                    normalizedPhone ===
                    normalizedQuery
                ) {
                    score += 100;
                }

                if (
                    normalizedPhone.startsWith(
                        normalizedQuery
                    )
                ) {
                    score += 50;
                }

                if (
                    normalizedPhone.includes(
                        normalizedQuery
                    )
                ) {
                    score += 30;
                }

                queryWords.forEach(word => {

                    if (
                        normalizedPhone.includes(word)
                    ) {
                        score += 10;
                    }
                });

                return {
                    phone,
                    score
                };
            })
            .filter(item => item.score > 0)
            .sort(
                (a, b) =>
                    b.score - a.score
            );

    return matches
        .slice(0, 5)
        .map(item => item.phone);
}

// ==============================
// Highlight Matching Text
// ==============================

function highlightMatch(phone, query) {

    if (!query) {
        return phone;
    }

    const escapedQuery =
        query.replace(
            /[.*+?^${}()|[\]\\]/g,
            "\\$&"
        );

    const regex =
        new RegExp(
            `(${escapedQuery})`,
            "gi"
        );

    return phone.replace(
        regex,
        "<strong>$1</strong>"
    );
}

// ==============================
// Show Suggestions
// ==============================

function showSuggestions() {

    const query =
        phoneInput.value.trim();

    suggestions.innerHTML = "";

    activeSuggestionIndex = -1;

    if (!query) {

        suggestions.classList.add(
            "hidden"
        );

        return;
    }

    filteredPhones =
        getSmartMatches(query);

    if (
        filteredPhones.length === 0
    ) {

        suggestions.classList.add(
            "hidden"
        );

        return;
    }

    filteredPhones.forEach(
        (phone, index) => {

            const item =
                document.createElement("div");

            item.classList.add(
                "suggestion-item"
            );

            item.dataset.index = index;

            item.innerHTML =
                highlightMatch(
                    phone,
                    query
                );

            item.addEventListener(
                "mousedown",
                function (event) {

                    event.preventDefault();

                    selectSuggestion(index);
                }
            );

            suggestions.appendChild(item);
        }
    );

    suggestions.classList.remove(
        "hidden"
    );
}

// ==============================
// Select Suggestion
// ==============================

function selectSuggestion(index) {

    if (
        index < 0 ||
        index >= filteredPhones.length
    ) {
        return;
    }

    phoneInput.value =
        filteredPhones[index];

    suggestions.classList.add(
        "hidden"
    );

    activeSuggestionIndex = -1;
}

// ==============================
// Active Suggestion
// ==============================

function updateActiveSuggestion() {

    const items =
        suggestions.querySelectorAll(
            ".suggestion-item"
        );

    items.forEach(item => {

        item.classList.remove(
            "active"
        );
    });

    if (
        activeSuggestionIndex >= 0 &&
        activeSuggestionIndex < items.length
    ) {

        items[
            activeSuggestionIndex
        ].classList.add("active");

        items[
            activeSuggestionIndex
        ].scrollIntoView({
            block: "nearest"
        });
    }
}

// ==============================
// Input Event
// ==============================

phoneInput.addEventListener(
    "input",
    showSuggestions
);

// ==============================
// Keyboard Navigation
// ==============================

phoneInput.addEventListener(
    "keydown",
    function (event) {

        if (
            suggestions.classList.contains(
                "hidden"
            ) ||
            filteredPhones.length === 0
        ) {
            return;
        }

        if (
            event.key === "ArrowDown"
        ) {

            event.preventDefault();

            activeSuggestionIndex++;

            if (
                activeSuggestionIndex >=
                filteredPhones.length
            ) {
                activeSuggestionIndex = 0;
            }

            updateActiveSuggestion();
        }

        else if (
            event.key === "ArrowUp"
        ) {

            event.preventDefault();

            activeSuggestionIndex--;

            if (
                activeSuggestionIndex < 0
            ) {

                activeSuggestionIndex =
                    filteredPhones.length - 1;
            }

            updateActiveSuggestion();
        }

        else if (
            event.key === "Enter"
        ) {

            if (
                activeSuggestionIndex >= 0
            ) {

                event.preventDefault();

                selectSuggestion(
                    activeSuggestionIndex
                );

                return;
            }

            searchPhone();
        }

        else if (
            event.key === "Escape"
        ) {

            suggestions.classList.add(
                "hidden"
            );

            activeSuggestionIndex = -1;
        }
    }
);

// ==============================
// Search Phone
// ==============================

async function searchPhone() {

    const phone =
        phoneInput.value.trim();

    if (!phone) {

        showError(
            "Please enter a Samsung phone name."
        );

        return;
    }

    suggestions.classList.add(
        "hidden"
    );

    resultSection.classList.add(
        "hidden"
    );

    errorMessage.classList.add(
        "hidden"
    );

    loading.classList.remove(
        "hidden"
    );

    searchBtn.disabled = true;

    searchBtn.innerHTML =
        "Analyzing...";

    try {

        const response =
            await fetch(
                `${API_URL}/review`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        phone_name: phone
                    })
                }
            );

        if (!response.ok) {
            throw new Error(
                "Server error"
            );
        }

        const data =
            await response.json();

        if (!data.success) {

            showError(
                data.message ||
                "Phone not found."
            );

            return;
        }

        // Phone Name

        phoneName.textContent =
            data.phone;

        document.getElementById(
            "phoneSubtitle"
        ).textContent =
            "AI-powered specification and product analysis";

        // Specifications

        const specs =
            data.specifications || {};

        displaySpec.textContent =
            specs.display ||
            specs.Display ||
            specs.Size ||
            "Information not available.";

        performanceSpec.textContent =
            specs.chipset ||
            specs.Chipset ||
            "Information not available.";

        cameraSpec.textContent =
            specs.camera ||
            specs.Camera ||
            specs["Main Camera"] ||
            "Information not available.";

        batterySpec.textContent =
            specs.battery ||
            specs.Battery ||
            "Information not available.";

        chargingSpec.textContent =
            specs.charging ||
            specs.Charging ||
            "Information not available.";

        // AI Review

        reviewText.textContent =
            data.review ||
            "Review not available.";

        resultSection.classList.remove(
            "hidden"
        );

    }

    catch (error) {

        console.error(error);

        showError(
            "Unable to connect to the server. Make sure FastAPI is running."
        );

    }

    finally {

        loading.classList.add(
            "hidden"
        );

        searchBtn.disabled = false;

        searchBtn.innerHTML =
            "🔍 Get Review";
    }
}

// ==============================
// Error
// ==============================

function showError(message) {

    errorMessage.classList.remove(
        "hidden"
    );

    const paragraph =
        errorMessage.querySelector("p");

    if (paragraph) {
        paragraph.textContent =
            message;
    }

    resultSection.classList.add(
        "hidden"
    );

    loading.classList.add(
        "hidden"
    );
}

// ==============================
// Search Button
// ==============================

searchBtn.addEventListener(
    "click",
    searchPhone
);

// ==============================
// Click Outside
// ==============================

document.addEventListener(
    "click",
    function (event) {

        if (
            !phoneInput.contains(
                event.target
            ) &&
            !suggestions.contains(
                event.target
            )
        ) {

            suggestions.classList.add(
                "hidden"
            );

            activeSuggestionIndex = -1;
        }
    }
);

// =====================================================
// PHONE COMPARISON
// =====================================================

// ==============================
// Load Comparison Phones
// ==============================

function loadComparePhones() {

    phone1Select.innerHTML =
        '<option value="">Select first phone</option>';

    phone2Select.innerHTML =
        '<option value="">Select second phone</option>';

    phoneDataList.forEach(phone => {

        const option1 =
            document.createElement(
                "option"
            );

        option1.value =
            phone.name;

        option1.textContent =
            phone.name;

        const option2 =
            document.createElement(
                "option"
            );

        option2.value =
            phone.name;

        option2.textContent =
            phone.name;

        phone1Select.appendChild(
            option1
        );

        phone2Select.appendChild(
            option2
        );
    });
}

// ==============================
// Get Comparison Value
// ==============================

function getCompareValue(
    phone,
    key
) {

    return (
        phone.specifications[key] ||
        "Information not available."
    );
}

// ==============================
// AI Comparison Verdict
// ==============================

function generateComparisonVerdict(
    phone1,
    phone2
) {

    const specs1 =
        phone1.specifications;

    const specs2 =
        phone2.specifications;

    let score1 = 0;
    let score2 = 0;

    let advantages1 = [];
    let advantages2 = [];

    // ==============================
    // Display
    // ==============================

    const size1 =
        parseFloat(
            specs1["Size"] || ""
        );

    const size2 =
        parseFloat(
            specs2["Size"] || ""
        );

    if (
        !isNaN(size1) &&
        !isNaN(size2)
    ) {

        if (size1 > size2) {

            score1++;

            advantages1.push(
                "larger display"
            );

        }

        else if (size2 > size1) {

            score2++;

            advantages2.push(
                "larger display"
            );
        }
    }

    // ==============================
    // Performance
    // ==============================

    const chipset1 =
        specs1["Chipset"] || "";

    const chipset2 =
        specs2["Chipset"] || "";

    const chipsetRanking = [

        "Snapdragon 8 Gen 3",

        "Snapdragon 8 Gen 2",

        "Snapdragon 8 Gen 1",

        "Snapdragon 888",

        "Snapdragon 865",

        "Exynos 2400",

        "Exynos 2200",

        "Exynos 2100"
    ];

    let rank1 = 0;
    let rank2 = 0;

    chipsetRanking.forEach(
        (chip, index) => {

            if (
                chipset1.includes(chip)
            ) {

                rank1 =
                    chipsetRanking.length -
                    index;
            }

            if (
                chipset2.includes(chip)
            ) {

                rank2 =
                    chipsetRanking.length -
                    index;
            }
        }
    );

    if (rank1 > rank2) {

        score1++;

        advantages1.push(
            "better chipset"
        );

    }

    else if (rank2 > rank1) {

        score2++;

        advantages2.push(
            "better chipset"
        );
    }

    // ==============================
    // Camera
    // ==============================

    const camera1 =
        specs1["Main Camera"] || "";

    const camera2 =
        specs2["Main Camera"] || "";

    const mp1 =
        parseFloat(camera1);

    const mp2 =
        parseFloat(camera2);

    if (
        !isNaN(mp1) &&
        !isNaN(mp2)
    ) {

        if (mp1 > mp2) {

            score1++;

            advantages1.push(
                "higher-resolution camera"
            );

        }

        else if (mp2 > mp1) {

            score2++;

            advantages2.push(
                "higher-resolution camera"
            );
        }
    }

    // ==============================
    // Battery
    // ==============================

    const battery1 =
        specs1["Battery"] || "";

    const battery2 =
        specs2["Battery"] || "";

    const batteryValue1 =
        parseInt(
            battery1.replace(
                /,/g,
                ""
            )
        );

    const batteryValue2 =
        parseInt(
            battery2.replace(
                /,/g,
                ""
            )
        );

    if (
        !isNaN(batteryValue1) &&
        !isNaN(batteryValue2)
    ) {

        if (
            batteryValue1 >
            batteryValue2
        ) {

            score1++;

            advantages1.push(
                "larger battery"
            );

        }

        else if (
            batteryValue2 >
            batteryValue1
        ) {

            score2++;

            advantages2.push(
                "larger battery"
            );
        }
    }

    // ==============================
    // Charging
    // ==============================

    const charging1 =
        specs1["Charging"] || "";

    const charging2 =
        specs2["Charging"] || "";

    const watt1 =
        parseInt(charging1);

    const watt2 =
        parseInt(charging2);

    if (
        !isNaN(watt1) &&
        !isNaN(watt2)
    ) {

        if (watt1 > watt2) {

            score1++;

            advantages1.push(
                "faster charging"
            );

        }

        else if (watt2 > watt1) {

            score2++;

            advantages2.push(
                "faster charging"
            );
        }
    }

    // ==============================
    // Final Verdict
    // ==============================

    let winner;
    let verdict;

    if (score1 > score2) {

        winner =
            phone1.name;

        verdict =
            `${phone1.name} is the better overall choice, winning ${score1} comparison categories over ${phone2.name}. ` +
            `Its main advantages include ${advantages1.join(", ")}.`;

    }

    else if (score2 > score1) {

        winner =
            phone2.name;

        verdict =
            `${phone2.name} is the better overall choice, winning ${score2} comparison categories over ${phone1.name}. ` +
            `Its main advantages include ${advantages2.join(", ")}.`;

    }

    else {

        winner =
            "It's a close comparison";

        verdict =
            `Both ${phone1.name} and ${phone2.name} perform similarly based on the available specifications. ` +
            `The better choice depends on which features are most important to the user.`;
    }

    winnerPhone.textContent =
        winner;

    verdictText.textContent =
        verdict;

    comparisonVerdict.classList.remove(
        "hidden"
    );
}

// ==============================
// Compare Button
// ==============================

compareBtn.addEventListener(
    "click",
    function () {

        const phone1Name =
            phone1Select.value;

        const phone2Name =
            phone2Select.value;

        if (
            !phone1Name ||
            !phone2Name
        ) {

            alert(
                "Please select two phones."
            );

            return;
        }

        if (
            phone1Name ===
            phone2Name
        ) {

            alert(
                "Please select two different phones."
            );

            return;
        }

        const phone1 =
            phoneDataList.find(
                phone =>
                    phone.name ===
                    phone1Name
            );

        const phone2 =
            phoneDataList.find(
                phone =>
                    phone.name ===
                    phone2Name
            );

        if (
            !phone1 ||
            !phone2
        ) {
            return;
        }

        // Phone Names

        document.getElementById(
            "comparePhone1"
        ).textContent =
            phone1.name;

        document.getElementById(
            "comparePhone2"
        ).textContent =
            phone2.name;

        // Display

        document.getElementById(
            "compareDisplay1"
        ).textContent =
            getCompareValue(
                phone1,
                "Size"
            );

        document.getElementById(
            "compareDisplay2"
        ).textContent =
            getCompareValue(
                phone2,
                "Size"
            );

        // Chipset

        document.getElementById(
            "compareChipset1"
        ).textContent =
            getCompareValue(
                phone1,
                "Chipset"
            );

        document.getElementById(
            "compareChipset2"
        ).textContent =
            getCompareValue(
                phone2,
                "Chipset"
            );

        // Camera

        document.getElementById(
            "compareCamera1"
        ).textContent =
            getCompareValue(
                phone1,
                "Main Camera"
            );

        document.getElementById(
            "compareCamera2"
        ).textContent =
            getCompareValue(
                phone2,
                "Main Camera"
            );

        // Battery

        document.getElementById(
            "compareBattery1"
        ).textContent =
            getCompareValue(
                phone1,
                "Battery"
            );

        document.getElementById(
            "compareBattery2"
        ).textContent =
            getCompareValue(
                phone2,
                "Battery"
            );

        // Charging

        document.getElementById(
            "compareCharging1"
        ).textContent =
            getCompareValue(
                phone1,
                "Charging"
            );

        document.getElementById(
            "compareCharging2"
        ).textContent =
            getCompareValue(
                phone2,
                "Charging"
            );

        // AI Comparison Verdict

        generateComparisonVerdict(
            phone1,
            phone2
        );

        compareResult.classList.remove(
            "hidden"
        );
    }
);