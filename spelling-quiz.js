// Spelling Quiz Logic
let spellingData = [];
let currentWordIndex = 0;
let score = 0;
let currentWord = null;
let hasAnswered = false;
let attemptCount = 0;

// Initialize quiz on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSpellingData();
});

// Load spelling data from localStorage and JSON file
async function loadSpellingData() {
    try {
        // Get subject info from localStorage (set by theme-selector)
        const subject = localStorage.getItem('autoStartSubject');
        const theme = localStorage.getItem('autoStartTheme');
        const level = localStorage.getItem('autoStartLevel') || 'groep4';

        // Update breadcrumb
        document.getElementById('breadcrumbLevel').textContent = formatLevel(level);

        // Load JSON data
        const filename = `spelling-${level}.json`;
        const response = await fetch(filename);

        if (!response.ok) {
            throw new Error(`Could not load ${filename}`);
        }

        spellingData = await response.json();

        // Filter by theme if specified
        if (theme) {
            spellingData = spellingData.filter(word => word.theme === theme);
        }

        // Shuffle words for variety
        shuffleArray(spellingData);

        // Start the quiz
        if (spellingData.length > 0) {
            showWord(0);
        } else {
            alert('Geen spellingwoorden gevonden voor dit niveau.');
            window.location.href = 'index.html';
        }
    } catch (error) {
        console.error('Error loading spelling data:', error);
        alert('Kon de spellingdata niet laden. Probeer het opnieuw.');
        window.location.href = 'index.html';
    }
}

// Show a word
function showWord(index) {
    if (index >= spellingData.length) {
        showResults();
        return;
    }

    currentWordIndex = index;
    currentWord = spellingData[index];
    hasAnswered = false;
    attemptCount = 0;

    // Update progress
    updateProgress();

    // Reset UI
    resetUI();

    // Load audio
    loadAudio();

    // Focus input
    document.getElementById('spellingInput').focus();
}

// Load audio for current word
function loadAudio() {
    const audioElement = document.getElementById('wordAudio');

    // Set audio source - supports both direct URLs and local files
    if (currentWord.audio_url) {
        audioElement.src = currentWord.audio_url;
    } else if (currentWord.audio_file) {
        audioElement.src = `audio/spelling/${currentWord.audio_file}`;
    } else {
        // Fallback: use Web Speech API for text-to-speech
        console.log('No audio file provided, will use text-to-speech');
    }
}

// Play word audio
function playWordAudio() {
    const audioElement = document.getElementById('wordAudio');
    const playButton = document.getElementById('audioPlayButton');
    const playIcon = document.getElementById('playIcon');

    // If audio file exists, play it
    if (audioElement.src && audioElement.src !== window.location.href) {
        playButton.classList.add('playing');
        playIcon.textContent = 'volume_up';

        audioElement.play();

        audioElement.onended = function() {
            playButton.classList.remove('playing');
        };
    } else {
        // Use Web Speech API as fallback
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(currentWord.word);
            utterance.lang = 'nl-NL';
            utterance.rate = 0.8; // Slower for spelling practice

            playButton.classList.add('playing');

            utterance.onend = function() {
                playButton.classList.remove('playing');
            };

            window.speechSynthesis.speak(utterance);
        } else {
            alert('Audio niet beschikbaar. Het woord is: ' + currentWord.word);
        }
    }
}

// Check spelling answer
function checkSpellingAnswer() {
    if (hasAnswered) return;

    const input = document.getElementById('spellingInput');
    const userAnswer = input.value.trim();

    if (!userAnswer) {
        alert('Vul eerst een antwoord in!');
        return;
    }

    attemptCount++;

    // Normalize for comparison (case-insensitive)
    const isCorrect = userAnswer.toLowerCase() === currentWord.word.toLowerCase();

    if (isCorrect) {
        handleCorrectAnswer();
    } else {
        handleIncorrectAnswer(userAnswer);
    }
}

// Handle correct answer
function handleCorrectAnswer() {
    hasAnswered = true;

    // Only count as correct on first attempt
    if (attemptCount === 1) {
        score++;
        updateScore();
    }

    // Update input styling
    const input = document.getElementById('spellingInput');
    input.classList.add('correct');
    input.disabled = true;

    // Disable check button
    document.getElementById('checkButton').disabled = true;

    // Show feedback
    showFeedback(true);
}

// Handle incorrect answer
function handleIncorrectAnswer(userAnswer) {
    const input = document.getElementById('spellingInput');

    if (attemptCount >= 3) {
        // After 3 attempts, show the answer
        hasAnswered = true;
        input.classList.add('incorrect');
        input.disabled = true;
        document.getElementById('checkButton').disabled = true;
        showFeedback(false);
    } else {
        // Allow retry
        input.classList.add('incorrect');

        // Visual feedback animation
        input.style.animation = 'shake 0.4s';
        setTimeout(() => {
            input.style.animation = '';
            input.classList.remove('incorrect');
        }, 400);

        // Show attempt count
        if (attemptCount === 1) {
            alert('Probeer het nog een keer! Luister goed naar het woord.');
        } else if (attemptCount === 2) {
            alert('Nog één kans! Let goed op alle letters.');
        }

        // Select text for easy retry
        input.select();
    }
}

// Show feedback
function showFeedback(isCorrect) {
    const feedbackSection = document.getElementById('feedbackSection');
    const feedbackIcon = document.getElementById('feedbackIcon');
    const feedbackTitle = document.getElementById('feedbackTitle');
    const correctSpellingDisplay = document.getElementById('correctSpellingDisplay');
    const explanationContent = document.getElementById('explanationContent');
    const visualExplanation = document.getElementById('visualExplanation');

    // Set feedback based on correctness
    if (isCorrect) {
        feedbackSection.className = 'feedback-section show correct';
        feedbackIcon.textContent = '🎉';

        if (attemptCount === 1) {
            feedbackTitle.textContent = 'Perfect! Helemaal goed!';
        } else {
            feedbackTitle.textContent = 'Goed gedaan!';
        }
    } else {
        feedbackSection.className = 'feedback-section show incorrect';
        feedbackIcon.textContent = '💡';
        feedbackTitle.textContent = 'Bijna! Hier is de juiste spelling:';
    }

    // Show correct spelling
    correctSpellingDisplay.textContent = currentWord.word;

    // Show visual explanation if available
    if (currentWord.visual_explanation) {
        visualExplanation.style.display = 'block';
        explanationContent.innerHTML = formatExplanation(currentWord.visual_explanation);
    } else {
        visualExplanation.style.display = 'none';
    }
}

// Format explanation with special formatting
function formatExplanation(explanation) {
    // Handle different explanation formats
    if (typeof explanation === 'string') {
        return `<p>${explanation}</p>`;
    } else if (Array.isArray(explanation)) {
        return '<ul>' + explanation.map(item => `<li>${item}</li>`).join('') + '</ul>';
    } else if (typeof explanation === 'object') {
        let html = '';
        if (explanation.rule) {
            html += `<p><strong>Regel:</strong> ${explanation.rule}</p>`;
        }
        if (explanation.examples) {
            html += '<p><strong>Voorbeelden:</strong></p>';
            html += '<ul>' + explanation.examples.map(ex => `<li>${ex}</li>`).join('') + '</ul>';
        }
        if (explanation.tip) {
            html += `<p><strong>💡 Tip:</strong> ${explanation.tip}</p>`;
        }
        return html;
    }
    return '';
}

// Move to next word
function nextWord() {
    showWord(currentWordIndex + 1);
}

// Reset UI for new word
function resetUI() {
    const input = document.getElementById('spellingInput');
    input.value = '';
    input.className = 'spelling-input';
    input.disabled = false;

    const checkButton = document.getElementById('checkButton');
    checkButton.disabled = false;

    const feedbackSection = document.getElementById('feedbackSection');
    feedbackSection.classList.remove('show');

    const playButton = document.getElementById('audioPlayButton');
    playButton.classList.remove('playing');
}

// Update progress bar and label
function updateProgress() {
    const progressLabel = document.getElementById('progressLabel');
    const progressBarFill = document.getElementById('progressBarFill');

    const total = spellingData.length;
    const current = currentWordIndex + 1;
    const percentage = (current / total) * 100;

    progressLabel.textContent = `Woord ${current} van ${total}`;
    progressBarFill.style.width = `${percentage}%`;
}

// Update score
function updateScore() {
    document.getElementById('totalCorrect').textContent = score;
}

// Show results at the end
function showResults() {
    const percentage = Math.round((score / spellingData.length) * 100);

    // Store results in localStorage
    localStorage.setItem('spellingQuizScore', score);
    localStorage.setItem('spellingQuizTotal', spellingData.length);
    localStorage.setItem('spellingQuizPercentage', percentage);

    // Redirect to results page (or show modal)
    alert(`Quiz voltooid!\n\nScore: ${score} / ${spellingData.length} (${percentage}%)`);
    window.location.href = 'index.html';
}

// Pause quiz
function pauseSpellingQuiz() {
    if (confirm('Wil je de quiz pauzeren? Je kunt later verdergaan.')) {
        // Save state to localStorage
        localStorage.setItem('spellingQuizState', JSON.stringify({
            data: spellingData,
            currentIndex: currentWordIndex,
            score: score
        }));
        window.location.href = 'index.html';
    }
}

// Stop quiz
function stopSpellingQuiz() {
    if (confirm('Weet je zeker dat je wilt stoppen? Je voortgang gaat verloren.')) {
        localStorage.removeItem('spellingQuizState');
        window.location.href = 'index.html';
    }
}

// Format level for display
function formatLevel(level) {
    return level.replace('groep', 'Groep ').replace('-', ' ');
}

// Shuffle array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Allow Enter key to submit answer
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('spellingInput');
    if (input) {
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !hasAnswered) {
                checkSpellingAnswer();
            }
        });
    }
});

// Add shake animation
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
`;
document.head.appendChild(style);
