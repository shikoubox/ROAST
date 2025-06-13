// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onCSVData: (callback) => {
    ipcRenderer.on('csv-data', (event, parsedObject) => {
    console.log('Parsed Object:', parsedObject);
    console.log('Callback Function:', callback);
    callback(parsedObject);

    });
  },
  logToConsole: (message) => ipcRenderer.send('log-to-console', message)
});
