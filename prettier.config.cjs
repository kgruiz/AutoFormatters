// prettier.config.cjs

const basePlugins = [
    "prettier-plugin-multiline-arrays",
    "prettier-plugin-organize-imports",
    "@huggingface/prettier-plugin-vertical-align",
    "@trivago/prettier-plugin-sort-imports",
];

module.exports = {
    printWidth: 80,
    tabWidth: 4,
    useTabs: false,
    endOfLine: "lf",
    quoteProps: "consistent",
    proseWrap: "preserve",
    htmlWhitespaceSensitivity: "css",
    bracketSpacing: true,
    trailingComma: "all",
    singleAttributePerLine: true,
    arrowParens: "always",
    semi: true,
    singleQuote: false,
    jsxSingleQuote: false,
    experimentalOperatorPosition: "end",
    plugins: basePlugins,
    multilineArraysWrapThreshold: 0,
    multilineArraysLinePattern: "1",
};
