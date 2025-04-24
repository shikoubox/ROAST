const { app, BrowserWindow } = require('electron') // import 

  app.disableHardwareAcceleration();

function createWindow() {
  const win = new BrowserWindow({
    width: 800, 
    height: 600   
  })

  win.loadFile('index.html') // load renderer 
}


app.whenReady().then(() => {  

  createWindow()

  app.on('activate', () => {

    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }

  })

})
