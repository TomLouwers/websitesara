/**
 * Accessibility Features for OefenPlatform
 * WCAG 2.1 AAA compliant accessibility options
 * Supports dyslexia, ADHD, autism, low-vision, and younger learners
 *
 * OPTIMIZED VERSION - Uses shared utilities and improved performance
 */

// Accessibility Manager Class - Singleton pattern for state management
class AccessibilityManager {
    constructor() {
        if (AccessibilityManager.instance) {
            return AccessibilityManager.instance;
        }

        this.elements = {};
        this.settings = {
            fontSize: CONFIG.accessibility.defaults.fontSize,
            dyslexiaMode: CONFIG.accessibility.defaults.dyslexiaMode,
            focusMode: false, // Not in CONFIG yet, keeping for backward compat
            highContrast: CONFIG.accessibility.defaults.highContrast
        };

        AccessibilityManager.instance = this;
    }

    /**
     * Initialize accessibility features
     */
    init() {
        this.cacheElements();
        this.loadSettings();
        this.attachEventListeners();
    }

    /**
     * Cache DOM elements for performance
     * @private
     */
    cacheElements() {
        this.elements = {
            toggle: document.getElementById('accessibilityToggle'),
            panel: document.getElementById('accessibilityPanel'),
            fontSizeButtons: document.querySelectorAll('.font-size-btn'),
            dyslexiaCheckbox: document.getElementById('dyslexiaMode'),
            focusModeCheckbox: document.getElementById('focusMode'),
            highContrastCheckbox: document.getElementById('highContrastMode'),
            body: document.body
        };
    }

    /**
     * Attach event listeners with event delegation
     * @private
     */
    attachEventListeners() {
        const { toggle, panel, dyslexiaCheckbox, focusModeCheckbox, highContrastCheckbox } = this.elements;

        // Toggle panel visibility
        if (toggle) {
            toggle.addEventListener('click', () => this.togglePanel());
        }

        // Close panel when clicking outside (using event delegation)
        document.addEventListener('click', (e) => {
            // Only run if both panel and toggle exist
            if (panel && toggle && !panel.contains(e.target) && !toggle.contains(e.target)) {
                panel.classList.remove('open');
            }
        });

        // Font size buttons - use event delegation for better performance
        this.elements.fontSizeButtons.forEach(button => {
            button.addEventListener('click', (e) => this.handleFontSizeChange(e.target));
        });

        // Checkbox event listeners with optimized handlers
        if (dyslexiaCheckbox) {
            dyslexiaCheckbox.addEventListener('change', (e) =>
                this.updateSetting('dyslexiaMode', e.target.checked, this.toggleDyslexiaMode.bind(this))
            );
        }

        if (focusModeCheckbox) {
            focusModeCheckbox.addEventListener('change', (e) =>
                this.updateSetting('focusMode', e.target.checked, this.toggleFocusMode.bind(this))
            );
        }

        if (highContrastCheckbox) {
            highContrastCheckbox.addEventListener('change', (e) =>
                this.updateSetting('highContrast', e.target.checked, this.toggleHighContrastMode.bind(this))
            );
        }
    }

    /**
     * Toggle accessibility panel
     * @private
     */
    togglePanel() {
        this.elements.panel?.classList.toggle('open');
    }

    /**
     * Handle font size button click
     * @private
     * @param {HTMLElement} button - Clicked button
     */
    handleFontSizeChange(button) {
        const size = button.dataset.size;
        if (!size) return;

        this.setFontSize(size);
        DOMUtils.toggleButtonGroup(this.elements.fontSizeButtons, size, 'size');
        this.updateSetting('fontSize', size);
    }

    /**
     * Generic setting update with storage and callback
     * @private
     * @param {string} key - Setting key
     * @param {*} value - Setting value
     * @param {Function} callback - Optional callback function
     */
    updateSetting(key, value, callback) {
        this.settings[key] = value;

        // Get storage key from config or fallback
        const storageKey = CONFIG.accessibility.storageKeys[key] || `accessibility${key.charAt(0).toUpperCase() + key.slice(1)}`;
        storage.set(storageKey, value);

        if (callback) {
            callback(value);
        }
    }

    /**
     * Load all settings from storage
     * @private
     */
    loadSettings() {
        // Load font size
        const savedFontSize = storage.get(
            CONFIG.accessibility.storageKeys.fontSize,
            CONFIG.accessibility.defaults.fontSize
        );
        this.setFontSize(savedFontSize);
        DOMUtils.toggleButtonGroup(this.elements.fontSizeButtons, savedFontSize, 'size');

        // Load and apply dyslexia mode
        const savedDyslexia = storage.get(
            CONFIG.accessibility.storageKeys.dyslexia,
            CONFIG.accessibility.defaults.dyslexiaMode
        );
        if (this.elements.dyslexiaCheckbox) {
            this.elements.dyslexiaCheckbox.checked = savedDyslexia;
        }
        this.toggleDyslexiaMode(savedDyslexia);

        // Load focus mode (backward compatibility)
        const savedFocusMode = storage.get('accessibilityFocusMode', false);
        if (this.elements.focusModeCheckbox) {
            this.elements.focusModeCheckbox.checked = savedFocusMode;
        }
        this.toggleFocusMode(savedFocusMode);

        // Load and apply high contrast mode
        const savedHighContrast = storage.get(
            CONFIG.accessibility.storageKeys.highContrast,
            CONFIG.accessibility.defaults.highContrast
        );
        if (this.elements.highContrastCheckbox) {
            this.elements.highContrastCheckbox.checked = savedHighContrast;
        }
        this.toggleHighContrastMode(savedHighContrast);

        // Update internal state
        this.settings = {
            fontSize: savedFontSize,
            dyslexiaMode: savedDyslexia,
            focusMode: savedFocusMode,
            highContrast: savedHighContrast
        };
    }

    /**
     * Set font size across the application
     * @param {string} size - Font size key (normal, large, xlarge)
     */
    setFontSize(size) {
        const { body } = this.elements;
        if (!body) return;

        // Remove all font size classes
        Object.values(CONFIG.accessibility.fontSizes).forEach(({ className }) => {
            body.classList.remove(className);
        });

        // Also remove legacy classes for backward compatibility
        body.classList.remove('font-scale-groot', 'font-scale-extra-groot');

        // Add new class if not normal
        const fontConfig = CONFIG.accessibility.fontSizes[size];
        if (fontConfig && size !== 'normal') {
            body.classList.add(fontConfig.className);
        }

        // Legacy support - map to old classes
        if (size === 'groot' || size === 'large') {
            body.classList.add('font-scale-groot');
        } else if (size === 'extra-groot' || size === 'xlarge') {
            body.classList.add('font-scale-extra-groot');
        }
    }

    /**
     * Toggle dyslexia-friendly mode
     * Uses Lexend font, increased spacing, left alignment
     * @param {boolean} enabled - Whether to enable dyslexia mode
     */
    toggleDyslexiaMode(enabled) {
        this.elements.body?.classList.toggle('dyslexia-mode', enabled);
        this.settings.dyslexiaMode = enabled;
    }

    /**
     * Toggle focus mode for minimal distraction
     * Dims/hides header, footer, and non-essential elements
     * @param {boolean} enabled - Whether to enable focus mode
     */
    toggleFocusMode(enabled) {
        this.elements.body?.classList.toggle('focus-mode', enabled);
        this.settings.focusMode = enabled;
    }

    /**
     * Toggle high contrast mode
     * Uses pure black text on white backgrounds
     * @param {boolean} enabled - Whether to enable high contrast mode
     */
    toggleHighContrastMode(enabled) {
        this.elements.body?.classList.toggle('high-contrast', enabled);
        this.settings.highContrast = enabled;
    }

    /**
     * Reset all accessibility settings to defaults
     */
    reset() {
        // Clear storage (batch operation)
        Object.values(CONFIG.accessibility.storageKeys).forEach(key => {
            storage.remove(key);
        });
        // Legacy keys for backward compatibility
        storage.remove('accessibilityFocusMode');

        // Flush changes immediately
        storage.flush();

        // Reset to defaults
        const defaults = CONFIG.accessibility.defaults;
        this.setFontSize(defaults.fontSize);
        this.toggleDyslexiaMode(defaults.dyslexiaMode);
        this.toggleFocusMode(false);
        this.toggleHighContrastMode(defaults.highContrast);

        // Reset UI elements
        if (this.elements.dyslexiaCheckbox) this.elements.dyslexiaCheckbox.checked = false;
        if (this.elements.focusModeCheckbox) this.elements.focusModeCheckbox.checked = false;
        if (this.elements.highContrastCheckbox) this.elements.highContrastCheckbox.checked = false;

        // Reset font size buttons
        DOMUtils.toggleButtonGroup(this.elements.fontSizeButtons, defaults.fontSize, 'size');
    }

    /**
     * Get current settings
     * @returns {Object} Current accessibility settings
     */
    getSettings() {
        return { ...this.settings };
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    const accessibilityManager = new AccessibilityManager();
    accessibilityManager.init();

    // Expose globally for potential external use
    window.accessibilityManager = accessibilityManager;
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AccessibilityManager };
}
