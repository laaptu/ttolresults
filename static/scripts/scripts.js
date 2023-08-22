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
        occurrences = results.response.occurrences
        days = results.response.days
        displayUniqueDays(days, (day) => {
            const dayData = occurrences.find(occ => occ.day === day);
            renderGraphs(dayData);
        });
        //renderGraphs(occurences);
    });
}

// Display unique days based on the fetched results
function displayUniqueDays(days, callback) {
    const container = document.getElementById('uniqueDaysContainer');
    container.innerHTML = ''; // Clear any previous content

    days.forEach(day => {
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'day';
        radio.value = day;
        radio.id = `radio-${day}`;
        radio.addEventListener('change', (event) => callback(day));

        const label = document.createElement('label');
        label.htmlFor = `radio-${day}`;
        label.textContent = day;

        container.appendChild(radio);
        container.appendChild(label);
        if(day == 'All'){
            radio.checked = true
            callback(day)
       }
    });
}


// Render bar graphs using Chart.js based on the fetched results
function renderGraphs(occurences) {
    primaryChart.refresh(occurences.primaryNumOcc);
    secondaryChart.refresh(occurences.secondaryNumOcc);
    combinedChart.refresh(occurences.combinedNumOcc);
}

// Initial call to populate the Lott dropdown
populateLottDropdown();
