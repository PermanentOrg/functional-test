# End-to-End Functional Test

The `js` directory contains the in-development replacement for the Permanent Functional Test. It uses end-to-end testing via Cypress to test functionality rather than hitting the API directly.

Currently it exists in a subdirectory since the plan is to eventually completely replace the Python project in this repository, rather than make a new one.

## Setup

Run `npm install` to install dependencies.

### Environment Files

To set the preexisting account used for testing, copy the `cypress.env.json.template` file to `cypress.env.json` and fill in the account information.

### Upload Test Files

To run the upload test suite, you must fetch the test files from AWS. Using the AWS CLI credentials [used in the devenv,](https://github.com/PermanentOrg/devenv) Permanent engineers can fetch the proper testing files and move them into the `files` directory:

```sh
mkdir files
aws s3 cp s3://permanent-repos/test_files/critical-path.zip .
unzip critical-path.zip -d files
rm critical-path.zip
```

## Running Tests

To run headless tests, simply run `npm start`.

To run tests in the Cypress UI, run `npm run cypress:open`.

By default, the functional test is configured to run on the local web-app proxy. To point it to a specific environment when running locally, use the `CYPRESS_BASE_URL` environment variable when running the tests:

```sh
CYPRESS_BASE_URL=https://local.permanent.org npm run start
```
