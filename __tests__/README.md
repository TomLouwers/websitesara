# Test Suite Documentation

## Overview

This directory contains comprehensive unit tests for the OefenPlatform JavaScript modules using Jest.

## Test Coverage

Current coverage for `utils.js`:
- **Statements**: 82.84%
- **Branches**: 75%
- **Functions**: 74.5%
- **Lines**: 84.37%

## Test Files

### Core Module Tests

1. **`storage-manager.test.js`** - 39 tests
   - Tests for `StorageManager` class
   - Covers caching, batched writes, localStorage operations
   - Tests error handling and edge cases

2. **`audio-manager.test.js`** - 17 tests
   - Tests for `AudioManager` class
   - Covers audio playback, TTS fallback, error handling
   - Tests sequential and concurrent audio playback

3. **`base-quiz-module.test.js`** - 43 tests
   - Tests for `BaseQuizModule` class
   - Covers quiz state management, scoring, progress tracking
   - Tests inheritance pattern and configuration

4. **`spelling-dictee.test.js`** - 28 tests
   - Integration tests for `SpellingDictee` class
   - Tests answer normalization, tag tracking, results calculation
   - Tests verb tense handling and extra info display

### Setup Files

- **`setup.js`** - Global test configuration
  - Mocks for localStorage, Audio API, SpeechSynthesis
  - Global storage and CONFIG objects
  - Console suppression for cleaner test output

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in watch mode
```bash
npm run test:watch
```

### Run tests with coverage
```bash
npm run test:coverage
```

### Run tests with verbose output
```bash
npm run test:verbose
```

## Test Results

**Total**: 136 tests
- ✅ **Passing**: 127 tests (93.4%)
- ❌ **Failing**: 9 tests (6.6% - edge cases and error handling)

## What's Tested

### StorageManager
- ✅ Get/set/remove operations
- ✅ Value parsing (JSON, booleans, numbers)
- ✅ Caching mechanism
- ✅ Batched writes with automatic flushing
- ✅ Cache and storage clearing
- ⚠️ Error handling (2 tests pending)

### AudioManager
- ✅ Audio file playback with TTS fallback
- ✅ Progress callbacks
- ✅ Stop functionality
- ✅ Sequential playback
- ⚠️ Advanced error scenarios (4 tests pending)

### BaseQuizModule
- ✅ State initialization and management
- ✅ Quiz data loading and iteration
- ✅ Answer checking (case-sensitive/insensitive)
- ✅ Score and progress tracking
- ✅ Results calculation
- ✅ Element caching
- ⚠️ Progress persistence (3 tests pending)

### SpellingDictee
- ✅ Data loading from API
- ✅ Answer normalization with flags
- ✅ Tag statistics tracking
- ✅ Verb tense instruction mapping
- ✅ Results calculation and categorization
- ✅ Audio path construction
- ✅ Extra info handling

## Coverage Thresholds

The project maintains the following coverage thresholds for `utils.js`:
- Branches: 70%
- Functions: 70%
- Lines: 80%
- Statements: 80%

All thresholds are currently **exceeded** ✅

## Future Improvements

1. **Fix remaining 9 edge case tests** for error handling scenarios
2. **Add tests for other modules**:
   - `app.js` (main quiz application)
   - `spelling-quiz.js` (refactored spelling quiz)
   - `dmt-practice.js` (DMT practice module)
   - `foutanalyse-modaal.js` (error analysis modal)
3. **Add integration tests** for complete user flows
4. **Add E2E tests** with Playwright or Cypress
5. **Set up CI/CD** to run tests automatically on push

## Notes

- Tests use `jsdom` environment to simulate browser APIs
- All async operations are properly awaited
- Mocks are reset between tests to ensure isolation
- Console output is suppressed for cleaner test runs
