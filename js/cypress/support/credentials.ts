import path from "path";

interface SessionData {
  sessions: number[];
}

export class Credentials {
  public static globalSession = 0;

  protected baseEmail: string;

  protected timestamp: string;

  protected password: string;

  protected currentSession = 0;

  protected sessionData: SessionData = { sessions: [0] };

  public constructor() {
    this.baseEmail = `${Cypress.env("BASE_EMAIL")}`;
    this.timestamp = `${Cypress.env("TIMESTAMP")}`;
    this.password = `${Cypress.env("PASSWORD")}`;
    this.currentSession = Credentials.globalSession;
  }

  public static createSessionsFile(): void {
    cy.writeFile(
      path.join(__dirname, "..", "fixtures", "sessions.json"),
      JSON.stringify({ sessions: [] }),
      "utf-8",
    );
  }

  public getEmail(): string {
    const email = this.baseEmail;
    return email.replace(
      "@",
      `${this.getSessionTag()}+prmnttstr${this.timestamp}@`,
    );
  }

  public getPassword(): string {
    return this.password;
  }

  public async loadSession(): Promise<void> {
    await this.readSessionData();
    const { sessions } = this.sessionData;
    this.currentSession = sessions[sessions.length - 1] ?? 0;
    Credentials.globalSession = this.currentSession;
  }

  public setSession(id: number): void {
    const { sessions } = this.sessionData;
    if (!sessions.includes(id)) {
      sessions.push(id);
      this.saveSession();
    }
    this.currentSession = id;
    Credentials.globalSession = id;
  }

  public createNewSession(): void {
    this.currentSession += 1;
    this.sessionData.sessions.push(this.currentSession);
    this.saveSession();
  }

  public resetSessions(): void {
    this.currentSession = 0;
    Credentials.globalSession = 0;
    this.sessionData.sessions = [];
    this.saveSession();
  }

  public getAllSessions(): number[] {
    return this.sessionData.sessions;
  }

  protected getSessionTag(): string {
    if (this.currentSession > 0) {
      return `+${this.currentSession}`;
    }
    return "";
  }

  protected async readSessionData(): Promise<SessionData> {
    return new Promise((resolve, _reject) => {
      cy.readFile(path.join(__dirname, "..", "fixtures", "sessions.json")).then(
        (data) => {
          this.sessionData = data as SessionData;
          resolve(this.sessionData);
        },
      );
    });
  }

  protected saveSession(): void {
    cy.writeFile(
      path.join(__dirname, "..", "fixtures", "sessions.json"),
      JSON.stringify(this.sessionData),
      "utf-8",
    );
  }
}
