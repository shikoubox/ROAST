// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs   = require('fs');

app.disableHardwareAcceleration();

let mainWindow = null;
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 480,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

app.whenReady().then(() => {
  createWindow();

  // Every 200 ms, re-read the “latest” line (line 2) from data.csv
  setInterval(() => {
    const csvPath = path.join(__dirname, 'data', 'data.csv');
    fs.readFile(csvPath, null, (err, buffer) => {
      if (err) {
        console.error('CSV Read Error:', err);
        return;
      }

      // Strip UTF-16 LE BOM if present (0xFF 0xFE)
      if (buffer[0] === 0xFF && buffer[1] === 0xFE) {
        buffer = buffer.slice(2);
      }

      // Decode as little-endian UTF-16
      const text = buffer.toString('utf16le');

      const lines = text.trimEnd().split(/\r?\n/);
      if (lines.length < 2) return;

      const headers = lines[0].split(',').map(h => h.trim());
      const values  = lines[1].split(',').map(v => v.trim());
      const parsed  = {};
      headers.forEach((h, i) => {
        parsed[h] = values[i] ?? '';
      });

      if (mainWindow && mainWindow.webContents) {
        mainWindow.webContents.send('csv-data', parsed);
      }
    });
  }, 200);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
