# End-to-End Functional Test

The `js` directory contains the in-development replacement for the Permanent Functional Test. It uses end-to-end testing via Cypress to test functionality rather than hitting the API directly.

Currently it exists in a subdirectory since the plan is to eventually completely replace the Python project in this repository, rather than make a new one.

## Setup

Run `npm install` to install dependencies.

## Running Tests

To run headless tests, simply run `npm start`.

To run tests in the Cypress UI, run `npm run cypress:open`.
