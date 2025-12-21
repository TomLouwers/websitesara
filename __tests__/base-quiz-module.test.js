/**
 * Unit tests for BaseQuizModule
 */

const { BaseQuizModule } = require('../static/src/utils.js');

describe('BaseQuizModule', () => {
  let quiz;

  beforeEach(() => {
    quiz = new BaseQuizModule({
      storagePrefix: 'test_quiz_',
      enableProgressTracking: true
    });
  });

  describe('constructor', () => {
    test('should initialize with default state', () => {
      expect(quiz.state.data).toEqual([]);
      expect(quiz.state.currentIndex).toBe(0);
      expect(quiz.state.score).toBe(0);
      expect(quiz.state.totalQuestions).toBe(0);
      expect(quiz.state.currentItem).toBeNull();
      expect(quiz.state.hasAnswered).toBe(false);
      expect(quiz.state.wrongAnswers).toEqual([]);
      expect(quiz.state.startTime).toBeNull();
      expect(quiz.state.endTime).toBeNull();
    });

    test('should apply custom config', () => {
      const customQuiz = new BaseQuizModule({
        storagePrefix: 'custom_',
        enableProgressTracking: false
      });

      expect(customQuiz.config.storagePrefix).toBe('custom_');
      expect(customQuiz.config.enableProgressTracking).toBe(false);
    });

    test('should use default config values when not provided', () => {
      const defaultQuiz = new BaseQuizModule();
      expect(defaultQuiz.config.storagePrefix).toBe('quiz_');
      expect(defaultQuiz.config.enableProgressTracking).toBe(true);
    });

    test('should initialize empty elements object', () => {
      expect(quiz.elements).toEqual({});
    });
  });

  describe('initialize()', () => {
    test('should set quiz data', () => {
      const data = [
        { question: 'Q1', answer: 'A1' },
        { question: 'Q2', answer: 'A2' }
      ];

      quiz.initialize(data);

      expect(quiz.state.data).toBe(data);
      expect(quiz.state.totalQuestions).toBe(2);
    });

    test('should reset state values', () => {
      quiz.state.score = 5;
      quiz.state.currentIndex = 3;
      quiz.state.wrongAnswers = [{ item: 'test' }];

      quiz.initialize([{ q: '1' }, { q: '2' }]);

      expect(quiz.state.score).toBe(0);
      expect(quiz.state.currentIndex).toBe(0);
      expect(quiz.state.wrongAnswers).toEqual([]);
    });

    test('should set startTime', () => {
      const beforeTime = Date.now();
      quiz.initialize([{ q: '1' }]);
      const afterTime = Date.now();

      expect(quiz.state.startTime).toBeGreaterThanOrEqual(beforeTime);
      expect(quiz.state.startTime).toBeLessThanOrEqual(afterTime);
    });

    test('should load current item', () => {
      const data = [
        { question: 'Q1', answer: 'A1' },
        { question: 'Q2', answer: 'A2' }
      ];

      quiz.initialize(data);

      expect(quiz.state.currentItem).toBe(data[0]);
    });
  });

  describe('loadCurrentItem()', () => {
    beforeEach(() => {
      quiz.initialize([
        { q: '1', a: 'A1' },
        { q: '2', a: 'A2' },
        { q: '3', a: 'A3' }
      ]);
    });

    test('should load item at current index', () => {
      quiz.state.currentIndex = 1;
      const item = quiz.loadCurrentItem();

      expect(item).toEqual({ q: '2', a: 'A2' });
      expect(quiz.state.currentItem).toEqual({ q: '2', a: 'A2' });
    });

    test('should reset hasAnswered flag', () => {
      quiz.state.hasAnswered = true;
      quiz.loadCurrentItem();

      expect(quiz.state.hasAnswered).toBe(false);
    });

    test('should return null if index is out of bounds', () => {
      quiz.state.currentIndex = 10;
      const item = quiz.loadCurrentItem();

      expect(item).toBeNull();
    });
  });

  describe('nextItem()', () => {
    beforeEach(() => {
      quiz.initialize([{ q: '1' }, { q: '2' }, { q: '3' }]);
    });

    test('should increment currentIndex', () => {
      expect(quiz.state.currentIndex).toBe(0);
      quiz.nextItem();
      expect(quiz.state.currentIndex).toBe(1);
    });

    test('should load next item', () => {
      quiz.nextItem();
      expect(quiz.state.currentItem).toEqual({ q: '2' });
    });

    test('should return true if more items exist', () => {
      const hasMore = quiz.nextItem();
      expect(hasMore).toBe(true);
    });

    test('should return false when reaching end', () => {
      quiz.state.currentIndex = 2;
      const hasMore = quiz.nextItem();
      expect(hasMore).toBe(false);
    });

    test('should set endTime when reaching end', () => {
      quiz.state.currentIndex = 2;
      const beforeTime = Date.now();
      quiz.nextItem();
      const afterTime = Date.now();

      expect(quiz.state.endTime).toBeGreaterThanOrEqual(beforeTime);
      expect(quiz.state.endTime).toBeLessThanOrEqual(afterTime);
    });
  });

  describe('checkAnswer()', () => {
    beforeEach(() => {
      quiz.initialize([{ question: 'Q1', answer: 'correct' }]);
    });

    test('should return true for correct answer', () => {
      const result = quiz.checkAnswer('correct', 'correct');
      expect(result).toBe(true);
      expect(quiz.state.score).toBe(1);
    });

    test('should return false for incorrect answer', () => {
      const result = quiz.checkAnswer('wrong', 'correct');
      expect(result).toBe(false);
      expect(quiz.state.score).toBe(0);
    });

    test('should be case-insensitive by default', () => {
      const result = quiz.checkAnswer('CORRECT', 'correct');
      expect(result).toBe(true);
    });

    test('should be case-sensitive when specified', () => {
      const result = quiz.checkAnswer('CORRECT', 'correct', true);
      expect(result).toBe(false);
    });

    test('should trim whitespace', () => {
      const result = quiz.checkAnswer('  correct  ', 'correct');
      expect(result).toBe(true);
    });

    test('should set hasAnswered flag', () => {
      quiz.checkAnswer('correct', 'correct');
      expect(quiz.state.hasAnswered).toBe(true);
    });

    test('should return false if already answered', () => {
      quiz.checkAnswer('correct', 'correct');
      const result = quiz.checkAnswer('correct', 'correct');
      expect(result).toBe(false);
    });

    test('should track wrong answers', () => {
      quiz.checkAnswer('wrong', 'correct');

      expect(quiz.state.wrongAnswers).toHaveLength(1);
      expect(quiz.state.wrongAnswers[0]).toEqual({
        index: 0,
        item: quiz.state.currentItem,
        userAnswer: 'wrong',
        correctAnswer: 'correct'
      });
    });

    test('should not track correct answers in wrongAnswers', () => {
      quiz.checkAnswer('correct', 'correct');
      expect(quiz.state.wrongAnswers).toHaveLength(0);
    });
  });

  describe('updateProgress()', () => {
    test('should update progress text element', () => {
      const progressText = document.createElement('div');
      quiz.elements.progressText = progressText;

      quiz.initialize([{ q: '1' }, { q: '2' }, { q: '3' }]);
      quiz.state.currentIndex = 1;
      quiz.updateProgress();

      expect(progressText.textContent).toBe('2 / 3');
    });

    test('should update progress bar width', () => {
      const progressBar = document.createElement('div');
      quiz.elements.progressBar = progressBar;

      quiz.initialize([{ q: '1' }, { q: '2' }, { q: '3' }, { q: '4' }]);
      quiz.state.currentIndex = 1;
      quiz.updateProgress();

      expect(progressBar.style.width).toBe('50%');
    });

    test('should handle missing elements gracefully', () => {
      quiz.elements.progressText = null;
      quiz.elements.progressBar = null;

      expect(() => quiz.updateProgress()).not.toThrow();
    });
  });

  describe('updateScore()', () => {
    test('should update score text element', () => {
      const scoreText = document.createElement('div');
      quiz.elements.scoreText = scoreText;

      quiz.initialize([{ q: '1' }, { q: '2' }, { q: '3' }]);
      quiz.state.score = 2;
      quiz.updateScore();

      expect(scoreText.textContent).toBe('2 / 3');
    });

    test('should handle missing element gracefully', () => {
      quiz.elements.scoreText = null;
      expect(() => quiz.updateScore()).not.toThrow();
    });
  });

  describe('getResults()', () => {
    test('should calculate percentage correctly', () => {
      quiz.initialize([{ q: '1' }, { q: '2' }, { q: '3' }, { q: '4' }]);
      quiz.state.score = 3;
      quiz.state.endTime = Date.now();

      const results = quiz.getResults();

      expect(results.percentage).toBe(75);
    });

    test('should include all result data', () => {
      quiz.initialize([{ q: '1' }, { q: '2' }]);
      quiz.state.score = 1;
      quiz.state.wrongAnswers = [{ index: 1 }];
      quiz.state.endTime = Date.now();

      const results = quiz.getResults();

      expect(results.score).toBe(1);
      expect(results.total).toBe(2);
      expect(results.percentage).toBe(50);
      expect(results.wrongAnswers).toEqual([{ index: 1 }]);
      expect(results.duration).toBeGreaterThanOrEqual(0);
      expect(results.timestamp).toBeDefined();
    });

    test('should calculate duration correctly', () => {
      quiz.state.startTime = 1000;
      quiz.state.endTime = 5000;

      const results = quiz.getResults();

      expect(results.duration).toBe(4000);
    });

    test('should handle null endTime', () => {
      quiz.initialize([{ q: '1' }]);
      quiz.state.endTime = null;

      const results = quiz.getResults();

      expect(results.duration).toBe(0);
    });
  });

  describe('saveProgress()', () => {
    test('should save progress to storage when enabled', () => {
      const mockStorage = {
        set: jest.fn()
      };
      global.storage = mockStorage;

      quiz.config.enableProgressTracking = true;
      quiz.state.currentIndex = 2;
      quiz.state.score = 1;
      quiz.state.wrongAnswers = [{ index: 1 }];

      quiz.saveProgress();

      expect(mockStorage.set).toHaveBeenCalledWith(
        'test_quiz_progress',
        expect.objectContaining({
          currentIndex: 2,
          score: 1,
          wrongAnswers: [{ index: 1 }],
          timestamp: expect.any(Number)
        })
      );
    });

    test('should not save when progress tracking is disabled', () => {
      const mockStorage = {
        set: jest.fn()
      };
      global.storage = mockStorage;

      quiz.config.enableProgressTracking = false;
      quiz.saveProgress();

      expect(mockStorage.set).not.toHaveBeenCalled();
    });
  });

  describe('loadProgress()', () => {
    test('should load progress from storage when enabled', () => {
      const savedProgress = {
        currentIndex: 3,
        score: 2,
        wrongAnswers: [],
        timestamp: Date.now()
      };

      const mockStorage = {
        get: jest.fn(() => savedProgress)
      };
      global.storage = mockStorage;

      quiz.config.enableProgressTracking = true;
      const result = quiz.loadProgress();

      expect(mockStorage.get).toHaveBeenCalledWith('test_quiz_progress');
      expect(result).toEqual(savedProgress);
    });

    test('should return null when progress tracking is disabled', () => {
      quiz.config.enableProgressTracking = false;
      const result = quiz.loadProgress();

      expect(result).toBeNull();
    });
  });

  describe('clearProgress()', () => {
    test('should remove progress from storage', () => {
      const mockStorage = {
        remove: jest.fn()
      };
      global.storage = mockStorage;

      quiz.clearProgress();

      expect(mockStorage.remove).toHaveBeenCalledWith('test_quiz_progress');
    });
  });

  describe('reset()', () => {
    test('should reset all state values', () => {
      quiz.initialize([{ q: '1' }, { q: '2' }]);
      quiz.state.currentIndex = 1;
      quiz.state.score = 1;
      quiz.state.wrongAnswers = [{ index: 0 }];
      quiz.state.hasAnswered = true;
      quiz.state.endTime = Date.now();

      quiz.reset();

      expect(quiz.state.currentIndex).toBe(0);
      expect(quiz.state.score).toBe(0);
      expect(quiz.state.wrongAnswers).toEqual([]);
      expect(quiz.state.hasAnswered).toBe(false);
      expect(quiz.state.endTime).toBeNull();
    });

    test('should set new startTime', () => {
      quiz.initialize([{ q: '1' }]);
      const oldStartTime = quiz.state.startTime;

      // Wait a bit
      const wait = () => new Promise(resolve => setTimeout(resolve, 10));
      return wait().then(() => {
        quiz.reset();
        expect(quiz.state.startTime).toBeGreaterThan(oldStartTime);
      });
    });

    test('should load first item', () => {
      const data = [{ q: '1' }, { q: '2' }];
      quiz.initialize(data);
      quiz.state.currentIndex = 1;

      quiz.reset();

      expect(quiz.state.currentItem).toBe(data[0]);
    });
  });

  describe('cacheElements()', () => {
    test('should cache elements by ID', () => {
      const element1 = document.createElement('div');
      element1.id = 'test1';
      const element2 = document.createElement('div');
      element2.id = 'test2';

      document.body.appendChild(element1);
      document.body.appendChild(element2);

      quiz.cacheElements({
        elem1: 'test1',
        elem2: 'test2'
      });

      expect(quiz.elements.elem1).toBe(element1);
      expect(quiz.elements.elem2).toBe(element2);

      document.body.removeChild(element1);
      document.body.removeChild(element2);
    });

    test('should handle missing elements', () => {
      quiz.cacheElements({
        missing: 'nonexistent'
      });

      expect(quiz.elements.missing).toBeNull();
    });
  });
});
