// BeneSafe Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (!alert.classList.contains('alert-permanent')) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    // File upload preview
    setupFileUploadPreview();

    // Drag and drop functionality
    setupDragAndDrop();

    // Form validation enhancements
    setupFormValidation();

    // Dashboard chart initialization
    initializeCharts();
});

// File Upload Preview
function setupFileUploadPreview() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const preview = input.parentNode.querySelector('.file-preview');
                if (preview) {
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            preview.src = e.target.result;
                            preview.style.display = 'block';
                        };
                        reader.readAsDataURL(file);
                    } else {
                        preview.style.display = 'none';
                    }
                }
            }
        });
    });
}

// Drag and Drop Functionality
function setupDragAndDrop() {
    const dropZones = document.querySelectorAll('.drop-zone');

    dropZones.forEach(function(zone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            zone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            zone.classList.add('drag-over');
        }

        function unhighlight(e) {
            zone.classList.remove('drag-over');
        }

        zone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                const input = zone.querySelector('input[type="file"]');
                if (input) {
                    input.files = files;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        }
    });
}

// Form Validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();

                // Show validation feedback
                const invalidInputs = form.querySelectorAll(':invalid');
                invalidInputs.forEach(function(input) {
                    input.classList.add('is-invalid');
                });
            }
            form.classList.add('was-validated');
        });
    });
}

// Chart Initialization
function initializeCharts() {
    // Asset distribution chart
    const assetChartCanvas = document.getElementById('assetChart');
    if (assetChartCanvas) {
        const ctx = assetChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Bank Accounts', 'Insurance', 'Vehicles', 'Property', 'Other'],
                datasets: [{
                    data: [12, 19, 3, 5, 2],
                    backgroundColor: [
                        '#0d6efd',
                        '#198754',
                        '#0dcaf0',
                        '#ffc107',
                        '#6f42c1'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    // Net worth chart
    const netWorthCanvas = document.getElementById('netWorthChart');
    if (netWorthCanvas) {
        const ctx = netWorthCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Net Worth',
                    data: [12000, 15000, 18000, 22000, 25000, 28000],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="loading"></div>';
        element.disabled = true;
    }
}

function hideLoading(element, originalText) {
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
}

// AJAX Helper
function makeRequest(url, method, data, successCallback, errorCallback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]')?.value);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                successCallback(JSON.parse(xhr.responseText));
            } else {
                errorCallback(xhr.status, xhr.responseText);
            }
        }
    };

    xhr.send(JSON.stringify(data));
}
