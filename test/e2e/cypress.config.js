const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:3000",
    video: false,
    chromeWebSecurity: false,
    supportFile: "cypress/support/e2e.js",
  },
});
