This is a guide on how to set Raspberry Pi up to work with dashboard and/or radio module.

# Requirements
RPI 3B+ with bullseye
    (3B+ has easiest USB booting capabilities (plug and play))
Do not attach high power components during booting. (recommended below 0.5A)

## Display requirements
node -v # should be v16+
npm -v  # should be v8+

## RF requirements:
python3
https://learn.adafruit.com/adafruit-radio-bonnets/rfm69-raspberry-pi-setup

## CAN requirements:
https://spotpear.com/index/study/detail/id/586.html

# Setup guide
sudo apt install -y git 
git clone --single-branch --branch pi_dashboard https://github.com/shikoubox/ROAST
(Now you can copy from readme)
sudo apt install -y ca-certificates curl gnupg python3 python3-venv python3-pip tmux vim


## Setup CircuitPython
python3 -m venv ~/ROAST/Parts/dashboard_2025/RF
source ~/ROAST/Parts/dashboard_2025/RF/bin/activate
pip3 install --upgrade adafruit-python-shell
sudo -E env PATH=$PATH python3 setup-circuitpython.py

### Check if RF is setup correctly
python3 radio_module.py ### is somewhere in dashboard_2025/radio_module folder

## Related to dashboard
### Setup nodejs and npm on Raspberry PI
```bash
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource.gpg
NODE_MAJOR=22
echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install nodejs
```

### Install dashboard on pi 
```bash
npm init -y
npm install electron --save-dev
```

### How to run dashboard
```bash
npm start
```
### Start dashboard on raspberry-pi through ssh
```bash
DISPLAY=:0 npm start
```

## Useful git commands
### Clone specific branch
git clone --single-branch --branch <desired_branch> https://github.com/shikoubox/ROAST
### Pull specific file from other branch
git checkout <source_branch>
git checkout <desired_branch> -- <desired_directory>
git add <desired_directory>
git commit -m "Copied directory from desired_branch to source_branch"

# Programming notes
Do not use the internal temperature of the rfm69hcw chip. Be warned this is not calibrated or very accurate. Warning: Reading this will STOP any receiving/sending that might be happening


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
