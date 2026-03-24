let currentTest = null;
let currentQuestionIndex = 0;
let userAnswers = [];

document.getElementById('startTestBtn').addEventListener('click', function () {
    const topic = document.getElementById('topic').value.trim();
    const numQuestions = parseInt(document.getElementById('numQuestions').value);

    if (!topic) {
        alert('Please enter a topic');
        return;
    }

    document.getElementById('loading').classList.remove('hidden');
    this.disabled = true;

    fetch('/api/test/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic, num_questions: numQuestions })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').classList.add('hidden');
            this.disabled = false;

            if (data.success && data.test) {
                currentTest = data.test;
                currentQuestionIndex = 0;
                userAnswers = new Array(data.test.questions.length).fill(null);
                startTest();
            }
        })
        .catch(error => {
            document.getElementById('loading').classList.add('hidden');
            this.disabled = false;
            alert('Error generating test. Please try again.');
        });
});

function startTest() {
    document.getElementById('setupSection').classList.add('hidden');
    document.getElementById('testSection').classList.remove('hidden');
    document.getElementById('testTopic').textContent = `Topic: ${currentTest.topic}`;
    document.getElementById('totalQuestions').textContent = currentTest.questions.length;

    displayQuestion();
}

function displayQuestion() {
    const question = currentTest.questions[currentQuestionIndex];

    document.getElementById('currentQuestion').textContent = currentQuestionIndex + 1;
    document.getElementById('questionText').textContent = question.question;

    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';

    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'flex items-center p-4 border rounded-lg cursor-pointer hover:bg-blue-50 transition';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'answer';
        radio.value = index;
        radio.id = `option${index}`;
        radio.className = 'mr-3';

        if (userAnswers[currentQuestionIndex] === index) {
            radio.checked = true;
        }

        radio.addEventListener('change', function () {
            userAnswers[currentQuestionIndex] = parseInt(this.value);
        });

        const label = document.createElement('label');
        label.htmlFor = `option${index}`;
        label.textContent = option;
        label.className = 'cursor-pointer flex-1';

        optionDiv.appendChild(radio);
        optionDiv.appendChild(label);
        optionsContainer.appendChild(optionDiv);
    });

    document.getElementById('prevBtn').disabled = currentQuestionIndex === 0;

    if (currentQuestionIndex === currentTest.questions.length - 1) {
        document.getElementById('nextBtn').classList.add('hidden');
        document.getElementById('submitTestBtn').classList.remove('hidden');
    } else {
        document.getElementById('nextBtn').classList.remove('hidden');
        document.getElementById('submitTestBtn').classList.add('hidden');
    }
}

document.getElementById('prevBtn').addEventListener('click', function () {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
});

document.getElementById('nextBtn').addEventListener('click', function () {
    if (currentQuestionIndex < currentTest.questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
});

document.getElementById('submitTestBtn').addEventListener('click', function () {
    const unanswered = userAnswers.filter(a => a === null).length;

    if (unanswered > 0) {
        if (!confirm(`You have ${unanswered} unanswered questions. Submit anyway?`)) {
            return;
        }
    }

    fetch('/api/test/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic: currentTest.topic,
            questions: currentTest.questions,
            answers: userAnswers
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResults(data.result);
            }
        });
});

function displayResults(result) {
    document.getElementById('testSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');

    document.getElementById('scoreValue').textContent = `${result.score}%`;
    document.getElementById('correctValue').textContent = `${result.correct_answers}/${result.total_questions}`;
    document.getElementById('performanceLevel').textContent = result.performance_level;

    const detailedResults = document.getElementById('detailedResults');
    detailedResults.innerHTML = '';

    result.results.forEach((item, index) => {
        const resultDiv = document.createElement('div');
        resultDiv.className = `p-4 rounded-lg ${item.is_correct ? 'bg-green-50' : 'bg-red-50'}`;

        resultDiv.innerHTML = `
            <div class="flex items-start justify-between mb-2">
                <h4 class="font-semibold ${item.is_correct ? 'text-green-700' : 'text-red-700'}">
                    Question ${index + 1}
                </h4>
                <span class="${item.is_correct ? 'text-green-600' : 'text-red-600'}">
                    ${item.is_correct ? '✓ Correct' : '✗ Incorrect'}
                </span>
            </div>
            <p class="text-gray-700 mb-2">${item.question}</p>
            <p class="text-sm text-gray-600">${item.explanation}</p>
        `;

        detailedResults.appendChild(resultDiv);
    });
}

document.getElementById('newTestBtn').addEventListener('click', function () {
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('setupSection').classList.remove('hidden');
    document.getElementById('topic').value = '';
    currentTest = null;
    currentQuestionIndex = 0;
    userAnswers = [];
});
