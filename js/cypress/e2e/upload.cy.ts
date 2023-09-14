import Conversions from "../fixtures/expected-conversions.json";
import TestFiles from "../fixtures/file-upload-data.json";

interface TestFile {
  filename: string;
  extension: string;
  type: string;
}

interface ExpectedConversion {
  type: string;
  extension: string;
  convertTime?: number;
}

const conversions: ExpectedConversion[] = Conversions as ExpectedConversion[];
const testFiles: TestFile[] = TestFiles as TestFile[];
const defaultConversionTime = 25000;

before(() => {
  loginWithAccount();
  cy.intercept("POST", "api/folder/navigateMin").as("navigate");
  cy.visit("/app/private");
  cy.wait("@navigate");
  cy.wait("@navigate");
  cy.window().then((windowObj) => {
    if (windowObj.document.querySelectorAll("pr-file-list-item").length > 0) {
      deleteFiles();
    }
  });
});

describe("upload spec", () => {
  beforeEach(() => {
    loginWithAccount();
  });
  after(() => {
    deleteFiles();
  });

  testFiles.forEach((file: TestFile) => {
    it(`can upload: ${file.extension}`, () => {
      testUploadFileAndConversion(file);
    });
  });

  function testUploadFileAndConversion(file: TestFile): void {
    uploadFile(file.filename, file.extension);
    waitForUploadAndConversion(getExpectedConversionTime(file));
    expectFileIsInFileList(file.filename);
    expectConversionToFormat(
      file.filename,
      file.extension,
      getExpectedConversionExtension(file),
    );
    disambiguateFilename(file.filename, file.extension);
  }
  function uploadFile(filename: string, extension: string): void {
    cy.get("pr-upload-button.full-width input").selectFile(
      `files/${filename}.${extension}`,
      { force: true },
    );
  }
  function waitForUploadAndConversion(expectedConversionTime: number): void {
    cy.wait("@getLeanItems", {
      timeout: 30000,
    }).then(() => {
      // Processing is completely opaque to the web-app, so we just have to sleep for an arbitrary time
      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(expectedConversionTime);
    });
  }
  function expectFileIsInFileList(filename: string): void {
    cy.get("pr-file-list-item").contains(filename).should("exist");
  }
  function expectConversionToFormat(
    filename: string,
    extension: string,
    conversionExtension: string,
  ): void {
    cy.get("pr-file-list-item").contains(filename).click();
    cy.get("label")
      .contains("Original Format")
      .siblings()
      .should("contain.text", extension);
    cy.get("label")
      .contains("Permanent Format")
      .siblings()
      .should("contain.text", conversionExtension);
  }
  function disambiguateFilename(filename: string, extension: string): void {
    cy.intercept("POST", "/api/record/update").as("updateRecord");
    cy.get("label")
      .contains("Name")
      .siblings()
      .filter("pr-inline-value-edit")
      .click();
    cy.get("input[name='text']").clear();
    cy.get("input[name='text']").type(`[PASSED] ${extension}: ${filename}`);
    cy.get("button[name='save']").click();
    cy.wait("@updateRecord");
  }
  function getExpectedConversionTime(file: TestFile): number {
    return (
      conversions.find((obj: ExpectedConversion) => obj.type === file.type)
        ?.convertTime ?? defaultConversionTime
    );
  }
  function getExpectedConversionExtension(file: TestFile): string {
    return (
      conversions.find((obj: ExpectedConversion) => obj.type === file.type)
        ?.extension ?? file.type
    );
  }
});

function loginWithAccount(): void {
  cy.intercept("POST", "api/folder/getLeanItems").as("getLeanItems");
  const email = `${Cypress.env("accountEmail")}`;
  const password = `${Cypress.env("accountPassword")}`;
  cy.login(email, password);
  cy.visit("/app/private");
}

function deleteFiles(): void {
  cy.get("pr-file-list-item").first().click();
  cy.get("pr-file-list-item").last().click({ shiftKey: true });
  cy.get("span").contains("Delete").parent().click();
  cy.get("pr-prompt .btn-primary").click();
}
