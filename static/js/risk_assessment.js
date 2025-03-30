document.addEventListener('DOMContentLoaded', function() {
    // Initialize risk assessment form functionality
    initRiskAssessmentForm();
    
    // Initialize visualization of previous assessments
    initPreviousAssessmentsVisualization();
    
    // Initialize risk score gauges
    initRiskGauges();
});

// Function to initialize the risk assessment form
function initRiskAssessmentForm() {
    const riskForm = document.getElementById('risk-assessment-form');
    
    if (!riskForm) return;
    
    // Show/hide related questions based on selections
    const conditionalGroups = document.querySelectorAll('.conditional-group');
    
    conditionalGroups.forEach(group => {
        const triggerInput = document.getElementById(group.getAttribute('data-trigger'));
        const targetGroup = document.getElementById(group.getAttribute('data-target'));
        
        if (triggerInput && targetGroup) {
            // Set initial state
            targetGroup.style.display = triggerInput.checked ? 'block' : 'none';
            
            // Add event listener for changes
            triggerInput.addEventListener('change', function() {
                if (this.checked) {
                    gsap.to(targetGroup, {
                        duration: 0.3,
                        height: 'auto',
                        opacity: 1,
                        display: 'block',
                        ease: 'power2.out'
                    });
                } else {
                    gsap.to(targetGroup, {
                        duration: 0.3,
                        height: 0,
                        opacity: 0,
                        display: 'none',
                        ease: 'power2.in'
                    });
                }
            });
        }
    });
    
    // Validate form on submit
    riskForm.addEventListener('submit', function(e) {
        if (!validateRiskForm()) {
            e.preventDefault();
            showValidationError('Please fill in all required fields');
        } else {
            // Show loading animation
            showLoading();
        }
    });
    
    // Add tooltip information for risk factors
    const riskFactorInputs = document.querySelectorAll('.risk-factor-input');
    riskFactorInputs.forEach(input => {
        const infoIcon = document.createElement('span');
        infoIcon.className = 'info-icon ms-2';
        infoIcon.innerHTML = '<i class="fas fa-info-circle"></i>';
        infoIcon.setAttribute('data-bs-toggle', 'tooltip');
        infoIcon.setAttribute('data-bs-placement', 'right');
        infoIcon.setAttribute('title', input.getAttribute('data-info') || 'Additional information about this risk factor');
        
        const inputLabel = input.closest('.form-check').querySelector('label');
        if (inputLabel) {
            inputLabel.appendChild(infoIcon);
        }
    });
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Function to validate the risk assessment form
function validateRiskForm() {
    const form = document.getElementById('risk-assessment-form');
    if (!form) return true;
    
    // For a simple validation, just check if any visible required fields are empty
    const requiredFields = form.querySelectorAll('[required]:not([type="hidden"])');
    
    for (let field of requiredFields) {
        // Skip hidden fields (from conditional display)
        if (field.closest('.form-group')?.style.display === 'none') continue;
        
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            return false;
        } else {
            field.classList.remove('is-invalid');
        }
    }
    
    return true;
}

// Function to show validation error message
function showValidationError(message) {
    const errorAlert = document.createElement('div');
    errorAlert.className = 'alert alert-danger alert-dismissible fade show mt-3';
    errorAlert.role = 'alert';
    errorAlert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const form = document.getElementById('risk-assessment-form');
    form.prepend(errorAlert);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        const bootstrap = window.bootstrap;
        const alert = bootstrap.Alert.getOrCreateInstance(errorAlert);
        alert.close();
    }, 5000);
}

// Function to initialize visualization of previous assessments
function initPreviousAssessmentsVisualization() {
    const assessmentHistory = document.getElementById('assessment-history');
    if (!assessmentHistory) return;
    
    const canvas = document.getElementById('assessment-history-chart');
    if (!canvas) return;
    
    try {
        // Get data from data attributes
        const dates = JSON.parse(canvas.getAttribute('data-dates') || '[]');
        const pregnancyRisks = JSON.parse(canvas.getAttribute('data-pregnancy-risks') || '[]');
        const anemiaRisks = JSON.parse(canvas.getAttribute('data-anemia-risks') || '[]');
        
        // Create chart
        const ctx = canvas.getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Pregnancy Risk',
                        data: pregnancyRisks,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: false
                    },
                    {
                        label: 'Anemia Risk',
                        data: anemiaRisks,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.parsed.y || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Risk Score (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Assessment Date'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing assessment history chart:', error);
    }
}

// Function to initialize risk gauges
function initRiskGauges() {
    // Get all gauge containers
    const gaugeContainers = document.querySelectorAll('.risk-gauge');
    
    gaugeContainers.forEach(container => {
        try {
            const value = parseFloat(container.getAttribute('data-value') || '0');
            const label = container.getAttribute('data-label') || 'Risk';
            const color = getGaugeColor(value);
            
            // Create gauge element
            const gauge = document.createElement('div');
            gauge.className = 'gauge-body';
            
            // Calculate rotation based on value (0-100)
            const rotation = (value / 100) * 180;
            
            // Create gauge HTML
            gauge.innerHTML = `
                <div class="gauge-fill" style="transform: rotate(${rotation}deg); background-color: ${color};"></div>
                <div class="gauge-cover"></div>
                <div class="gauge-value">${value}%</div>
                <div class="gauge-label">${label}</div>
            `;
            
            // Add gauge to container
            container.appendChild(gauge);
            
            // Animate gauge on load
            setTimeout(() => {
                const fill = gauge.querySelector('.gauge-fill');
                const gaugeValue = gauge.querySelector('.gauge-value');
                
                // Reset rotation to 0 for animation
                fill.style.transform = 'rotate(0deg)';
                gaugeValue.textContent = '0%';
                
                // Animate to actual value
                gsap.to(fill, {
                    duration: 1.5,
                    rotation: rotation,
                    ease: 'power2.out'
                });
                
                let displayValue = { value: 0 };
                gsap.to(displayValue, {
                    duration: 1.5,
                    value: value,
                    ease: 'power2.out',
                    onUpdate: function() {
                        gaugeValue.textContent = Math.round(displayValue.value) + '%';
                    }
                });
            }, 300);
            
        } catch (error) {
            console.error('Error creating gauge:', error);
        }
    });
}

// Function to get appropriate color based on risk value
function getGaugeColor(value) {
    if (value >= 70) {
        return '#dc3545'; // High risk - red
    } else if (value >= 40) {
        return '#ffc107'; // Medium risk - yellow
    } else {
        return '#28a745'; // Low risk - green
    }
}

// Function to show loading spinner
function showLoading() {
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <div class="mt-2">Analyzing risk factors...</div>
    `;
    
    document.body.appendChild(loadingOverlay);
}

// Function to hide loading spinner
function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}
