const primaryChart = new ChartWrapper("Primary Numbers")
const secondaryChart = new ChartWrapper("Secondary Numbers")
const combinedChart = new ChartWrapper("Primary+Secondary Numbers")
// Populate the dropdown with available Lott values
function populateLottDropdown() {
    console.log("Trying to fetch Lott types...");
    
    fetch('/lott-types')
    .then(response => {
        console.log("Received response:", response);
        return response.json();
    })
    .then(lottTypes => {
        console.log("Parsed Lott types:", lottTypes);
        
        const lottSelect = document.getElementById('lottSelect');
        lottTypes.forEach(lott => {
            const option = document.createElement('option');
            option.value = lott;
            option.textContent = lott;
            lottSelect.appendChild(option);
        });
    })
    .catch(error => {
        console.error("Error fetching Lott types:", error);
    });
}

// Fetch results for the selected Lott type and render graphs
function fetchResults() {
    const selectedLott = document.getElementById('lottSelect').value;
    fetch(`/results/${selectedLott}`)
    .then(response => response.json())
    .then(results => {
        displayUniqueDays(results);
        renderGraphs(results);
    });
}

// Display unique days based on the fetched results
function displayUniqueDays(results) {
    const uniqueDays = [...new Set(results.map(result => new Date(result.draw_date).getDay()))];
    const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const daysDiv = document.getElementById('uniqueDays');
    daysDiv.textContent = uniqueDays.map(dayIndex => dayNames[dayIndex]).join(', ');
}

function getNumberOccurrences(numbers) {
    let occurrences = {};
    numbers.forEach(number => {
        occurrences[number] = (occurrences[number] || 0) + 1;
    });
    const sortedNumbers = Object.keys(occurrences).sort((a, b) => occurrences[b] - occurrences[a]);
    const sortedOccurrences = sortedNumbers.map(number => occurrences[number]);
    return { numbers: sortedNumbers, occurrences: sortedOccurrences };
}

// Render bar graphs using Chart.js based on the fetched results
function renderGraphs(results) {
    // Extract and process data for primary numbers, secondary numbers, and combined numbers
    const primaryNumbers = results.flatMap(result => result.primary_numbers);
    const secondaryNumbers = results.flatMap(result => result.secondary_numbers);
    
    const primaryOccurrences = getNumberOccurrences(primaryNumbers);
    const secondaryOccurrences = getNumberOccurrences(secondaryNumbers);
    const combinedOccurrences = getNumberOccurrences([...primaryNumbers, ...secondaryNumbers]);

    primaryChart.refresh(primaryOccurrences);
    secondaryChart.refresh(secondaryOccurrences);
    combinedChart.refresh(combinedOccurrences);
}

// Initial call to populate the Lott dropdown
populateLottDropdown();
