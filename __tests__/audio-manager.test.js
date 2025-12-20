/**
 * Unit tests for AudioManager
 */

const { AudioManager } = require('../static/src/utils.js');

describe('AudioManager', () => {
  let audioManager;

  beforeEach(() => {
    audioManager = new AudioManager();
    jest.clearAllMocks();
  });

  afterEach(() => {
    audioManager.stop();
  });

  describe('constructor', () => {
    test('should initialize with null currentAudio', () => {
      expect(audioManager.currentAudio).toBeNull();
    });

    test('should initialize with isPlaying=false', () => {
      expect(audioManager.isPlaying).toBe(false);
    });
  });

  describe('playAudio()', () => {
    test('should play audio file successfully', async () => {
      const mockAudio = new Audio();
      global.Audio = jest.fn(() => mockAudio);

      const promise = audioManager.playAudio('test.mp3', 'fallback text', { timeout: 100 });

      // Simulate successful audio playback
      setTimeout(() => {
        mockAudio._triggerEvent('ended');
      }, 10);

      await promise;

      expect(audioManager.isPlaying).toBe(false);
      expect(mockAudio.play).toHaveBeenCalled();
    });

    test('should fallback to TTS when audio file fails', async () => {
      const mockAudio = new Audio();
      mockAudio.play = jest.fn(() => Promise.reject(new Error('Audio failed')));
      global.Audio = jest.fn(() => mockAudio);

      const promise = audioManager.playAudio('nonexistent.mp3', 'fallback text', { timeout: 100 });

      await promise;

      // Should have attempted to use speechSynthesis
      expect(console.log).toHaveBeenCalledWith(
        expect.stringContaining('Audio playback failed'),
        expect.any(String)
      );
    });

    test('should stop current audio before playing new audio', async () => {
      const mockAudio1 = new Audio();
      const mockAudio2 = new Audio();

      let callCount = 0;
      global.Audio = jest.fn(() => {
        callCount++;
        return callCount === 1 ? mockAudio1 : mockAudio2;
      });

      // Start first audio
      const promise1 = audioManager.playAudio('test1.mp3', 'text1', { timeout: 100 });

      expect(audioManager.currentAudio).toBe(mockAudio1);
      expect(audioManager.isPlaying).toBe(true);

      // Start second audio before first finishes
      const promise2 = audioManager.playAudio('test2.mp3', 'text2', { timeout: 100 });

      expect(mockAudio1.pause).toHaveBeenCalled();
      expect(mockAudio1.currentTime).toBe(0);
      expect(audioManager.currentAudio).toBe(mockAudio2);

      // Complete second audio
      setTimeout(() => mockAudio2._triggerEvent('ended'), 10);
      await promise2;
    });

    test('should handle timeout', async () => {
      const mockAudio = new Audio();
      // Don't trigger 'ended' event to simulate timeout
      global.Audio = jest.fn(() => mockAudio);

      await expect(
        audioManager.playAudio('test.mp3', 'fallback', { timeout: 50 })
      ).rejects.toThrow();
    });

    test('should call onProgress callback if provided', async () => {
      const mockAudio = new Audio();
      global.Audio = jest.fn(() => mockAudio);
      const onProgress = jest.fn();

      const promise = audioManager.playAudio('test.mp3', 'fallback', {
        timeout: 100,
        onProgress
      });

      // Simulate timeupdate event
      mockAudio._triggerEvent('timeupdate');

      expect(onProgress).toHaveBeenCalledWith(
        mockAudio.currentTime,
        mockAudio.duration
      );

      // Complete playback
      setTimeout(() => mockAudio._triggerEvent('ended'), 10);
      await promise;
    });

    test('should throw error if no fallback text provided', async () => {
      const mockAudio = new Audio();
      mockAudio.play = jest.fn(() => Promise.reject(new Error('Audio failed')));
      global.Audio = jest.fn(() => mockAudio);

      await expect(
        audioManager.playAudio('test.mp3', null, { timeout: 100 })
      ).rejects.toThrow('No fallback text provided for TTS');
    });
  });

  describe('playTextToSpeech()', () => {
    test('should play text using speech synthesis', async () => {
      const mockUtterance = new SpeechSynthesisUtterance('test text');
      global.SpeechSynthesisUtterance = jest.fn(() => mockUtterance);

      const promise = audioManager.playTextToSpeech('test text');

      expect(audioManager.isPlaying).toBe(true);
      expect(mockUtterance.lang).toBe('nl-NL');
      expect(mockUtterance.rate).toBe(0.9);

      // Simulate TTS completion
      setTimeout(() => mockUtterance._triggerEvent('end'), 10);
      await promise;

      expect(audioManager.isPlaying).toBe(false);
    });

    test('should reject if speechSynthesis is not supported', async () => {
      const originalSpeechSynthesis = window.speechSynthesis;
      delete window.speechSynthesis;

      await expect(
        audioManager.playTextToSpeech('test text')
      ).rejects.toThrow('Text-to-Speech not supported');

      window.speechSynthesis = originalSpeechSynthesis;
    });

    test('should handle TTS errors', async () => {
      const mockUtterance = new SpeechSynthesisUtterance('test text');
      global.SpeechSynthesisUtterance = jest.fn(() => mockUtterance);

      const promise = audioManager.playTextToSpeech('test text');

      // Simulate TTS error
      setTimeout(() => {
        mockUtterance._triggerEvent('error', { error: 'synthesis-failed' });
      }, 10);

      await expect(promise).rejects.toThrow('TTS error');
      expect(audioManager.isPlaying).toBe(false);
    });
  });

  describe('stop()', () => {
    test('should stop audio playback', () => {
      const mockAudio = new Audio();
      audioManager.currentAudio = mockAudio;
      audioManager.isPlaying = true;

      audioManager.stop();

      expect(mockAudio.pause).toHaveBeenCalled();
      expect(mockAudio.currentTime).toBe(0);
      expect(audioManager.currentAudio).toBeNull();
      expect(audioManager.isPlaying).toBe(false);
    });

    test('should stop speech synthesis', () => {
      speechSynthesis.speaking = true;
      const cancelSpy = jest.spyOn(speechSynthesis, 'cancel');

      audioManager.stop();

      expect(cancelSpy).toHaveBeenCalled();
      expect(audioManager.isPlaying).toBe(false);
    });

    test('should handle being called when nothing is playing', () => {
      audioManager.currentAudio = null;
      audioManager.isPlaying = false;

      expect(() => audioManager.stop()).not.toThrow();
      expect(audioManager.isPlaying).toBe(false);
    });
  });

  describe('getIsPlaying()', () => {
    test('should return true when audio is playing', () => {
      audioManager.isPlaying = true;
      expect(audioManager.getIsPlaying()).toBe(true);
    });

    test('should return false when audio is not playing', () => {
      audioManager.isPlaying = false;
      expect(audioManager.getIsPlaying()).toBe(false);
    });
  });

  describe('integration tests', () => {
    test('should handle rapid play/stop cycles', async () => {
      const mockAudio = new Audio();
      global.Audio = jest.fn(() => mockAudio);

      // Start playing
      const promise = audioManager.playAudio('test.mp3', 'fallback', { timeout: 100 });
      expect(audioManager.isPlaying).toBe(true);

      // Stop immediately
      audioManager.stop();
      expect(audioManager.isPlaying).toBe(false);

      // Complete the audio (should be handled gracefully)
      mockAudio._triggerEvent('ended');

      await expect(promise).rejects.toThrow();
    });

    test('should handle multiple audio files in sequence', async () => {
      const mockAudio1 = new Audio();
      const mockAudio2 = new Audio();
      const mockAudio3 = new Audio();

      let callCount = 0;
      global.Audio = jest.fn(() => {
        callCount++;
        if (callCount === 1) return mockAudio1;
        if (callCount === 2) return mockAudio2;
        return mockAudio3;
      });

      // Play first audio
      const promise1 = audioManager.playAudio('test1.mp3', 'text1', { timeout: 100 });
      setTimeout(() => mockAudio1._triggerEvent('ended'), 10);
      await promise1;
      expect(audioManager.isPlaying).toBe(false);

      // Play second audio
      const promise2 = audioManager.playAudio('test2.mp3', 'text2', { timeout: 100 });
      setTimeout(() => mockAudio2._triggerEvent('ended'), 10);
      await promise2;
      expect(audioManager.isPlaying).toBe(false);

      // Play third audio
      const promise3 = audioManager.playAudio('test3.mp3', 'text3', { timeout: 100 });
      setTimeout(() => mockAudio3._triggerEvent('ended'), 10);
      await promise3;
      expect(audioManager.isPlaying).toBe(false);
    });
  });
});
