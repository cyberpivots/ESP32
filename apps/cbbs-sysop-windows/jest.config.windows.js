const config = {
  moduleNameMapper: {
    "^@cbbs/product$": "<rootDir>/../../packages/cbbs-product/src",
    "^@cbbs/product-ui$": "<rootDir>/../../packages/cbbs-product-ui/src",
    "^@cbbs/protocol$": "<rootDir>/../../packages/cbbs-protocol/src"
  },
  transform: {
    "\\.[jt]sx?$": ["babel-jest", { presets: ["module:@react-native/babel-preset"] }]
  }
};

module.exports = require('@rnx-kit/jest-preset')('windows', config);
