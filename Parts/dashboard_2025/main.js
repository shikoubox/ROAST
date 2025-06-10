// main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs   = require('fs');

// Import the function that prepends a new row to data.csv:
const { execFile } = require("child_process");
function prependNewRow() {
  execFile("python", [path.join(__dirname, "data", "data.py")], (error, stdout, stderr) => {
    if (error) {
      console.error("Python script error:", stderr);
      return;
    }
    console.log(stdout);
  });
}


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

 /* // Every 2 seconds, prepend a new row to data.csv:
  setInterval(() => {
    prependNewRow();
  }, 2000);
*/

  // Every 2 seconds, re‐read the “latest” line (line 2) from data.csv
  // and send it via IPC to renderer.js:
  setInterval(() => {
    const csvPath = path.join(__dirname, 'data', 'data.csv');
    fs.readFile(csvPath, 'utf8', (err, rawText) => {
      if (err) {
        console.error('CSV Read Error:', err);
        return;
      }
      const lines = rawText.trimEnd().split('\n');
      if (lines.length < 2) return;
      const headers = lines[0].split(',').map(h => h.trim());
      const values  = lines[1].split(',').map(v => v.trim());
      const parsed = {};
      headers.forEach((h, i) => {
        parsed[h] = values[i] !== undefined ? values[i] : '';
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
