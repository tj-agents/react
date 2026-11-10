import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default [
  { ignores: ["node_modules/**", "dist/**", "build/**"] },
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      "@typescript-eslint": tseslint.plugin,
      "react-hooks": reactHooks,
    },
    rules: {
      "@typescript-eslint/consistent-type-definitions": ["error", "interface"],
      "@typescript-eslint/naming-convention": [
        "error",
        {
          selector: "typeProperty",
          format: ["camelCase"],
          filter: { regex: "^\\$type$", match: false },
        },
      ],
      "@typescript-eslint/switch-exhaustiveness-check": "error",
      "no-restricted-syntax": [
        "error",
        {
          selector: "TSTypeAliasDeclaration > TSIntersectionType",
          message: "Extend object shapes with an interface instead of an intersection.",
        },
      ],
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "error",
    },
  },
];
