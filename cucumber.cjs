module.exports = {
  default: {
    paths: ['automation/gherkin/features/**/*.feature'],
    require: ['automation/gherkin/steps/**/*.cjs'],
    format: ['progress', 'json:reports/generated/cucumber.json'],
    publishQuiet: true,
  },
};
