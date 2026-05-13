const API_URL = 'https://ai-health-api-xyz.onrender.com'; 
let allSymptoms = [];
let selectedSymptoms = new Set();

const symptomInput = document.getElementById('symptomInput');
const suggestionsList = document.getElementById('suggestions');
const selectedSymptomsDiv = document.getElementById('selectedSymptoms');
const predictBtn = document.getElementById('predictBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsSection = document.getElementById('resultsSection');
const predictionsList = document.getElementById('predictionsList');

// Initialize
fetchSymptoms();

async function fetchSymptoms() {
    try {
        const response = await fetch(`${API_URL}/symptoms`);
        const data = await response.json();
        allSymptoms = data.symptoms;
    } catch (error) {
        console.error('Error fetching symptoms:', error);
    }
}

symptomInput.addEventListener('input', (e) => {
    const value = e.target.value.toLowerCase();
    if (!value) {
        suggestionsList.style.display = 'none';
        return;
    }

    const filtered = allSymptoms.filter(s => 
        s.toLowerCase().includes(value) && !selectedSymptoms.has(s)
    ).slice(0, 5);

    if (filtered.length > 0) {
        suggestionsList.innerHTML = filtered.map(s => `
            <div class="suggestion-item" onclick="addSymptom('${s}')">${s.replace(/_/g, ' ')}</div>
        `).join('');
        suggestionsList.style.display = 'block';
    } else {
        suggestionsList.style.display = 'none';
    }
});

function addSymptom(symptom) {
    selectedSymptoms.add(symptom);
    symptomInput.value = '';
    suggestionsList.style.display = 'none';
    renderTags();
    checkPredictButton();
}

function removeSymptom(symptom) {
    selectedSymptoms.delete(symptom);
    renderTags();
    checkPredictButton();
}

function renderTags() {
    selectedSymptomsDiv.innerHTML = Array.from(selectedSymptoms).map(s => `
        <div class="tag">
            ${s.replace(/_/g, ' ')}
            <span class="close" onclick="removeSymptom('${s}')">&times;</span>
        </div>
    `).join('');
}

function checkPredictButton() {
    predictBtn.disabled = selectedSymptoms.size === 0;
}

clearBtn.addEventListener('click', () => {
    selectedSymptoms.clear();
    renderTags();
    checkPredictButton();
    resultsSection.classList.add('hidden');
});

predictBtn.addEventListener('click', async () => {
    predictBtn.innerHTML = 'Analyzing Symptoms...';
    predictBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: Array.from(selectedSymptoms) })
        });

        const data = await response.json();
        displayResults(data.predictions);
        saveToHistory(Array.from(selectedSymptoms), data.predictions);
    } catch (error) {
        console.error('Error predicting:', error);
        alert('Could not connect to the medical AI server.');
    } finally {
        predictBtn.innerHTML = 'Predict Possible Diseases';
        checkPredictButton();
    }
});

function displayResults(predictions) {
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    if (!predictions || predictions.length === 0) {
        predictionsList.innerHTML = '<p>No specific disease matches these symptoms. However, you should monitor your health and consult a professional.</p>';
        return;
    }

    predictionsList.innerHTML = predictions.map(pred => `
        <div class="prediction-card severity-${pred.severity.toLowerCase()}">
            <div class="pred-header">
                <div>
                    <span class="pred-title">${pred.disease}</span>
                    <span class="status-pill status-${pred.severity.toLowerCase()}">${pred.severity}</span>
                </div>
                <span class="confidence-badge">${pred.confidence}% Match</span>
            </div>
            
            <p class="disease-desc">${pred.description || ''}</p>

            <div class="info-grid">
                <div class="info-col">
                    <h4>⚠️ Precautions</h4>
                    <ul class="tips-list">
                        ${(pred.precautions || []).map(p => `<li>${p}</li>`).join('')}
                    </ul>
                </div>
                <div class="info-col">
                    <h4>💡 Health Advice</h4>
                    <p class="advice-text">${pred.health_advice || 'Maintain a healthy lifestyle.'}</p>
                </div>
            </div>
        </div>
    `).join('');
}

// History Tracking
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');

function loadHistory() {
    const history = JSON.parse(localStorage.getItem('health_history') || '[]');
    if (history.length === 0) {
        historyList.innerHTML = '<p class="empty-msg">No recent history</p>';
        return;
    }

    historyList.innerHTML = history.slice(0, 5).map((item, idx) => `
        <div class="history-item" onclick="loadHistoryItem(${idx})">
            <div class="history-date">${new Date(item.date).toLocaleDateString()}</div>
            <div class="history-syms">${item.symptoms.join(', ')}</div>
            <div class="history-result">${item.results[0]?.disease || 'No match'}</div>
        </div>
    `).join('');
}

function saveToHistory(symptoms, results) {
    const history = JSON.parse(localStorage.getItem('health_history') || '[]');
    history.unshift({
        date: new Date().toISOString(),
        symptoms,
        results
    });
    localStorage.setItem('health_history', JSON.stringify(history));
    loadHistory();
}

function loadHistoryItem(index) {
    const history = JSON.parse(localStorage.getItem('health_history') || '[]');
    const item = history[index];
    if (item) {
        selectedSymptoms = new Set(item.symptoms);
        renderTags();
        displayResults(item.results);
        checkPredictButton();
    }
}

clearHistoryBtn.addEventListener('click', () => {
    localStorage.removeItem('health_history');
    loadHistory();
});

// Initial Load
loadHistory();

// Close suggestions on click away
document.addEventListener('click', (e) => {
    if (e.target !== symptomInput) {
        suggestionsList.style.display = 'none';
    }
});
