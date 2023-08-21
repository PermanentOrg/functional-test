const path = require("path");

module.exports = {
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: path.join(__dirname, "tsconfig.json"),
  },
  plugins: ["@typescript-eslint", "import", "prettier", "cypress"],
  extends: [
    "plugin:@typescript-eslint/all",
    "airbnb-base",
    "airbnb-typescript/base",
    "prettier",
    "plugin:cypress/recommended",
  ],
  rules: {
    "import/prefer-default-export": "off",
    "import/no-default-export": "off",
    "@typescript-eslint/prefer-readonly-parameter-types": "off",
    "prettier/prettier": "error",
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    "@typescript-eslint/no-unused-expressions": "off",
    "@typescript-eslint/no-namespace": "off",
    "@typescript-eslint/no-extraneous-class": "off",
    "cypress/no-async-tests": "off",
    "no-restricted-syntax": "off",
  },
  ignorePatterns: [".eslintrc.js"],
  env: {
    es6: true,
    node: true,
  },
};
