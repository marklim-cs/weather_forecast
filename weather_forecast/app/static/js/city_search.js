let cities = [];

document.addEventListener("DOMContentLoaded", () => {
    // Fetch the city list JSON file
    fetch("/static/data/current.city.list.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            cities = data;  // Store the cities data
            console.log("Cities loaded:", cities);
        })
        .catch(error => console.error("Error loading cities:", error));

    // Get input fields
    const cityInput1 = document.getElementById("city_input1");
    const cityInput2 = document.getElementById("city_input2");

    // Attach event listeners
    cityInput1.addEventListener("input", () => filterCities(cityInput1, ".city_list1"));
    cityInput2.addEventListener("input", () => filterCities(cityInput2, ".city_list2"));
});

function filterCities(inputElement, listSelector) {
    const inputValue = inputElement.value.toLowerCase();

    // Filter cities based on the input value
    const filteredCities = cities.filter(city =>
        city.name.toLowerCase().startsWith(inputValue)
    );

    // Get the city list to populate
    const cityList = document.querySelector(listSelector);

    if (!cityList) {
        console.error(`List element not found for selector: ${listSelector}`);
        return;
    }

    // Clear the city list
    cityList.innerHTML = "";

    // Limit the number of displayed results (optional)
    const maxResults = 10;

    // Populate the list with filtered cities
    filteredCities.slice(0, maxResults).forEach(city => {
        const li = document.createElement("li");
        li.textContent = `${city.name}, ${city.country}`;
        cityList.appendChild(li);
    });
}
