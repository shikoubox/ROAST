// Switch between dark and light themes by toggling class on body
function toggleTheme() {
    document.body.classList.toggle("dark-mode");
}

// Download sample CSV data - simulates exporting current dashboard state
function downloadCSV() {
    const csvContent = `speed,battery,engine_temp,fuel\n no,no,no,no`;
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.setAttribute("href", URL.createObjectURL(blob));
    link.setAttribute("download", "dashboard_data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-container').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

// Optional: default tab on page load
window.onload = () => showTab('full');

window.electronAPI.onCSVData(data => {
    document.getElementById('speed').textContent = `${data.speed} km/h`;
    document.getElementById('battery-voltage').textContent = `${data.battery} V`;
    document.getElementById('engine-temp').textContent = `${data.engine_temp} °C`;
    document.getElementById('fuel-level').textContent = `${data.fuel}%`;

    // Also update "quick" container
    document.getElementById('speed-quick').textContent = `${data.speed} km/h`;
    document.getElementById('battery-voltage-quick').textContent = `${data.battery} V`;
});

