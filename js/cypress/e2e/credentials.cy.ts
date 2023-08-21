import { Credentials } from "../support/credentials";

describe("Sessions + Credentials", () => {
  before(() => {
    Credentials.createSessionsFile();
  });
  beforeEach(() => {
    Cypress.env("BASE_EMAIL", "test@invalid.test");
    Cypress.env("TIMESTAMP", "123456789");
    Cypress.env("PASSWORD", "testpassword");
  });
  afterEach(() => {
    new Credentials().resetSessions();
  });
  it("should be able to get email env", () => {
    const credentials = new Credentials();
    expect(credentials.getEmail()).to.equal(
      "test+prmnttstr123456789@invalid.test",
    );
  });
  it("should be able to get password from env", () => {
    const credentials = new Credentials();
    expect(credentials.getPassword()).to.equal("testpassword");
  });
  it("should be able to create a new session", () => {
    const credentials = new Credentials();
    credentials.createNewSession();
    expect(credentials.getEmail()).to.equal(
      "test+1+prmnttstr123456789@invalid.test",
    );
    credentials.resetSessions();
  });
  it("should be able to completely clear out sessions", () => {
    const credentials = new Credentials();
    credentials.createNewSession();
    credentials.createNewSession();
    credentials.createNewSession();
    credentials.createNewSession();
    credentials.createNewSession();
    credentials.resetSessions();
    expect(credentials.getEmail()).to.equal(
      "test+prmnttstr123456789@invalid.test",
    );
  });
  it("should be able to get all sessions (for iterating over all of them)", () => {
    const credentials = new Credentials();
    credentials.resetSessions();
    credentials.createNewSession();
    credentials.createNewSession();
    credentials.createNewSession();
    const sessions = credentials.getAllSessions();
    expect(sessions).to.have.lengthOf(3);
    credentials.setSession(2);
    expect(credentials.getEmail()).to.equal(
      "test+2+prmnttstr123456789@invalid.test",
    );
  });
  it("should persist sessions between test specs", async () => {
    const credentials = new Credentials();
    credentials.createNewSession();
    const credentials2 = new Credentials();
    await credentials2.loadSession();
    expect(credentials2.getEmail()).to.equal(
      "test+1+prmnttstr123456789@invalid.test",
    );
    credentials.resetSessions();
  });
});
