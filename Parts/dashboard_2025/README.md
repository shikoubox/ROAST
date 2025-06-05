# Requirements
node -v # should be v16+
npm -v  # should be v8+

## RF requirements:
python3
https://learn.adafruit.com/adafruit-radio-bonnets/rfm69-raspberry-pi-setup

## CAN requirements:
https://spotpear.com/index/study/detail/id/586.html

# Install locally
npm init -y
npm install electron --save-dev

# How to run
npm start

### Run on raspberry-pi through ssh
DISPLAY=:0 npm start


# Explanations of electron structure:
* main.js: The electron entry (main process) that runs the backend main process to control GUI and respond to system events
* index.html: The frontend UI that will be loaded into the render process (browser window)
* styles.css: CSS stylesheet to decorate the UI
* node_modules: Electron, Node.js and other dependencies


project/
├── main.js           <- Electron entry (main process)
├── preload.js        <- Bridge between Node.js and renderer
├── renderer/
│   ├── index.html
│   ├── renderer.js       <- All UI logic
├── data/
│   └── data.csv      <- Simulated sensor data (updated externally)
├── styles.css
