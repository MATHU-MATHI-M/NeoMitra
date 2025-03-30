document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Handle conditional form fields (e.g., pregnancy-related fields)
    const pregnancyCheckbox = document.getElementById('is_pregnant');
    if (pregnancyCheckbox) {
        const pregnancyFields = document.getElementById('pregnancy-fields');
        
        function togglePregnancyFields() {
            if (pregnancyCheckbox.checked) {
                pregnancyFields.classList.remove('d-none');
            } else {
                pregnancyFields.classList.add('d-none');
            }
        }
        
        // Initial state
        togglePregnancyFields();
        
        // Listen for changes
        pregnancyCheckbox.addEventListener('change', togglePregnancyFields);
    }
    
    // Handle language selection
    const languageSelector = document.getElementById('language-selector');
    if (languageSelector) {
        languageSelector.addEventListener('change', function() {
            const selectedLanguage = this.value;
            // Set a cookie to remember the language preference
            document.cookie = `language=${selectedLanguage}; path=/; max-age=31536000`;
            // Reload the page to apply the new language
            window.location.reload();
        });
    }
    
    // Initialize charts if they exist on the page
    initializeCharts();
});

// Function to initialize all charts
function initializeCharts() {
    // Risk score chart
    const riskScoreCanvas = document.getElementById('risk-score-chart');
    if (riskScoreCanvas) {
        const riskScoreChart = new Chart(riskScoreCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Pregnancy Risk', 'Anemia Risk', 'Remaining'],
                datasets: [{
                    data: [
                        riskScoreCanvas.getAttribute('data-pregnancy-risk') || 0, 
                        riskScoreCanvas.getAttribute('data-anemia-risk') || 0,
                        100 - (riskScoreCanvas.getAttribute('data-pregnancy-risk') || 0) - (riskScoreCanvas.getAttribute('data-anemia-risk') || 0)
                    ],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(200, 200, 200, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(200, 200, 200, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Health metrics chart
    const healthMetricsCanvas = document.getElementById('health-metrics-chart');
    if (healthMetricsCanvas) {
        const dates = JSON.parse(healthMetricsCanvas.getAttribute('data-dates') || '[]');
        const weights = JSON.parse(healthMetricsCanvas.getAttribute('data-weights') || '[]');
        const hemoValues = JSON.parse(healthMetricsCanvas.getAttribute('data-hemoglobin') || '[]');
        
        const healthMetricsChart = new Chart(healthMetricsCanvas, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Weight (kg)',
                        data: weights,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        tension: 0.1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Hemoglobin (g/dL)',
                        data: hemoValues,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        tension: 0.1,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Weight (kg)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Hemoglobin (g/dL)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
}

// Function to show loading spinner
function showLoading() {
    const loadingSpinner = document.createElement('div');
    loadingSpinner.id = 'loading-spinner';
    loadingSpinner.innerHTML = `
        <div class="spinner-overlay">
            <div class="spinner-container">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loadingSpinner);
}

// Function to hide loading spinner
function hideLoading() {
    const loadingSpinner = document.getElementById('loading-spinner');
    if (loadingSpinner) {
        loadingSpinner.remove();
    }
}

// Function to show validation error message
function showValidationError(inputElement, message) {
    // Clear any existing error
    clearValidationError(inputElement);
    
    // Create error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'invalid-feedback';
    errorElement.textContent = message;
    
    // Add error class to input
    inputElement.classList.add('is-invalid');
    
    // Insert error message after input
    inputElement.parentNode.appendChild(errorElement);
}

// Function to clear validation error
function clearValidationError(inputElement) {
    inputElement.classList.remove('is-invalid');
    const errorElement = inputElement.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.remove();
    }
}

// Function to validate a form
function validateForm(formElement) {
    let isValid = true;
    
    // Check all required inputs
    const requiredInputs = formElement.querySelectorAll('[required]');
    requiredInputs.forEach(input => {
        if (!input.value.trim()) {
            showValidationError(input, 'This field is required');
            isValid = false;
        } else {
            clearValidationError(input);
        }
    });
    
    // Check email format
    const emailInputs = formElement.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        if (input.value.trim() && !isValidEmail(input.value)) {
            showValidationError(input, 'Please enter a valid email address');
            isValid = false;
        }
    });
    
    return isValid;
}

// Function to validate email format
function isValidEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

// Function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}
