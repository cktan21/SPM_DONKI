const { defineConfig } = require("cypress");
const fs = require("fs");
const path = require("path");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:3000",
    video: false,
    chromeWebSecurity: false,
    supportFile: "cypress/support/e2e.js",
      
    setupNodeEvents(on, config) {
      // custom tasks for checking and clearing downloads
      on("task", {
        findDownloadedFile({ dir, ext }) {
          const files = fs.readdirSync(dir);
          const found = files.find((file) => file.endsWith(ext));
          return found ? path.join(dir, found) : null;
        },

        clearDownloads(dir) {
          fs.rmSync(dir, { recursive: true, force: true });
          return null;
        },
      });

      return config;
    },
  },
});

