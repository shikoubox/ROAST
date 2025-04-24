# Requirements
node -v # should be v16+
npm -v  # should be v8+

# Install locally
npm init -y
npm install electron --save-dev

# Start
npm start

Explanations of electron structure:
* main.js: The main script that runs the backend main process to control GUI and respond to system events
* index.html: The frontend UI that will be loaded into the render process (browser window)
* styles.css: CSS stylesheet to decorate the UI
* node_modules: Electron, Node.js and other dependencies

