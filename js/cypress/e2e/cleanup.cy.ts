import { Credentials } from "../support/credentials";

describe("cleanup tests", () => {
  const credentials = new Credentials();
  beforeEach(async () => {
    await credentials.loadSession();
  });
  it("can delete its account", () => {
    const sessions = credentials.getAllSessions();
    for (const session of sessions) {
      credentials.setSession(session);
      cy.login(credentials.getEmail(), credentials.getPassword());
      cy.url().should("include", "private");

      cy.visit(`/app/account`);
      cy.get("pr-account-settings-dialog .settings-tab")
        .contains("Delete Account")
        .click();
      cy.get("pr-account-settings-dialog input[type='text']").type("DELETE");
      cy.get("pr-account-settings-dialog button.btn-danger").click();
      cy.url().should("not.include", "app");
    }
    credentials.resetSessions();
  });
});
