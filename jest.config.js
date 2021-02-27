module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  testPathIgnorePatterns: ["/node_modules/", "/examples/"],
  moduleNameMapper: {
    "@radiant-voices(.*)$": "<rootDir>/src/ts$1",
  },
}
