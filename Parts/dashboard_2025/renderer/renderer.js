// renderer.js
// This script listens for incoming CSV data (using `window.electronAPI.onCSVData(...)`)
// and updates every piece of the dashboard, including:
//  • Temperature bar height & readouts
//  • Speed, Motor Usage, Total Wh, Distance, Solar, etc.
//  • Eight per‐module cell bars (0–5 V → width%)
//  • Brake status, tyre pressures, module state, etc.

// 1) Toggle theme and Download CSV functions (you can keep or remove if not used)
function toggleTheme() {
  document.body.classList.toggle("dark-mode");
}

function downloadCSV() {
  const csvContent = `speed,battery,engine_temp,fuel
0,0,0,0`;
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.setAttribute("href", URL.createObjectURL(blob));
  link.setAttribute("download", "dashboard_data.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// 2) Helper to clamp values (e.g. for bar widths)
function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

// 3) Listener: when new CSV arrives, update the DOM
window.electronAPI.onCSVData((data) => {
  // Example CSV headers (as an object `data`):
  // {
  //   speed: "15",
  //   motor_usage: "120",
  //   total_wh: "260",
  //   distance: "1.23",
  //   solar_output: "130",
  //   solar_cumulative: "0.3",
  //   current_temp: "27.8",
  //   cooling_temp: "28.0",
  //   // … etc. plus module1_percent, module1_voltage, m1c1_voltage, m1c2_voltage, …
  //   // m1c1_voltage: "4.002", m1c2_voltage: "4.008", …, tyre_lf: "35.9", brake_status: "applied", …
  // }

  // 3.1 TEMPERATURE SECTION
  const tempValue = parseFloat(data.current_temp || "0");
  const maxTempValue = parseFloat(data.max_temp || "80"); // default max
  const fillPct = clamp((tempValue / maxTempValue) * 100, 0, 100);
  document.getElementById("current-temp").textContent = `${tempValue.toFixed(1)}°C`;
  document.getElementById("cooling-temp").textContent = `Cooling ${parseFloat(data.cooling_temp || "0").toFixed(1)}°C`;
  document.querySelector(".temp-fill").style.height = `${fillPct}%`;

  // 3.2 CORE STATS: Motor Usage, Speed, Total Wh
  const motorUsage = parseFloat(data.motor_usage || "0");
  const speed = parseFloat(data.speed || "0");
  const totalWh = parseFloat(data.total_wh || "0");
  document.getElementById("motor-usage").textContent = `${motorUsage.toFixed(0)} W`;
  document.getElementById("speed").textContent = `${speed.toFixed(0)}`;
  document.getElementById("wh-total").textContent = `${totalWh.toFixed(0)} Wh`;

  // 3.3 SUMMARY CARD: Distance & Solar
  const distance = parseFloat(data.distance || "0");
  const solarValue = parseFloat(data.solar_output || "0");
  const solarCum = parseFloat(data.solar_cumulative || "0");
  document.getElementById("distance").textContent = `${distance.toFixed(2)} km`;
  document.getElementById("solar-output").textContent = `${solarValue.toFixed(0)} W`;
  document.querySelector(".solar-cumulative").textContent = `Cumulative: ${solarCum.toFixed(1)} Wh`;

  // 3.4 BRAKE STATUS
  const brakeState = data.brake_status === "applied" ? "applied" : "released";
  const brakeIndicator = document.getElementById("brake-status");
  brakeIndicator.textContent = brakeState === "applied" ? "Applied" : "Released";
  brakeIndicator.className = brakeState === "applied" ? "brake-indicator applied" : "brake-indicator released";

  // 3.5 TYRE PRESSURES
  document.getElementById("tyre-lf").textContent = `${parseFloat(data.tyre_lf || "0").toFixed(1)} PSI`;
  document.getElementById("tyre-rf").textContent = `${parseFloat(data.tyre_rf || "0").toFixed(1)} PSI`;
  document.getElementById("tyre-lr").textContent = `${parseFloat(data.tyre_lr || "0").toFixed(1)} PSI`;
  document.getElementById("tyre-rr").textContent = `${parseFloat(data.tyre_rr || "0").toFixed(1)} PSI`;

  // 3.6 MODULE 1: Percent, Voltage, and 8 Cell Bars (0–5V)
  const m1Percent = clamp(parseFloat(data.module1_percent || "0"), 0, 100);
  const m1Voltage = parseFloat(data.module1_voltage || "0");
  document.getElementById("module1-percent").textContent = `${m1Percent.toFixed(1)} %`;
  document.getElementById("module1-voltage").textContent = `V: ${m1Voltage.toFixed(2)} V`;
  document.querySelector("#m1c1-bar").style.width = `${clamp((parseFloat(data.m1c1_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c1").textContent = `${parseFloat(data.m1c1_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c2-bar").style.width = `${clamp((parseFloat(data.m1c2_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c2").textContent = `${parseFloat(data.m1c2_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c3-bar").style.width = `${clamp((parseFloat(data.m1c3_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c3").textContent = `${parseFloat(data.m1c3_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c4-bar").style.width = `${clamp((parseFloat(data.m1c4_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c4").textContent = `${parseFloat(data.m1c4_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c5-bar").style.width = `${clamp((parseFloat(data.m1c5_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c5").textContent = `${parseFloat(data.m1c5_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c6-bar").style.width = `${clamp((parseFloat(data.m1c6_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c6").textContent = `${parseFloat(data.m1c6_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c7-bar").style.width = `${clamp((parseFloat(data.m1c7_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c7").textContent = `${parseFloat(data.m1c7_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m1c8-bar").style.width = `${clamp((parseFloat(data.m1c8_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m1c8").textContent = `${parseFloat(data.m1c8_voltage || "0").toFixed(3)} V`;

  // 3.7 MODULE 2: Percent, Voltage, and 8 Cell Bars
  const m2Percent = clamp(parseFloat(data.module2_percent || "0"), 0, 100);
  const m2Voltage = parseFloat(data.module2_voltage || "0");
  document.getElementById("module2-percent").textContent = `${m2Percent.toFixed(1)} %`;
  document.getElementById("module2-voltage").textContent = `V: ${m2Voltage.toFixed(2)} V`;
  document.querySelector("#m2c1-bar").style.width = `${clamp((parseFloat(data.m2c1_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c1").textContent = `${parseFloat(data.m2c1_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c2-bar").style.width = `${clamp((parseFloat(data.m2c2_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c2").textContent = `${parseFloat(data.m2c2_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c3-bar").style.width = `${clamp((parseFloat(data.m2c3_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c3").textContent = `${parseFloat(data.m2c3_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c4-bar").style.width = `${clamp((parseFloat(data.m2c4_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c4").textContent = `${parseFloat(data.m2c4_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c5-bar").style.width = `${clamp((parseFloat(data.m2c5_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c5").textContent = `${parseFloat(data.m2c5_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c6-bar").style.width = `${clamp((parseFloat(data.m2c6_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c6").textContent = `${parseFloat(data.m2c6_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c7-bar").style.width = `${clamp((parseFloat(data.m2c7_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c7").textContent = `${parseFloat(data.m2c7_voltage || "0").toFixed(3)} V`;
  document.querySelector("#m2c8-bar").style.width = `${clamp((parseFloat(data.m2c8_voltage || "0") / 5) * 100, 0, 100)}%`;
  document.getElementById("m2c8").textContent = `${parseFloat(data.m2c8_voltage || "0").toFixed(3)} V`;

  // 3.8 12V BATTERY: Percent & Voltage
  const battPercent = clamp(parseFloat(data.battery_percent || "0"), 0, 100);
  const battVoltage = parseFloat(data.battery_voltage || "0");
  document.getElementById("battery-percent").textContent = `${battPercent.toFixed(1)} %`;
  document.getElementById("battery-voltage").textContent = `V: ${battVoltage.toFixed(2)} V`;
});
