const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    onCSVData: (callback) => ipcRenderer.on('csv-data', (_, data) => callback(data))
});

