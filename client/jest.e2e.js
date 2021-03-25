module.exports = {
  moduleNameMapper: {
    '@/(.*)$': '<rootDir>/src/$1',
    '@tests/(.*)$': '<rootDir>/tests/$1',
  },
  testMatch: ['<rootDir>/tests/e2e/*.spec.js'],
  preset: '@vue/cli-plugin-unit-jest',
  setupFiles: [],
  transform: {
    '^.+\\.vue$': 'vue-jest',
  },
  testEnvironment: 'node',
}
