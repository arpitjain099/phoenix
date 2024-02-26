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
			files: ["./**/*.js"],
		},
	],
	plugins: ["react", "react-hooks", "prettier", "@typescript-eslint"],
	rules: {
		"@typescript-eslint/ban-types": "off",
		"@typescript-eslint/interface-name-prefix": "off",
		"@typescript-eslint/explicit-function-return-type": "off",
		"@typescript-eslint/no-explicit-any": "off",
		"react/prop-types": "off",
		"react/react-in-jsx-scope": "off",
		"no-unused-vars": "off",
		"@typescript-eslint/no-unused-vars": [
			"warn",
			{
				argsIgnorePattern: "^_",
				varsIgnorePattern: "^_",
			},
		],
		"arrow-body-style": ["error", "as-needed"],
		"react/jsx-props-no-spreading": "off",
		"react-hooks/exhaustive-deps": "error",
	},
};
