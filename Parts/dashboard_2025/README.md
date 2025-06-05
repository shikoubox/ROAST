# Requirements
node -v # should be v16+
npm -v  # should be v8+

## RF requirements:
python3
https://learn.adafruit.com/adafruit-radio-bonnets/rfm69-raspberry-pi-setup

## CAN requirements:
https://spotpear.com/index/study/detail/id/586.html

# Setup guide

## Setup nodejs and npm on Raspberry PI
```bash
sudo apt install -y ca-certificates curl gnupg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource.gpg
NODE_MAJOR=22
echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install nodejs
```

## Install locally
```bash
npm init -y
npm install electron --save-dev
```
# How to run
```bash
npm start
```
### Run on raspberry-pi through ssh
```bash
DISPLAY=:0 npm start
```

# Explanations of electron structure:
* main.js: The electron entry (main process) that runs the backend main process to control GUI and respond to system events
* index.html: The frontend UI that will be loaded into the render process (browser window)
* styles.css: CSS stylesheet to decorate the UI
* node_modules: Electron, Node.js and other dependencies

```
project/
├── main.js           <- Electron entry (main process)
├── preload.js        <- Bridge between Node.js and renderer
├── renderer/
│   ├── index.html
│   ├── renderer.js   <- All UI logic
├── data/
│   └── data.csv      <- Simulated sensor data (updated externally)
├── styles.css
```
```bash
