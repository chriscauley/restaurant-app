module.exports = {
  env: {
    node: true,
  },

  extends: ['plugin:vue/vue3-essential', 'eslint:recommended', 'plugin:prettier/recommended'],

  parserOptions: {
    parser: 'babel-eslint',
  },

  rules: {
    'no-console': ['error', { allow: ['warn', 'error'] }],
    'prettier/prettier': [
      'error',
      {
        singleQuote: true,
        trailingComma: 'all',
        semi: false,
        printWidth: 100,
      },
    ],
    'no-unused-vars': [
      'error',
      {
        argsIgnorePattern: '^_',
      },
    ],
  },

  overrides: [
    {
      files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
      env: {
        jest: true,
      },
    },
  ],

  globals: {
    jest: 'readonly',
  },
}
