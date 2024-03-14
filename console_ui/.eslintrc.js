module.exports = {
	extends: [
		"airbnb",
		"airbnb-typescript",
		"airbnb/hooks",
		"next/core-web-vitals",
		"plugin:react/recommended",
		"plugin:@typescript-eslint/recommended",
		"prettier",
	],
	parser: "@typescript-eslint/parser",
	root: true,
	parserOptions: {
		project: "tsconfig.eslint.json",
		tsconfigRootDir: __dirname,
		sourceType: "module",
	},
	overrides: [
		{
			files: ["*.js"],
			rules: {
				"@typescript-eslint/no-var-requires": "off",
			},
		},
		{
			extends: ["plugin:@typescript-eslint/disable-type-checked"],
			files: ["./**/*.js", "./**/*.ts", "./**/*.tsx"],
		},
	],
	plugins: ["react", "react-hooks", "prettier", "@typescript-eslint"],
	settings: {
		"import/resolver": {
			node: {
				extensions: [".js", ".jsx", ".ts", ".tsx"],
				paths: ["./src"],
			},
		},
	},
	rules: {
		"@typescript-eslint/ban-types": "off",
		"@typescript-eslint/explicit-function-return-type": "off",
		"@typescript-eslint/interface-name-prefix": "off",
		"@typescript-eslint/naming-convention": [
			"error",
			{
				selector: "memberLike",
				modifiers: ["private"],
				format: ["camelCase"],
				leadingUnderscore: "require",
			},
		],
		"@typescript-eslint/no-explicit-any": "off",
		"@typescript-eslint/no-unused-vars": [
			"warn",
			{
				argsIgnorePattern: "^_",
				varsIgnorePattern: "^_",
			},
		],
		"react/prop-types": "off",
		"react/react-in-jsx-scope": "off",
		"no-nested-ternary": "off",
		"no-unused-vars": "off",
		"arrow-body-style": ["error", "as-needed"],
		"react/jsx-props-no-spreading": "off",
		"react/function-component-definition": [
			2,
			{
				namedComponents: [
					"function-declaration",
					"function-expression",
					"arrow-function",
				],
				unnamedComponents: ["function-expression", "arrow-function"],
			},
		],
		"react/no-unstable-nested-components": [
			"warn",
			{
				allowAsProps: true,
			},
		],
		"react-hooks/exhaustive-deps": "error",
	},
};
