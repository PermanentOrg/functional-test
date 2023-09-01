import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    setupNodeEvents(_on, config) {
      // implement node event listeners here
      const conf = config;
      conf.env["BASE_EMAIL"] = "engineers@permanent.org";
      return conf;
    },
    video: false,
    specPattern: ["cypress/e2e/health.cy.ts", "cypress/e2e/signup.cy.ts"],
    baseUrl: "https://ng.permanent.org:4200",
  },
});
