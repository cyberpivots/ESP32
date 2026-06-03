import expoConfig from "eslint-config-expo/flat.js";
import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";

export default [
  ...expoConfig,
  {
    ignores: ["dist/**", "node_modules/**", "coverage/**"]
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: false
      }
    },
    plugins: {
      "@typescript-eslint": tsPlugin
    },
    rules: {
      "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
      "import/no-unresolved": "off",
      "no-restricted-globals": ["error", "fetch", "WebSocket"]
    }
  }
];
