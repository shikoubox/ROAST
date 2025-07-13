/* renderer.js
This script listens for incoming CSV data (using `window.electronAPI.onCSVData(...)`)
and updates every piece of the dashboard, including:
- Temperature bar height & readouts
- Speed, Motor Usage, Total Wh, Distance, Solar, etc.
- Eight per‐module cell bars (0–5 V → height%)
- Brake status, tyre pressures, module state, etc.
*/
// Toggle theme and download CSV functions
const toggleButton = document.getElementById('theme_toggle');
toggleButton.addEventListener('click', ()=> {
    document.body.classList.toggle('dark-mode');
});

function downloadCSV() {
  const csvContent = `speed,battery,engine_temp,fuel,0,0,0`;
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.setAttribute("href", URL.createObjectURL(blob));
  link.setAttribute("download", "dashboard_data.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Clamp values (e.g. for bar widths)
function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

// When new CSV arrives, update the DOM
window.electronAPI.onCSVData((data) => {

  // Temperature and Cooling
  const tempValue = parseFloat(data.current_temp || "ERROR");
  const maxTempValue = parseFloat(data.max_temp || "ERROR"); // default max
  const fillPct = clamp((tempValue / maxTempValue) * 100, 0, 100);
  document.getElementById("current_temp").textContent = `${tempValue.toFixed(1)}°C`;
  document.getElementById("cooling_temp").textContent = `Cooling ${parseFloat(data.cooling_temp || "0").toFixed(1)}°C`;
  document.querySelector(".temp-fill").style.height = `${fillPct}%`;

  // Motor Usage, Speed, Total Wh
  const motorUsage = parseFloat(data.motor_usage || "0");
  const speed = parseFloat(data.speed || "0");
  const totalWh = parseFloat(data.wh_total || "0");
  document.getElementById("motor_usage").textContent = `${motorUsage.toFixed(0)}`;
  document.getElementById("speed").textContent = `${speed.toFixed(0)}`;
  document.getElementById("wh_total").textContent = `${totalWh.toFixed(0)}`;

  // Distance, Solar Output, and Cumulative Solar
  const distance = parseFloat(data.distance || "0");
  const solarValue = parseFloat(data.solar_output || "0");
  const solarCum = parseFloat(data.solar_cumulative || "0");
  document.getElementById("distance").textContent = `${distance.toFixed(2)} km`;
  document.getElementById("solar_output").textContent = `${solarValue.toFixed(0)} W`;
  document.querySelector(".solar-cumulative").textContent = `Cumulative: ${solarCum.toFixed(1)} Wh`;

  // Brake status
  const brakeState = data.brake_status === "1" ? "1" : "0";
  const brakeIndicator = document.getElementById("brake-status");
  brakeIndicator.textContent = brakeState === "1" ? "Applied" : "Released";
  brakeIndicator.className = brakeState === "applied" ? "indicator green" : "indicator red";
    

  const radioState = parseFloat(data.radio_state || "0");
  document.getElementById('dBm').textContent = `Last radio packet strength: ${radioState} dBm`;

  // Tyre Pressures
  document.getElementById("tyre_lf").textContent = `${parseFloat(data.tyre_lf || "0").toFixed(1)} PSI`;
  document.getElementById("tyre_rf").textContent = `${parseFloat(data.tyre_rf || "0").toFixed(1)} PSI`;
  document.getElementById("tyre_lr").textContent = `${parseFloat(data.tyre_lr || "0").toFixed(1)} PSI`;
  document.getElementById("tyre_rr").textContent = `${parseFloat(data.tyre_rr || "0").toFixed(1)} PSI`;

  // Module one states
  const m1Percent = clamp(parseFloat(data.module1_percent || "0"), 0, 100);
  const m1Voltage = parseFloat(data.module1_voltage || "0");
  document.getElementById("module1_percent").textContent = `${m1Percent.toFixed(1)} %`;
  document.getElementById("module1_voltage").textContent = `V: ${m1Voltage.toFixed(2)} V`;
  document.querySelector("#m1-bar").style.width    = `${clamp(parseFloat(m1Percent || "0"), 0, 100)}%`;
  updateCellBar("#m1c1-bar", "m1c1", data.m1c1);
  updateCellBar("#m1c2-bar", "m1c2", data.m1c2);
  updateCellBar("#m1c3-bar", "m1c3", data.m1c3);
  updateCellBar("#m1c4-bar", "m1c4", data.m1c4);
  updateCellBar("#m1c5-bar", "m1c5", data.m1c5);
  updateCellBar("#m1c6-bar", "m1c6", data.m1c6);
  updateCellBar("#m1c7-bar", "m1c7", data.m1c7);
  updateCellBar("#m1c8-bar", "m1c8", data.m1c8);

  // Module two states
  const m2Percent = clamp(parseFloat(data.module2_percent || "0"), 0, 100);
  const m2Voltage = parseFloat(data.module2_voltage || "0");
  document.getElementById("module2_percent").textContent = `${m2Percent.toFixed(1)} %`;
  document.getElementById("module2_voltage").textContent = `V: ${m2Voltage.toFixed(2)} V`;
  document.querySelector("#m2-bar").style.width    = `${clamp(parseFloat(m2Percent || "0"), 0, 100)}%`;
  updateCellBar("#m2c1-bar", "m2c1", data.m2c1);
  updateCellBar("#m2c2-bar", "m2c2", data.m2c2);
  updateCellBar("#m2c3-bar", "m2c3", data.m2c3);
  updateCellBar("#m2c4-bar", "m2c4", data.m2c4);
  updateCellBar("#m2c5-bar", "m2c5", data.m2c5);
  updateCellBar("#m2c6-bar", "m2c6", data.m2c6);
  updateCellBar("#m2c7-bar", "m2c7", data.m2c7);
  updateCellBar("#m2c8-bar", "m2c8", data.m2c8);


  // 12 V battery states
  const battPercent = clamp(parseFloat(data.battery_percent || "0"), 0, 100);
  const battVoltage = parseFloat(data.battery_voltage || "0");
  document.getElementById("battery_percent").textContent = `${battPercent.toFixed(1)} %`;
  document.getElementById("battery_voltage").textContent = `V: ${battVoltage.toFixed(2)} V`;
});

// Update cell bar heights and voltages
function updateCellBar(barSelector, voltageId, voltageData) {
  const cellPercent = clamp((parseFloat(voltageData || "0") / 5) * 100, 0, 100);
  document.querySelector(barSelector).style.height = `${cellPercent}%`;

  // Change background color based on height
  if (cellPercent < 81 && cellPercent > 63) {
    document.querySelector(barSelector).style.backgroundColor = '#22c55e'; // Green
  } else if (cellPercent >= 59 && cellPercent < 85) {

    document.querySelector(barSelector).style.backgroundColor = '#f59e0b'; // Yellow
  } else {
    document.querySelector(barSelector).style.backgroundColor = '#ef4444'; // Red
  }
  document.getElementById(voltageId).textContent = `${parseFloat(voltageData || "0").toFixed(3)} V`;
}

