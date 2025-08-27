// prettier.config.cjs
const PNPM_GLOBAL = "/Users/kadengruizenga/Library/pnpm/global/5/node_modules";
const R = (m) => require.resolve(m, { paths: [PNPM_GLOBAL] });

const basePlugins = [
    R("prettier-plugin-multiline-arrays"),
    R("prettier-plugin-organize-imports"),
    R("@huggingface/prettier-plugin-vertical-align"),
    R("@trivago/prettier-plugin-sort-imports"),
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
