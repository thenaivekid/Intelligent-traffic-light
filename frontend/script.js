// Initialize map
const map = L.map('map').setView([27.677097, 85.316301], 30);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap'
}).addTo(map);

// Define lanes
const lanes = [
  { name: 'North Lane', lat: 27.677097, lng: 85.316301 },
  // { name: 'South Lane', lat: 27.6840, lng: 85.3188 },
  // { name: 'East Lane', lat: 27.6845, lng: 85.3192 },
  // { name: 'West Lane', lat: 27.6845, lng: 85.3184 }
];

// Fetch vehicle count for a lane (dummy data)
async function getLaneVehicleCount(lat, lng) {
  // Simulated API response - replace with real API call if necessary
  const vehicleCount = Math.floor(Math.random() * 50); // Random vehicle count
  let signalColor;

  if (vehicleCount < 10) {
    signalColor = 'green';
  } else if (vehicleCount < 30) {
    signalColor = 'yellow';
  } else {
    signalColor = 'red';
  }

  return { vehicleCount, signalColor };
}



// Display lane counts with traffic light indicators
async function displayLaneCounts() {
  for (const lane of lanes) {
    const { vehicleCount, signalColor } = await getLaneVehicleCount(lane.lat, lane.lng);

    // Custom traffic light icon (only one light is bright)
    const trafficLightIconCustom = L.divIcon({
      className: 'traffic-light-icon',
      html: `
        <div style="display: flex; flex-direction: column;">
          <div style="background-color: ${signalColor}; width: 20px; height: 20px; border-radius: 50%;"></div>
        </div>
      `,
      iconSize: [30, 30] // Icon size
    });

    // Add marker with the custom traffic light
    L.marker([lane.lat, lane.lng], { icon: trafficLightIconCustom })
      .addTo(map)
      .bindPopup(`${vehicleCount} vehicles`)
      .openPopup()
      
  }
}

// Custom CSS for popup
const popupStyle = `
  .leaflet-popup-content-wrapper {
    background-color: transparent;
    border: none;
    box-shadow: none;
  }
  .leaflet-popup-content {
    color: blue; /* Adjust text color */
    font-size: 20px; /* Adjust text size */
  }
  .leaflet-popup-tip-container {
    display: none; /* Hide the popup arrow */
  }
`;

// Append style to the document
const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = popupStyle;
document.head.appendChild(styleSheet);

// Display counts initially and update dynamically
displayLaneCounts();
setInterval(displayLaneCounts, 10000); // Refresh every 10 seconds
