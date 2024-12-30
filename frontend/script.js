// // Initialize map
// const map = L.map('map').setView([27.677097, 85.316301], 30);

// // Add OpenStreetMap tiles
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//   maxZoom: 19,
//   attribution: '© OpenStreetMap'
// }).addTo(map);

// // Define camera locations with their IDs
// const cameraLocations = {
//   cam1: { name: 'Patan', lat: 27.677079, lng: 85.316386 },
//   cam2: { name: 'Kupandol', lat: 27.677414, lng: 85.316343 },
//   cam3: { name: 'Jaulakhel', lat: 27.676861, lng: 85.316115 }
// };

// // Fetch traffic data from the API
// async function getTrafficData() {
//   try {
//     const response = await fetch('http://127.0.0.1:8000/traffic');
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     return await response.json();
//   } catch (error) {
//     console.error('Error fetching traffic data:', error);
//     return null;
//   }
// }

// // Define a map to keep track of markers
// const markers = {};

// // Display camera locations with traffic light indicators
// async function displayTrafficStatus() {
//   const trafficData = await getTrafficData();

//   if (!trafficData) {
//     console.error('Failed to fetch traffic data');
//     return;
//   }

//   // Add or update markers for each camera
//   for (const [camId, location] of Object.entries(cameraLocations)) {
//     const signalColor = trafficData.lights[camId];
//     const vehicleCount = trafficData.num_vehicles[camId];

//     // Custom traffic light icon
//     const trafficLightIconCustom = L.divIcon({
//       className: 'traffic-light-icon',
//       html: `
//         <div style="background-color: ${signalColor}; width: 20px; height: 20px; border-radius: 50%;"></div>
//       `,
//       iconSize: [30, 30]
//     });

//     if (markers[camId]) {
//       // Update existing marker
//       markers[camId].setIcon(trafficLightIconCustom).setPopupContent(`${location.name}: ${vehicleCount} vehicles`);
//     } else {
//       // Create a new marker
//       const marker = L.marker([location.lat, location.lng], { icon: trafficLightIconCustom })
//         .addTo(map)
//         .bindPopup(`${location.name}: ${vehicleCount} vehicles`);
//       markers[camId] = marker;
//     }
//   }
// }

// // Custom CSS for popup
// const popupStyle = `
//   .leaflet-popup-content-wrapper {
//     background-color: transparent;
//     border: none;
//     box-shadow: none;
//   }
//   .leaflet-popup-content {
//     color: blue;
//     font-size: 20px;
//     font-weight: bold;
//   }
//   .leaflet-popup-tip-container {
//     display: none;
//   }
// `;

// // Append style to the document
// const styleSheet = document.createElement("style");
// styleSheet.type = "text/css";
// styleSheet.innerText = popupStyle;
// document.head.appendChild(styleSheet);

// // Display status initially and update every second
// displayTrafficStatus();
// setInterval(displayTrafficStatus, 1000); // Refresh every 1 second



// Initialize map
const map = L.map('map').setView([27.677097, 85.316301], 18);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap'
}).addTo(map);

// Define camera locations with their IDs
const cameraLocations = {
  cam1: { name: 'Patan', lat: 27.677079, lng: 85.316386 },
  cam2: { name: 'Kupandol', lat: 27.677414, lng: 85.316343 },
  cam3: { name: 'Jaulakhel', lat: 27.676861, lng: 85.316115 }
};

// Fetch traffic data from the API
async function getTrafficData() {
  try {
    const response = await fetch('http://127.0.0.1:8000/traffic');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching traffic data:', error);
    return null;
  }
}

// Define a map to keep track of markers
const markers = {};

// Display camera locations with traffic light indicators
async function displayTrafficStatus(trafficData) {
  // Add or update markers for each camera
  for (const [camId, location] of Object.entries(cameraLocations)) {
    const signalColor = trafficData.lights[camId];
    const vehicleCount = trafficData.num_vehicles[camId];

    // Custom traffic light icon
    const trafficLightIconCustom = L.divIcon({
      className: 'traffic-light-icon',
      html: `
        <div style="background-color: ${signalColor}; width: 20px; height: 20px; border-radius: 50%;"></div>
      `,
      iconSize: [30, 30]
    });

    if (markers[camId]) {
      // Update existing marker
      markers[camId].setIcon(trafficLightIconCustom).setPopupContent(`${location.name}: ${vehicleCount} vehicles`);
    } else {
      // Create a new marker
      const marker = L.marker([location.lat, location.lng], { icon: trafficLightIconCustom })
        .addTo(map)
        .bindPopup(`${location.name}: ${vehicleCount} vehicles`);
      markers[camId] = marker;
    }
  }
}

// Main function to fetch and display traffic data every 30 seconds
async function main() {
  while (true) {
    const trafficData = await getTrafficData();

    if (trafficData) {
      displayTrafficStatus(trafficData);
    }

    // Wait for 30 seconds before fetching data again
    await new Promise((resolve) => setTimeout(resolve, 30000));
  }
}

// Start the UI update process
main();
