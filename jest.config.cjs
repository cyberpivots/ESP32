module.exports = {
  preset: "react-native",
  testMatch: [
    "<rootDir>/apps/**/__tests__/**/*.test.ts?(x)",
    "<rootDir>/packages/**/__tests__/**/*.test.ts?(x)"
  ],
  transform: {
    "^.+\\.[jt]sx?$": ["babel-jest", { presets: ["babel-preset-expo"] }]
  },
  transformIgnorePatterns: [
    "node_modules/(?!((jest-)?react-native|@react-native|react-native|@testing-library/react-native)/)"
  ],
  moduleNameMapper: {
    "^@cbbs/evidence$": "<rootDir>/packages/cbbs-evidence/src",
    "^@cbbs/fixtures$": "<rootDir>/packages/cbbs-fixtures/src",
    "^@cbbs/product$": "<rootDir>/packages/cbbs-product/src",
    "^@cbbs/product-ui$": "<rootDir>/packages/cbbs-product-ui/src",
    "^@cbbs/protocol$": "<rootDir>/packages/cbbs-protocol/src",
    "^@cbbs/state$": "<rootDir>/packages/cbbs-state/src",
    "^@cbbs/theme$": "<rootDir>/packages/cbbs-theme/src",
    "^@cbbs/ui$": "<rootDir>/packages/cbbs-ui/src"
  }
};
