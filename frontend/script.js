// Initialize map
const map = L.map('map').setView([27.677097, 85.316301], 18);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap',
}).addTo(map);

// Define camera locations with their IDs
const cameraLocations = {
  cam1: { name: 'Patan', lat: 27.677079, lng: 85.316386 },
  cam2: { name: 'Kupandol', lat: 27.677414, lng: 85.316343 },
  cam3: { name: 'Jaulakhel', lat: 27.676861, lng: 85.316115 },
};

// Markers for traffic lights
const trafficCircles = {};

// Initialize traffic light markers on the map
function initializeMarkers() {
  Object.entries(cameraLocations).forEach(([camId, location]) => {
    trafficCircles[camId] = L.circle([location.lat, location.lng], {
      color: 'red', // Default color
      fillColor: 'red',
      fillOpacity: 0.5,
      radius: 10, // Circle radius in meters
    }).addTo(map);
  });
}
function createTrafficTable() {
    const container = document.getElementById('traffic-container');
    
    const table = document.createElement('table');
    table.id = 'traffic-table';
    table.style.width = '40%';
    table.style.borderCollapse = 'collapse';
    table.style.margin = '20px auto';
    table.style.fontSize = '18px';
    table.style.fontFamily = 'Arial, sans-serif';
    table.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';

    table.innerHTML = `
      <thead style="background-color: #4CAF50; color: white;">
        <tr>
          <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Path from</th>
          <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Number of Vehicles</th>
        </tr>
      </thead>
      <tbody>
        ${Object.entries(cameraLocations).map(([camId, location]) => `
          <tr id="${camId}-row" style="background-color: #f9f9f9; transition: background-color 0.3s;">
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">${location.name}</td>
            <td id="${camId}-count" style="padding: 10px; border-bottom: 1px solid #ddd;">0</td>
          </tr>`).join('')}
      </tbody>
    `;

    container.appendChild(table);

    // Add hover effect for rows
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseover', () => {
            row.style.backgroundColor = '#f1f1f1';
        });
        row.addEventListener('mouseout', () => {
            row.style.backgroundColor = '#f9f9f9';
        });
    });
}


  function updateTrafficTable(vehicleCounts) {
    Object.entries(vehicleCounts).forEach(([camId, count]) => {
      const countCell = document.getElementById(`${camId}-count`);
      if (countCell) {
        countCell.textContent = count;
      }
    });
  }
  
  
// Fetch traffic data from the API
async function getTrafficData() {
  try {
    const response = await fetch('http://127.0.0.1:8000/traffic');
    if (!response.ok) {
      throw new Error(`Network error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching traffic data:', error);
    return null;
  }
}

// Update traffic light markers based on the data
async function updateTrafficLights(trafficData) {
  if (!trafficData || !trafficData.green_duration) {
    console.error('Invalid traffic data format');
    return;
  }

  const { green_duration } = trafficData;
  const cameras = Object.keys(cameraLocations);

  for (const [index, camId] of cameras.entries()) {
    const duration = green_duration[camId] || 0;

    // Set the current traffic light to green
    trafficCircles[camId].setStyle({
      color: 'green',
      fillColor: 'green',
    });

    // Wait for the green duration minus 1 second
    await new Promise((resolve) => setTimeout(resolve, (duration - 1) * 1000));

    // Set the current traffic light to yellow for 1 second
    trafficCircles[camId].setStyle({
      color: 'yellow',
      fillColor: 'yellow',
    });
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Set the current traffic light to red
    trafficCircles[camId].setStyle({
      color: 'red',
      fillColor: 'red',
    });
  }
}

// Main function to fetch and update traffic data every 30 seconds
async function main() {
  initializeMarkers();
  createTrafficTable();
  while (true) {
    const trafficData = await getTrafficData();
    console.log(trafficData);
    if (trafficData) {
        updateTrafficTable(trafficData.num_vehicles);
      await updateTrafficLights(trafficData);
    }

    // Wait for 30 seconds before fetching the data again
    await new Promise((resolve) => setTimeout(resolve, 0));
  }
}

// Start the application
main();
