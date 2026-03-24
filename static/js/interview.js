let currentInterview = null;
let currentQuestionIndex = 0;
let evaluations = [];
let selectedDifficulty = 'Easy';

document.querySelectorAll('.difficulty-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        document.querySelectorAll('.difficulty-btn').forEach(b => {
            b.className = 'difficulty-btn px-4 py-3 border-2 border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition';
        });

        this.className = 'difficulty-btn px-4 py-3 border-2 border-green-600 text-green-600 rounded-lg hover:bg-green-50 transition';
        selectedDifficulty = this.dataset.difficulty;
        document.getElementById('difficulty').value = selectedDifficulty;
    });
});

document.getElementById('startInterviewBtn').addEventListener('click', function () {
    const topic = document.getElementById('topic').value.trim();
    const numQuestions = parseInt(document.getElementById('numQuestions').value);

    if (!topic) {
        alert('Please enter a topic');
        return;
    }

    document.getElementById('loading').classList.remove('hidden');
    this.disabled = true;

    fetch('/api/interview/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic,
            difficulty: selectedDifficulty,
            num_questions: numQuestions
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').classList.add('hidden');
            this.disabled = false;

            if (data.success && data.interview) {
                currentInterview = data.interview;
                currentQuestionIndex = 0;
                evaluations = [];
                startInterview();
            }
        })
        .catch(error => {
            document.getElementById('loading').classList.add('hidden');
            this.disabled = false;
            alert('Error starting interview. Please try again.');
        });
});

function startInterview() {
    document.getElementById('setupSection').classList.add('hidden');
    document.getElementById('interviewSection').classList.remove('hidden');
    document.getElementById('totalQuestions').textContent = currentInterview.questions.length;
    document.getElementById('difficultyBadge').textContent = currentInterview.difficulty;

    displayQuestion();
}

function displayQuestion() {
    const question = currentInterview.questions[currentQuestionIndex];

    document.getElementById('currentQuestion').textContent = currentQuestionIndex + 1;
    document.getElementById('questionText').textContent = question.question;
    document.getElementById('responseText').value = '';

    const hintsList = document.getElementById('hintsList');
    hintsList.innerHTML = '';
    if (question.hints && question.hints.length > 0) {
        question.hints.forEach(hint => {
            const li = document.createElement('li');
            li.textContent = hint;
            hintsList.appendChild(li);
        });
    }

    document.getElementById('hintsSection').classList.add('hidden');
    document.getElementById('evaluationSection').classList.add('hidden');
    document.getElementById('showHintsBtn').classList.remove('hidden');
    document.getElementById('submitResponseBtn').classList.remove('hidden');
}

document.getElementById('showHintsBtn').addEventListener('click', function () {
    document.getElementById('hintsSection').classList.remove('hidden');
    this.classList.add('hidden');
});

document.getElementById('submitResponseBtn').addEventListener('click', function () {
    const response = document.getElementById('responseText').value.trim();

    if (!response) {
        alert('Please provide a response');
        return;
    }

    const question = currentInterview.questions[currentQuestionIndex];

    this.disabled = true;
    this.textContent = 'Evaluating...';

    fetch('/api/interview/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: question.question,
            response: response
        })
    })
        .then(response => response.json())
        .then(data => {
            this.disabled = false;
            this.textContent = 'Submit Response';

            if (data.success && data.evaluation) {
                evaluations.push(data.evaluation);
                displayEvaluation(data.evaluation);
            }
        })
        .catch(error => {
            this.disabled = false;
            this.textContent = 'Submit Response';
            alert('Error evaluating response. Please try again.');
        });
});

function displayEvaluation(evaluation) {
    document.getElementById('evaluationSection').classList.remove('hidden');
    document.getElementById('showHintsBtn').classList.add('hidden');
    document.getElementById('submitResponseBtn').classList.add('hidden');

    document.getElementById('techScore').textContent = `${evaluation.technical_score}/10`;
    document.getElementById('commScore').textContent = `${evaluation.communication_score}/10`;
    document.getElementById('psScore').textContent = `${evaluation.problem_solving_score}/10`;
    document.getElementById('overallScore').textContent = `${evaluation.overall_score}/10`;
    document.getElementById('feedbackText').textContent = evaluation.feedback;
}

document.getElementById('nextQuestionBtn').addEventListener('click', function () {
    if (currentQuestionIndex < currentInterview.questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        showSummary();
    }
});

function showSummary() {
    fetch('/api/interview/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic: currentInterview.topic,
            difficulty: currentInterview.difficulty,
            evaluations: evaluations
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.summary) {
                displaySummary(data.summary);
            }
        });
}

function displaySummary(summary) {
    document.getElementById('interviewSection').classList.add('hidden');
    document.getElementById('summarySection').classList.remove('hidden');

    document.getElementById('avgScore').textContent = `${summary.average_score}/10`;
    document.getElementById('perfLevel').textContent = summary.performance_level;

    const strengthsList = document.getElementById('strengthsList');
    strengthsList.innerHTML = '';
    summary.strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });

    const improvementsList = document.getElementById('improvementsList');
    improvementsList.innerHTML = '';
    summary.improvements.forEach(improvement => {
        const li = document.createElement('li');
        li.textContent = improvement;
        improvementsList.appendChild(li);
    });

    const ctx = document.getElementById('scoreChart').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Technical', 'Communication', 'Problem Solving', 'Cultural Fit'],
            datasets: [{
                label: 'Your Scores',
                data: [
                    summary.score_breakdown.technical,
                    summary.score_breakdown.communication,
                    summary.score_breakdown.problem_solving,
                    summary.score_breakdown.cultural_fit
                ],
                backgroundColor: 'rgba(34, 197, 94, 0.2)',
                borderColor: 'rgba(34, 197, 94, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
}

document.getElementById('newInterviewBtn').addEventListener('click', function () {
    document.getElementById('summarySection').classList.add('hidden');
    document.getElementById('setupSection').classList.remove('hidden');
    document.getElementById('topic').value = '';
    currentInterview = null;
    currentQuestionIndex = 0;
    evaluations = [];
});
