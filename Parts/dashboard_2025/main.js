// main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs   = require('fs');
const { execFile } = require('child_process');  // ← add this

app.disableHardwareAcceleration();



let mainWindow = null;
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 870,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.setMenuBarVisibility(false);
  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

ipcMain.on('log-to-console', (event, message) => {
  console.log(message);
});

let previousParsed = {};

app.whenReady().then(() => {
  createWindow();

  // Every 10 seconds, append a snapshot row:
  setInterval(() => {
    execFile('python', [path.join(__dirname, 'radio_module', 'csv_handler.py'), 'log'], (err, stdout, stderr) => {
      if (err) {
        console.error('Logging error:', stderr || err);
      } else {
        console.log('Logged snapshot:', stdout.trim());
      }
    });
  }, 10_000);  // ← 10 000 ms = 10 s

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

      // Compare the new parsed data with the previous data
      const changes = {};
      let hasChanges = false;


      for (const key in parsed) {
        if (parsed[key] !== previousParsed[key]) {
          changes[key] = parsed[key];
          hasChanges = true;
        }
      }

      if (hasChanges && mainWindow && mainWindow.webContents) {
        mainWindow.webContents.send('csv-data', parsed);
      }

      // If there are changes, send only the changed pairs
      //if (hasChanges && mainWindow && mainWindow.webContents) {
      //  mainWindow.webContents.send('csv-data', changes);
      //}
      // NOT IMPLEMENTED IN RENDERER.JS, thus leave ito ut for now.


      previousParsed = parsed;
    });
  }, 200);
});


app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
