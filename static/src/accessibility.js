/**
 * Accessibility Features for OefenPlatform
 * WCAG 2.1 AAA compliant accessibility options
 * Supports dyslexia, ADHD, autism, low-vision, and younger learners
 */

// Initialize accessibility features on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeAccessibility();
});

function initializeAccessibility() {
    const toggle = document.getElementById('accessibilityToggle');
    const panel = document.getElementById('accessibilityPanel');
    const dyslexiaCheckbox = document.getElementById('dyslexiaMode');
    const focusModeCheckbox = document.getElementById('focusMode');
    const highContrastCheckbox = document.getElementById('highContrastMode');
    const fontSizeButtons = document.querySelectorAll('.font-size-btn');

    // Load saved settings from localStorage
    loadAccessibilitySettings();

    // Toggle panel open/close
    if (toggle) {
        toggle.addEventListener('click', function() {
            panel.classList.toggle('open');
        });
    }

    // Close panel when clicking outside
    document.addEventListener('click', function(event) {
        if (!panel.contains(event.target) && !toggle.contains(event.target)) {
            panel.classList.remove('open');
        }
    });

    // Font size controls
    fontSizeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const size = this.getAttribute('data-size');
            setFontSize(size);

            // Update active state
            fontSizeButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Save to localStorage
            localStorage.setItem('accessibilityFontSize', size);
        });
    });

    // Dyslexia mode toggle
    if (dyslexiaCheckbox) {
        dyslexiaCheckbox.addEventListener('change', function() {
            toggleDyslexiaMode(this.checked);
            localStorage.setItem('accessibilityDyslexia', this.checked);
        });
    }

    // Focus mode toggle
    if (focusModeCheckbox) {
        focusModeCheckbox.addEventListener('change', function() {
            toggleFocusMode(this.checked);
            localStorage.setItem('accessibilityFocusMode', this.checked);
        });
    }

    // High contrast mode toggle
    if (highContrastCheckbox) {
        highContrastCheckbox.addEventListener('change', function() {
            toggleHighContrastMode(this.checked);
            localStorage.setItem('accessibilityHighContrast', this.checked);
        });
    }
}

/**
 * Load saved accessibility settings from localStorage
 */
function loadAccessibilitySettings() {
    // Load font size
    const savedFontSize = localStorage.getItem('accessibilityFontSize');
    if (savedFontSize) {
        setFontSize(savedFontSize);
        // Update button active state
        const buttons = document.querySelectorAll('.font-size-btn');
        buttons.forEach(btn => {
            if (btn.getAttribute('data-size') === savedFontSize) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // Load dyslexia mode
    const savedDyslexia = localStorage.getItem('accessibilityDyslexia') === 'true';
    const dyslexiaCheckbox = document.getElementById('dyslexiaMode');
    if (dyslexiaCheckbox) {
        dyslexiaCheckbox.checked = savedDyslexia;
        toggleDyslexiaMode(savedDyslexia);
    }

    // Load focus mode
    const savedFocusMode = localStorage.getItem('accessibilityFocusMode') === 'true';
    const focusModeCheckbox = document.getElementById('focusMode');
    if (focusModeCheckbox) {
        focusModeCheckbox.checked = savedFocusMode;
        toggleFocusMode(savedFocusMode);
    }

    // Load high contrast mode
    const savedHighContrast = localStorage.getItem('accessibilityHighContrast') === 'true';
    const highContrastCheckbox = document.getElementById('highContrastMode');
    if (highContrastCheckbox) {
        highContrastCheckbox.checked = savedHighContrast;
        toggleHighContrastMode(savedHighContrast);
    }
}

/**
 * Set font size across the application
 * @param {string} size - 'standard', 'groot', or 'extra-groot'
 */
function setFontSize(size) {
    const body = document.body;

    // Remove all font size classes
    body.classList.remove('font-scale-groot', 'font-scale-extra-groot');

    // Add appropriate class
    if (size === 'groot') {
        body.classList.add('font-scale-groot');
    } else if (size === 'extra-groot') {
        body.classList.add('font-scale-extra-groot');
    }
}

/**
 * Toggle dyslexia-friendly mode
 * Uses Lexend font, increased spacing, left alignment
 * @param {boolean} enabled - Whether to enable dyslexia mode
 */
function toggleDyslexiaMode(enabled) {
    const body = document.body;

    if (enabled) {
        body.classList.add('dyslexia-mode');
    } else {
        body.classList.remove('dyslexia-mode');
    }
}

/**
 * Toggle focus mode for minimal distraction
 * Dims/hides header, footer, and non-essential elements
 * @param {boolean} enabled - Whether to enable focus mode
 */
function toggleFocusMode(enabled) {
    const body = document.body;

    if (enabled) {
        body.classList.add('focus-mode');
    } else {
        body.classList.remove('focus-mode');
    }
}

/**
 * Toggle high contrast mode
 * Uses pure black text on white backgrounds
 * @param {boolean} enabled - Whether to enable high contrast mode
 */
function toggleHighContrastMode(enabled) {
    const body = document.body;

    if (enabled) {
        body.classList.add('high-contrast');
    } else {
        body.classList.remove('high-contrast');
    }
}

/**
 * Reset all accessibility settings to defaults
 */
function resetAccessibilitySettings() {
    // Clear localStorage
    localStorage.removeItem('accessibilityFontSize');
    localStorage.removeItem('accessibilityDyslexia');
    localStorage.removeItem('accessibilityFocusMode');
    localStorage.removeItem('accessibilityHighContrast');

    // Reset UI
    setFontSize('standard');
    toggleDyslexiaMode(false);
    toggleFocusMode(false);
    toggleHighContrastMode(false);

    // Reset checkboxes
    const dyslexiaCheckbox = document.getElementById('dyslexiaMode');
    const focusModeCheckbox = document.getElementById('focusMode');
    const highContrastCheckbox = document.getElementById('highContrastMode');

    if (dyslexiaCheckbox) dyslexiaCheckbox.checked = false;
    if (focusModeCheckbox) focusModeCheckbox.checked = false;
    if (highContrastCheckbox) highContrastCheckbox.checked = false;

    // Reset font size buttons
    const fontSizeButtons = document.querySelectorAll('.font-size-btn');
    fontSizeButtons.forEach(btn => {
        if (btn.getAttribute('data-size') === 'standard') {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Export functions for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        setFontSize,
        toggleDyslexiaMode,
        toggleFocusMode,
        toggleHighContrastMode,
        resetAccessibilitySettings
    };
}
