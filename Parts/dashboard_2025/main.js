const { app, BrowserWindow } = require('electron') // import 
const path = require('path');
const fs = require('fs');

app.disableHardwareAcceleration();

function createWindow() {
    const win = new BrowserWindow({
        width: 800, 
        height: 480,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        }
  })

  win.loadFile('renderer/index.html') // load renderer 
}


app.whenReady().then(() => {  

    createWindow()

    startCSVWatcher();

})


  /*  
  app.on('activate', () => {

    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }

  })*/



function startCSVWatcher() {
    const csvPath = path.join(__dirname, 'data', 'data.csv');

    setInterval(() => {
        fs.readFile(csvPath, 'utf8', (err, data) => {
            if (err) return console.error("CSV Read Error:", err);

            const lines = data.trim().split('\n');
            const headers = lines[0].split(',');
            const values = lines[1].split(',');

            const parsed = {};
            headers.forEach((h, i) => parsed[h.trim()] = values[i].trim());

            BrowserWindow.getAllWindows()[0].webContents.send('csv-data', parsed);
        });
    }, 2000); // every 2 seconds
}

