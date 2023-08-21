import { Credentials } from "./credentials";

declare global {
  namespace Cypress {
    interface Chainable {
      login: (email?: string, password?: string) => Chainable<void>;
    }
  }
}

Cypress.Commands.add("login", (email?: string, password?: string) => {
  const credentials = new Credentials();
  cy.visit(`/app/auth`);
  cy.get('input[name="email"]').type(email ?? credentials.getEmail());
  cy.get('input[name="password"]').type(password ?? credentials.getPassword());
  cy.get("#rememberMe").click();
  cy.get('button[type="submit"]').click();
});
