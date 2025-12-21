/**
 * Unit tests for StorageManager
 */

const { StorageManager } = require('../static/src/utils.js');

describe('StorageManager', () => {
  let storage;

  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    storage = new StorageManager();
  });

  afterEach(() => {
    storage.clear(true);
  });

  describe('get()', () => {
    test('should return default value when key does not exist', () => {
      expect(storage.get('nonexistent', 'default')).toBe('default');
    });

    test('should return null when key does not exist and no default provided', () => {
      expect(storage.get('nonexistent')).toBeNull();
    });

    test('should retrieve string values', () => {
      localStorage.setItem('testKey', 'testValue');
      expect(storage.get('testKey')).toBe('testValue');
    });

    test('should parse JSON objects', () => {
      localStorage.setItem('jsonKey', JSON.stringify({ foo: 'bar' }));
      expect(storage.get('jsonKey')).toEqual({ foo: 'bar' });
    });

    test('should parse JSON arrays', () => {
      localStorage.setItem('arrayKey', JSON.stringify([1, 2, 3]));
      expect(storage.get('arrayKey')).toEqual([1, 2, 3]);
    });

    test('should parse boolean true', () => {
      localStorage.setItem('boolKey', 'true');
      expect(storage.get('boolKey')).toBe(true);
    });

    test('should parse boolean false', () => {
      localStorage.setItem('boolKey', 'false');
      expect(storage.get('boolKey')).toBe(false);
    });

    test('should parse numbers', () => {
      localStorage.setItem('numKey', '42');
      expect(storage.get('numKey')).toBe(42);
    });

    test('should cache retrieved values', () => {
      localStorage.setItem('cacheKey', 'cacheValue');
      storage.get('cacheKey');

      // Remove from localStorage but should still be in cache
      localStorage.removeItem('cacheKey');
      expect(storage.get('cacheKey')).toBe('cacheValue');
    });
  });

  describe('set()', () => {
    test('should store string values', () => {
      storage.set('stringKey', 'value');
      storage.flush();
      expect(localStorage.getItem('stringKey')).toBe('value');
    });

    test('should store object values as JSON', () => {
      const obj = { name: 'test', value: 123 };
      storage.set('objKey', obj);
      storage.flush();
      expect(JSON.parse(localStorage.getItem('objKey'))).toEqual(obj);
    });

    test('should store array values as JSON', () => {
      const arr = [1, 2, 3];
      storage.set('arrKey', arr);
      storage.flush();
      expect(JSON.parse(localStorage.getItem('arrKey'))).toEqual(arr);
    });

    test('should update cache immediately', () => {
      storage.set('cacheKey', 'newValue');
      expect(storage.get('cacheKey')).toBe('newValue');
    });

    test('should batch writes', (done) => {
      storage.set('key1', 'value1');
      storage.set('key2', 'value2');

      // Should not be in localStorage immediately
      expect(localStorage.getItem('key1')).toBeNull();
      expect(localStorage.getItem('key2')).toBeNull();

      // Should be in cache
      expect(storage.get('key1')).toBe('value1');
      expect(storage.get('key2')).toBe('value2');

      // After flush timeout (300ms), should be in localStorage
      setTimeout(() => {
        expect(localStorage.getItem('key1')).toBe('value1');
        expect(localStorage.getItem('key2')).toBe('value2');
        done();
      }, 350);
    });

    test('should reset flush timer on subsequent writes', (done) => {
      storage.set('key1', 'value1');

      setTimeout(() => {
        storage.set('key2', 'value2');
      }, 200);

      // After 250ms (200ms + 50ms), key1 should not be flushed yet
      setTimeout(() => {
        expect(localStorage.getItem('key1')).toBeNull();
      }, 250);

      // After 550ms (200ms + 350ms), both should be flushed
      setTimeout(() => {
        expect(localStorage.getItem('key1')).toBe('value1');
        expect(localStorage.getItem('key2')).toBe('value2');
        done();
      }, 550);
    });
  });

  describe('flush()', () => {
    test('should write all pending items to localStorage', () => {
      storage.set('key1', 'value1');
      storage.set('key2', 'value2');
      storage.set('key3', { nested: 'object' });

      storage.flush();

      expect(localStorage.getItem('key1')).toBe('value1');
      expect(localStorage.getItem('key2')).toBe('value2');
      expect(JSON.parse(localStorage.getItem('key3'))).toEqual({ nested: 'object' });
    });

    test('should clear write queue after flushing', () => {
      storage.set('key1', 'value1');
      expect(storage.writeQueue.size).toBe(1);

      storage.flush();
      expect(storage.writeQueue.size).toBe(0);
    });
  });

  describe('remove()', () => {
    test('should remove item from cache', () => {
      storage.set('testKey', 'testValue');
      expect(storage.cache.has('testKey')).toBe(true);

      storage.remove('testKey');
      expect(storage.cache.has('testKey')).toBe(false);
    });

    test('should remove item from write queue', () => {
      storage.set('testKey', 'testValue');
      expect(storage.writeQueue.has('testKey')).toBe(true);

      storage.remove('testKey');
      expect(storage.writeQueue.has('testKey')).toBe(false);
    });

    test('should remove item from localStorage', () => {
      localStorage.setItem('testKey', 'testValue');
      storage.remove('testKey');
      expect(localStorage.getItem('testKey')).toBeNull();
    });
  });

  describe('clear()', () => {
    test('should clear cache', () => {
      storage.set('key1', 'value1');
      storage.set('key2', 'value2');

      storage.clear();
      expect(storage.cache.size).toBe(0);
    });

    test('should clear write queue', () => {
      storage.set('key1', 'value1');
      storage.set('key2', 'value2');

      storage.clear();
      expect(storage.writeQueue.size).toBe(0);
    });

    test('should clear localStorage when clearStorage=true', () => {
      localStorage.setItem('key1', 'value1');
      localStorage.setItem('key2', 'value2');

      storage.clear(true);
      expect(localStorage.length).toBe(0);
    });

    test('should not clear localStorage when clearStorage=false', () => {
      localStorage.setItem('key1', 'value1');
      localStorage.setItem('key2', 'value2');

      storage.clear(false);
      expect(localStorage.length).toBe(2);
    });
  });

  describe('parseValue()', () => {
    test('should parse JSON objects', () => {
      const result = storage.parseValue('{"foo":"bar"}');
      expect(result).toEqual({ foo: 'bar' });
    });

    test('should parse JSON arrays', () => {
      const result = storage.parseValue('[1,2,3]');
      expect(result).toEqual([1, 2, 3]);
    });

    test('should parse "true" as boolean', () => {
      expect(storage.parseValue('true')).toBe(true);
    });

    test('should parse "false" as boolean', () => {
      expect(storage.parseValue('false')).toBe(false);
    });

    test('should parse numeric strings as numbers', () => {
      expect(storage.parseValue('42')).toBe(42);
      expect(storage.parseValue('3.14')).toBe(3.14);
    });

    test('should return string for non-parseable values', () => {
      expect(storage.parseValue('hello')).toBe('hello');
    });

    test('should return string for invalid JSON', () => {
      expect(storage.parseValue('{invalid json}')).toBe('{invalid json}');
    });
  });

  describe('error handling', () => {
    test('should handle localStorage errors gracefully on get', () => {
      // Mock localStorage.getItem to throw error
      const originalGetItem = localStorage.getItem;
      localStorage.getItem = jest.fn(() => {
        throw new Error('Storage error');
      });

      const result = storage.get('errorKey', 'default');
      expect(result).toBe('default');
      expect(console.warn).toHaveBeenCalled();

      localStorage.getItem = originalGetItem;
    });

    test('should handle localStorage errors gracefully on flush', () => {
      const originalSetItem = localStorage.setItem;
      localStorage.setItem = jest.fn(() => {
        throw new Error('Storage full');
      });

      storage.set('key', 'value');
      storage.flush();

      expect(console.warn).toHaveBeenCalled();

      localStorage.setItem = originalSetItem;
    });
  });
});
