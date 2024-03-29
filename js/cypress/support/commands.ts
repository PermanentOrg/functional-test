declare global {
  namespace Cypress {
    interface Chainable {
      login: (email: string, password: string) => Chainable<void>;
    }
  }
}

Cypress.Commands.add("login", (email: string, password: string) => {
  cy.visit(`/app/auth`);
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.get("#rememberMe").uncheck();
  cy.get('button[type="submit"]').click();
});

// We need an import or export for TypeScript to recognize this file as a module
export {};
