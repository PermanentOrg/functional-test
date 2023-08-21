import { Credentials } from "../support/credentials";

describe("signup spec", () => {
  const credentials = new Credentials();
  before(async () => {
    await credentials.loadSession();
    credentials.createNewSession();
  });
  it("gets redirected to app/auth when logged out", () => {
    cy.visit(`/app`);
    cy.url().should("include", "app/auth");
  });
  it("can signup from login page", () => {
    const email = credentials.getEmail();
    const password = credentials.getPassword();
    cy.visit(`/app`);
    cy.get("a").contains("sign up").click();
    cy.get('input[name="name"]').type("Functional Test");
    cy.get('input[name="email"').type(email);
    cy.get('input[name="password"]').type(password);
    cy.get('input[name="confirm"]').type(password);
    cy.get("input#terms").check();
    cy.get("input#mailingList").uncheck();

    cy.get('button[type="submit"]').click();
    cy.url().should("include", "onboarding");

    // Do onboarding:
    cy.get(".get-started button").click();
    cy.get('input[value="type.archive.person"]').parent().click();
    cy.get(".next-button").click();
    cy.get("#archive-name").type("Functional Test");
    cy.get(".next-button").click();

    // Welcome dialog:
    cy.url().should("include", "welcome");
    cy.get("pr-welcome-dialog button.btn-primary").click();

    // Sign up done!
    cy.url().should("include", "private");
  });
  it("can log in to new account", () => {
    cy.login(credentials.getEmail(), credentials.getPassword());
    cy.url().should("include", "private");
  });
});
