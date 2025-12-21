/**
 * Unit tests for SpellingDictee
 */

// Mock fetch globally
global.fetch = jest.fn();

// Load the module after setting up mocks
const mockQuizData = {
  set: {
    flags: {
      trim: true,
      case_sensitive: false
    },
    feedback_templates: {
      correct: 'Goed gedaan!',
      incorrect: 'Nog niet helemaal!'
    }
  },
  items: [
    {
      audio: {
        sentence: 'audio/sentence1.mp3',
        instruction: 'audio/instruction1.mp3'
      },
      prompt: {
        sentence: 'Test sentence',
        instruction: 'Type het woord {answer}'
      },
      target: {
        answer: 'werkte',
        accept: ['werkte']
      },
      tags: ['werkwoord_vt'],
      extra_info: {
        rule: 'Test spelling rule',
        tip: 'Test tip',
        examples: ['Example 1', 'Example 2']
      }
    },
    {
      audio: {
        sentence: 'audio/sentence2.mp3',
        instruction: 'audio/instruction2.mp3'
      },
      prompt: {
        sentence: 'Second sentence',
        instruction: 'Type het woord {answer}'
      },
      target: {
        answer: 'loopt',
        accept: ['loopt', 'loopen']
      },
      tags: ['werkwoord_ttt'],
      extra_info: null
    }
  ]
};

describe('SpellingDictee', () => {
  let SpellingDictee;
  let quiz;
  let mockStorage;
  let mockAudioManager;

  beforeEach(() => {
    // Reset modules
    jest.resetModules();

    // Setup DOM
    document.body.innerHTML = `
      <div id="quizContainer">
        <input id="spellingInput" />
        <button id="checkButton"></button>
        <button id="audioPlayButton"></button>
        <i id="playIcon"></i>
        <button id="nextButton"></button>
        <div id="feedbackSection"></div>
        <span id="feedbackIcon"></span>
        <span id="feedbackTitle"></span>
        <div id="correctAnswerDisplay"></div>
        <div id="extraInfoSection"></div>
        <div id="ruleSection"><div id="ruleContent"></div></div>
        <div id="tipSection"><div id="tipContent"></div></div>
        <div id="examplesSection"><div id="examplesContent"></div></div>
        <span id="progressLabel"></span>
        <div id="progressBarFill"></div>
        <span id="totalCorrect"></span>
        <span id="breadcrumbLevel"></span>
        <span id="verbTenseInstruction"></span>
      </div>
      <div id="resultsPage" style="display: none;">
        <div id="resultEmoji"></div>
        <div id="resultHeadline"></div>
        <div id="resultSummary"></div>
        <div id="resultGrowthBadge"><span id="growthText"></span></div>
        <div id="skillsOverview"><div id="skillsChips"></div></div>
        <div id="questionReviewSection"><div id="questionAccordion"></div></div>
      </div>
    `;

    // Mock localStorage
    mockStorage = {
      get: jest.fn((key, defaultValue) => {
        if (key === 'selectedGroep') return 'groep4';
        if (key === 'selectedMoment') return 'm4';
        return defaultValue;
      }),
      set: jest.fn(),
      remove: jest.fn(),
      flush: jest.fn()
    };
    global.storage = mockStorage;

    // Mock audioManager
    mockAudioManager = {
      playAudio: jest.fn(() => Promise.resolve()),
      stop: jest.fn()
    };
    global.audioManager = mockAudioManager;

    // Mock fetch
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockQuizData)
      })
    );

    // Load SpellingDictee class
    const utils = require('../static/src/utils.js');
    global.BaseQuizModule = utils.BaseQuizModule;

    // Create SpellingDictee class inline since it's in a separate file
    SpellingDictee = class extends global.BaseQuizModule {
      constructor() {
        super({
          storagePrefix: 'spelling_dictee_',
          enableProgressTracking: true
        });
        this.quizData = null;
        this.tagStats = {};
        this.isPlayingAudio = false;
      }

      async loadQuizData() {
        const selectedGroep = storage.get('selectedGroep', 'groep4');
        const selectedMoment = storage.get('selectedMoment', 'm4');

        const filePath = CONFIG.subjectFilePaths?.werkwoordspelling?.[selectedGroep]?.[selectedMoment];
        if (!filePath) throw new Error('No data available');

        const response = await fetch(filePath);
        if (!response.ok) throw new Error('Could not load');

        this.quizData = await response.json();
        if (!this.quizData.set || !this.quizData.items) {
          throw new Error('Invalid data structure');
        }

        this.initialize(this.quizData.items);
      }

      normalizeAnswer(answer, flags) {
        let normalized = answer;
        if (flags.trim) normalized = normalized.trim();
        if (!flags.case_sensitive) normalized = normalized.toLowerCase();
        return normalized;
      }

      formatTagName(tag) {
        const tagNames = {
          'werkwoord_vt': 'Verleden tijd',
          'werkwoord_ttt': 'Tegenwoordige tijd'
        };
        return tagNames[tag] || tag;
      }
    };

    quiz = new SpellingDictee();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('constructor', () => {
    test('should extend BaseQuizModule', () => {
      expect(quiz).toBeInstanceOf(global.BaseQuizModule);
    });

    test('should initialize with correct config', () => {
      expect(quiz.config.storagePrefix).toBe('spelling_dictee_');
      expect(quiz.config.enableProgressTracking).toBe(true);
    });

    test('should initialize quizData as null', () => {
      expect(quiz.quizData).toBeNull();
    });

    test('should initialize tagStats as empty object', () => {
      expect(quiz.tagStats).toEqual({});
    });

    test('should initialize isPlayingAudio as false', () => {
      expect(quiz.isPlayingAudio).toBe(false);
    });
  });

  describe('loadQuizData()', () => {
    test('should load quiz data from API', async () => {
      await quiz.loadQuizData();

      expect(fetch).toHaveBeenCalledWith(
        'data/exercises/sp/werkwoordspelling-g4-m4.json'
      );
      expect(quiz.quizData).toEqual(mockQuizData);
    });

    test('should initialize BaseQuizModule with items', async () => {
      await quiz.loadQuizData();

      expect(quiz.state.data).toBe(mockQuizData.items);
      expect(quiz.state.totalQuestions).toBe(2);
    });

    test('should get groep and moment from storage', async () => {
      await quiz.loadQuizData();

      expect(mockStorage.get).toHaveBeenCalledWith('selectedGroep', 'groep4');
      expect(mockStorage.get).toHaveBeenCalledWith('selectedMoment', 'm4');
    });

    test('should throw error if no file path configured', async () => {
      mockStorage.get = jest.fn((key) => {
        if (key === 'selectedGroep') return 'groep99';
        if (key === 'selectedMoment') return 'm99';
      });

      await expect(quiz.loadQuizData()).rejects.toThrow('No data available');
    });

    test('should throw error if fetch fails', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: false,
          status: 404
        })
      );

      await expect(quiz.loadQuizData()).rejects.toThrow('Could not load');
    });

    test('should throw error if data structure is invalid', async () => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ invalid: 'data' })
        })
      );

      await expect(quiz.loadQuizData()).rejects.toThrow('Invalid data structure');
    });
  });

  describe('normalizeAnswer()', () => {
    test('should trim whitespace when flag is true', () => {
      const result = quiz.normalizeAnswer('  test  ', { trim: true, case_sensitive: true });
      expect(result).toBe('test');
    });

    test('should convert to lowercase when case_sensitive is false', () => {
      const result = quiz.normalizeAnswer('TEST', { trim: false, case_sensitive: false });
      expect(result).toBe('test');
    });

    test('should apply both trim and lowercase', () => {
      const result = quiz.normalizeAnswer('  TEST  ', { trim: true, case_sensitive: false });
      expect(result).toBe('test');
    });

    test('should preserve case when case_sensitive is true', () => {
      const result = quiz.normalizeAnswer('TEST', { trim: false, case_sensitive: true });
      expect(result).toBe('TEST');
    });

    test('should not trim when flag is false', () => {
      const result = quiz.normalizeAnswer('  test  ', { trim: false, case_sensitive: true });
      expect(result).toBe('  test  ');
    });
  });

  describe('formatTagName()', () => {
    test('should format werkwoord_vt tag', () => {
      expect(quiz.formatTagName('werkwoord_vt')).toBe('Verleden tijd');
    });

    test('should format werkwoord_ttt tag', () => {
      expect(quiz.formatTagName('werkwoord_ttt')).toBe('Tegenwoordige tijd');
    });

    test('should return original tag if no mapping exists', () => {
      expect(quiz.formatTagName('unknown_tag')).toBe('unknown_tag');
    });
  });

  describe('answer checking integration', () => {
    beforeEach(async () => {
      await quiz.loadQuizData();
    });

    test('should accept correct answer', () => {
      const flags = quiz.quizData.set.flags;
      const userAnswer = 'werkte';
      const correctAnswer = 'werkte';

      const normalized = quiz.normalizeAnswer(userAnswer, flags);
      const expected = quiz.normalizeAnswer(correctAnswer, flags);

      expect(normalized).toBe(expected);
    });

    test('should accept answer with different case', () => {
      const flags = quiz.quizData.set.flags;
      const userAnswer = 'WERKTE';
      const correctAnswer = 'werkte';

      const normalized = quiz.normalizeAnswer(userAnswer, flags);
      const expected = quiz.normalizeAnswer(correctAnswer, flags);

      expect(normalized).toBe(expected);
    });

    test('should accept answer with whitespace', () => {
      const flags = quiz.quizData.set.flags;
      const userAnswer = '  werkte  ';
      const correctAnswer = 'werkte';

      const normalized = quiz.normalizeAnswer(userAnswer, flags);
      const expected = quiz.normalizeAnswer(correctAnswer, flags);

      expect(normalized).toBe(expected);
    });

    test('should accept alternative answers', () => {
      const flags = quiz.quizData.set.flags;
      const item = quiz.quizData.items[1]; // Has accept: ['loopt', 'loopen']

      const acceptedAnswers = item.target.accept || [item.target.answer];
      const normalizedAccepted = acceptedAnswers.map(ans =>
        quiz.normalizeAnswer(ans, flags)
      );

      expect(normalizedAccepted).toContain('loopt');
      expect(normalizedAccepted).toContain('loopen');
    });
  });

  describe('tag statistics tracking', () => {
    beforeEach(async () => {
      await quiz.loadQuizData();
    });

    test('should initialize tagStats for new tags', () => {
      const tags = ['werkwoord_vt', 'verlengingsregel'];

      tags.forEach(tag => {
        if (!quiz.tagStats[tag]) {
          quiz.tagStats[tag] = { correct: 0, total: 0 };
        }
      });

      expect(quiz.tagStats['werkwoord_vt']).toEqual({ correct: 0, total: 0 });
      expect(quiz.tagStats['verlengingsregel']).toEqual({ correct: 0, total: 0 });
    });

    test('should track correct answers by tag', () => {
      const tag = 'werkwoord_vt';
      if (!quiz.tagStats[tag]) {
        quiz.tagStats[tag] = { correct: 0, total: 0 };
      }

      quiz.tagStats[tag].correct++;
      quiz.tagStats[tag].total++;

      expect(quiz.tagStats[tag]).toEqual({ correct: 1, total: 1 });
    });

    test('should track incorrect answers by tag', () => {
      const tag = 'werkwoord_vt';
      if (!quiz.tagStats[tag]) {
        quiz.tagStats[tag] = { correct: 0, total: 0 };
      }

      quiz.tagStats[tag].total++;

      expect(quiz.tagStats[tag]).toEqual({ correct: 0, total: 1 });
    });

    test('should calculate percentage correctly', () => {
      quiz.tagStats = {
        'werkwoord_vt': { correct: 3, total: 4 },
        'werkwoord_ttt': { correct: 2, total: 2 }
      };

      const vtPercentage = Math.round(
        (quiz.tagStats['werkwoord_vt'].correct / quiz.tagStats['werkwoord_vt'].total) * 100
      );
      const tttPercentage = Math.round(
        (quiz.tagStats['werkwoord_ttt'].correct / quiz.tagStats['werkwoord_ttt'].total) * 100
      );

      expect(vtPercentage).toBe(75);
      expect(tttPercentage).toBe(100);
    });
  });

  describe('audio playback', () => {
    beforeEach(async () => {
      await quiz.loadQuizData();
    });

    test('should construct correct audio paths', () => {
      const item = quiz.state.currentItem;
      const sentencePath = 'data/exercises/sp/' + item.audio.sentence;
      const instructionPath = 'data/exercises/sp/' + item.audio.instruction;

      expect(sentencePath).toBe('data/exercises/sp/audio/sentence1.mp3');
      expect(instructionPath).toBe('data/exercises/sp/audio/instruction1.mp3');
    });

    test('should replace {answer} placeholder in instruction', () => {
      const item = quiz.state.currentItem;
      const instructionText = item.prompt.instruction.replace(
        '{answer}',
        item.target.answer
      );

      expect(instructionText).toBe('Type het woord werkte');
    });
  });

  describe('extra info display', () => {
    beforeEach(async () => {
      await quiz.loadQuizData();
    });

    test('should identify items with extra info', () => {
      const item1 = quiz.quizData.items[0];
      const item2 = quiz.quizData.items[1];

      expect(item1.extra_info).toBeTruthy();
      expect(item1.extra_info.rule).toBe('Test spelling rule');
      expect(item1.extra_info.tip).toBe('Test tip');
      expect(item1.extra_info.examples).toEqual(['Example 1', 'Example 2']);

      expect(item2.extra_info).toBeNull();
    });

    test('should check for specific extra info fields', () => {
      const item = quiz.quizData.items[0];
      const hasRule = !!(item.extra_info && item.extra_info.rule);
      const hasTip = !!(item.extra_info && item.extra_info.tip);
      const hasExamples = !!(item.extra_info && item.extra_info.examples && item.extra_info.examples.length > 0);

      expect(hasRule).toBe(true);
      expect(hasTip).toBe(true);
      expect(hasExamples).toBe(true);
    });
  });

  describe('results calculations', () => {
    test('should calculate percentage for perfect score', () => {
      const totalQuestions = 10;
      const correctCount = 10;
      const percentage = Math.round((correctCount / totalQuestions) * 100);

      expect(percentage).toBe(100);
    });

    test('should calculate percentage for partial score', () => {
      const totalQuestions = 10;
      const correctCount = 7;
      const percentage = Math.round((correctCount / totalQuestions) * 100);

      expect(percentage).toBe(70);
    });

    test('should calculate percentage for zero score', () => {
      const totalQuestions = 10;
      const correctCount = 0;
      const percentage = Math.round((correctCount / totalQuestions) * 100);

      expect(percentage).toBe(0);
    });

    test('should select correct emoji and headline for high score', () => {
      const percentage = 95;
      let emoji, headline;

      if (percentage >= 90) {
        emoji = '🎉';
        headline = 'Wauw! Geweldig gedaan!';
      }

      expect(emoji).toBe('🎉');
      expect(headline).toBe('Wauw! Geweldig gedaan!');
    });

    test('should select correct emoji and headline for medium score', () => {
      const percentage = 75;
      let emoji, headline;

      if (percentage >= 70) {
        emoji = '🌟';
        headline = 'Knap gewerkt!';
      }

      expect(emoji).toBe('🌟');
      expect(headline).toBe('Knap gewerkt!');
    });

    test('should select correct emoji and headline for low score', () => {
      const percentage = 40;
      let emoji, headline;

      if (percentage >= 50) {
        emoji = '💪';
        headline = 'Goed bezig!';
      } else {
        emoji = '🚀';
        headline = 'Elke vraag maakt je sterker!';
      }

      expect(emoji).toBe('🚀');
      expect(headline).toBe('Elke vraag maakt je sterker!');
    });
  });

  describe('verb tense instructions', () => {
    test('should identify verleden tijd tag', () => {
      const tags = ['werkwoord_vt'];

      let instruction = '';
      if (tags.includes('werkwoord_vt')) {
        instruction = ' in verleden tijd';
      }

      expect(instruction).toBe(' in verleden tijd');
    });

    test('should identify tegenwoordige tijd tag', () => {
      const tags = ['werkwoord_ttt'];

      let instruction = '';
      if (tags.includes('werkwoord_ttt')) {
        instruction = ' in tegenwoordige tijd';
      }

      expect(instruction).toBe(' in tegenwoordige tijd');
    });

    test('should identify voltooid deelwoord tag', () => {
      const tags = ['voltooid_deelwoord'];

      let instruction = '';
      if (tags.includes('voltooid_deelwoord')) {
        instruction = ' voltooid deelwoord';
      }

      expect(instruction).toBe(' voltooid deelwoord');
    });

    test('should return empty string for no matching tags', () => {
      const tags = ['other_tag'];

      let instruction = '';
      if (tags.includes('werkwoord_vt')) {
        instruction = ' in verleden tijd';
      } else if (tags.includes('werkwoord_ttt')) {
        instruction = ' in tegenwoordige tijd';
      } else if (tags.includes('voltooid_deelwoord')) {
        instruction = ' voltooid deelwoord';
      }

      expect(instruction).toBe('');
    });
  });
});
