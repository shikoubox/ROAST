// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onCSVData: (callback) => {
    ipcRenderer.on('csv-data', (event, parsedObject) => {
      callback(parsedObject);
    });
  }
});
