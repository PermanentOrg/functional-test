import { defineConfig } from "cypress";
import { generatePassword } from "./cypress/support/generatePassword";

export default defineConfig({
  e2e: {
    setupNodeEvents(_on, config) {
      // implement node event listeners here
      const conf = config;
      const date = new Date();
      const timestamp = Math.floor(date.getTime() / 1000);
      conf.env["BASE_EMAIL"] = "engineers@permanent.org";
      conf.env["TIMESTAMP"] = timestamp.toString();
      conf.env["PASSWORD"] = generatePassword(12);
      return conf;
    },
    video: false,
    specPattern: [
      "cypress/e2e/health.cy.ts",
      "cypress/e2e/credentials.cy.ts",
      "cypress/e2e/signup.cy.ts",
      "cypress/e2e/cleanup.cy.ts",
    ],
    baseUrl: "https://ng.permanent.org:4200",
  },
});
