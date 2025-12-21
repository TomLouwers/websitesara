/**
 * Jest setup file
 * Configures global test environment and mocks
 */

// Mock localStorage
class LocalStorageMock {
  constructor() {
    this.store = {};
  }

  clear() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key] || null;
  }

  setItem(key, value) {
    this.store[key] = String(value);
  }

  removeItem(key) {
    delete this.store[key];
  }

  get length() {
    return Object.keys(this.store).length;
  }

  key(index) {
    const keys = Object.keys(this.store);
    return keys[index] || null;
  }
}

global.localStorage = new LocalStorageMock();

// Mock Audio API
global.Audio = class {
  constructor(src) {
    this.src = src;
    this.currentTime = 0;
    this.duration = 10;
    this.paused = true;
    this.play = jest.fn(() => {
      this.paused = false;
      return Promise.resolve();
    });
    this.pause = jest.fn(() => {
      this.paused = true;
    });
  }

  addEventListener(event, handler) {
    // Store handlers for testing if needed
    if (!this._handlers) this._handlers = {};
    if (!this._handlers[event]) this._handlers[event] = [];
    this._handlers[event].push(handler);
  }

  removeEventListener(event, handler) {
    if (!this._handlers || !this._handlers[event]) return;
    const index = this._handlers[event].indexOf(handler);
    if (index > -1) this._handlers[event].splice(index, 1);
  }

  // Trigger event for testing
  _triggerEvent(eventName, data = {}) {
    if (!this._handlers || !this._handlers[eventName]) return;
    this._handlers[eventName].forEach(handler => handler(data));
  }
};

// Mock SpeechSynthesisUtterance
global.SpeechSynthesisUtterance = class {
  constructor(text) {
    this.text = text;
    this.lang = 'en-US';
    this.rate = 1;
  }

  addEventListener(event, handler) {
    if (!this._handlers) this._handlers = {};
    if (!this._handlers[event]) this._handlers[event] = [];
    this._handlers[event].push(handler);
  }

  _triggerEvent(eventName, data = {}) {
    if (!this._handlers || !this._handlers[eventName]) return;
    this._handlers[eventName].forEach(handler => handler(data));
  }
};

// Mock speechSynthesis
global.speechSynthesis = {
  speaking: false,
  speak(utterance) {
    this.speaking = true;
    setTimeout(() => {
      utterance._triggerEvent('end');
      this.speaking = false;
    }, 10);
  },
  cancel() {
    this.speaking = false;
  }
};

// Mock CONFIG object
global.CONFIG = {
  ui: {
    audioTimeout: 2000
  },
  feedback: {
    noAnswer: {
      openEnded: 'Vul eerst een antwoord in!'
    }
  },
  subjectFilePaths: {
    werkwoordspelling: {
      groep4: {
        m4: 'data/exercises/sp/werkwoordspelling-g4-m4.json'
      }
    }
  }
};

// Mock storage manager global instance
global.storage = {
  cache: new Map(),
  writeQueue: new Map(),
  flushTimer: null,

  get(key, defaultValue = null) {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    const value = localStorage.getItem(key);
    if (value !== null) {
      const parsed = JSON.parse(value);
      this.cache.set(key, parsed);
      return parsed;
    }
    return defaultValue;
  },

  set(key, value) {
    this.cache.set(key, value);
    this.writeQueue.set(key, value);
    clearTimeout(this.flushTimer);
    this.flushTimer = setTimeout(() => this.flush(), 300);
  },

  flush() {
    this.writeQueue.forEach((value, key) => {
      const serialized = typeof value === 'string' ? value : JSON.stringify(value);
      localStorage.setItem(key, serialized);
    });
    this.writeQueue.clear();
  },

  remove(key) {
    this.cache.delete(key);
    this.writeQueue.delete(key);
    localStorage.removeItem(key);
  },

  clear(clearStorage = false) {
    this.cache.clear();
    this.writeQueue.clear();
    clearTimeout(this.flushTimer);
    if (clearStorage) {
      localStorage.clear();
    }
  }
};

// Suppress console.log/warn/error in tests unless needed
global.console = {
  ...console,
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
};
