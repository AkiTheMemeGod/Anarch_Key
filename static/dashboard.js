
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
});

// Set username from session
document.getElementById('username').textContent = '{{ session.username }}';
document.getElementById('accountUsername').textContent = '{{ session.username }}';

// Fetch user details including email
fetchUserDetails();

// Load API keys from database
loadApiKeys();

// Load activity data and render graph
loadActivityData();

// Modal functionality - FIXED
const createKeyBtn = document.getElementById('createKeyBtn');
const createKeyModal = document.getElementById('createKeyModal');
const cancelCreateKey = document.getElementById('cancelCreateKey');

createKeyBtn.addEventListener('click', () => {
    createKeyModal.style.display = 'flex';
});

cancelCreateKey.addEventListener('click', () => {
    createKeyModal.style.display = 'none';
});

// Form submission for creating a new key
const createKeyForm = document.getElementById('createKeyForm');
createKeyForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const projectName = document.getElementById('projectName').value;
    const customApiKey = document.getElementById('customApiKey').value;

    // Send request to backend to add the custom API key
    fetch('/add_api_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            project_name: projectName,
            api_key: customApiKey
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            createKeyModal.style.display = 'none';
            showAlert('API key added successfully!', 'success');
            loadApiKeys(); // Refresh the list
        } else {
            showAlert(data.message || 'Failed to add API key', "success");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred while adding the API key', 'error');
    });
});


    // Function to fetch user details
function fetchUserDetails() {
    fetch('/get_user_details', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const emailElement = document.getElementById('accountEmail');
            const memberSinceElement = document.getElementById('memberSince');

            if (emailElement) {
                emailElement.textContent = data.email;
            } else {
                console.error('Element with id "accountEmail" not found.');
            }

            if (memberSinceElement) {
                memberSinceElement.textContent = new Date(data.created_at).toLocaleDateString();
            } else {
                console.error('Element with id "memberSince" not found.');
            }
        } else {
            console.error('Failed to fetch user details:', data.message);
        }
    })
    .catch(error => {
        console.error('Error fetching user details:', error);
    });
}

    // Function to load API keys from database
    function loadApiKeys() {
    fetch('/get_user_api_keys', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const apiKeys = data.api_keys;
            const apiKeysList = document.getElementById('apiKeysList');
            document.getElementById('keyCount').textContent = apiKeys.length;

            if (apiKeys.length > 0) {
                // Clear existing content first
                apiKeysList.innerHTML = '';

                // Remove existing event listener if it exists
                apiKeysList.removeEventListener('click', handleApiKeyActions);

                apiKeys.forEach(key => {
                    const keyItem = document.createElement('div');
                    keyItem.className = 'api-key-item';
                    keyItem.dataset.keyId = key.id;
                    keyItem.dataset.apiKey = key.api_key;

                    keyItem.innerHTML = `
                        <div>
                            <strong>${key.project_name}</strong>
                            <div style="font-size: 0.8rem; opacity: 0.7;">Created: ${new Date(key.created_at).toLocaleDateString()}</div>
                            <div style="font-size: 0.8rem; margin-top: 0.25rem;">
                                <span class="key-badge" title="Number of API calls">${key.usage_count || 0} uses</span>
                            </div>
                        </div>
                        <div class="api-key-actions">
                            <button class="view-btn" type="button">View</button>
                            <button class="delete-btn" type="button">Delete</button>
                        </div>
                    `;

                    apiKeysList.appendChild(keyItem);
                });

                // Add the event listener for delegation
                apiKeysList.addEventListener('click', handleApiKeyActions);

                // Add a separate function for handling the clicks
                function handleApiKeyActions(e) {
                    // Log any click on the container for debugging

                    if (e.target.classList.contains('view-btn')) {
                        const keyItem = e.target.closest('.api-key-item');
                        const apiKey = keyItem.dataset.apiKey;
                        viewApiKey(apiKey);
                    } else if (e.target.classList.contains('delete-btn')) {
                        const keyItem = e.target.closest('.api-key-item');
                        const keyId = keyItem.dataset.keyId;
                        deleteApiKey(keyId);
                    }
                }
            } else {
                apiKeysList.innerHTML = `
                    <div class="empty-state">
                        <i data-lucide="key" style="width: 3rem; height: 3rem; margin-bottom: 1rem;"></i>
                        <p>No API keys found. Create your first key to get started.</p>
                    </div>
                `;
                lucide.createIcons();
            }
        } else {
            console.error('Failed to load API keys:', data.message);
        }
    })
    .catch(error => {
        console.error('Error loading API keys:', error);
    });
}

    // Function to load activity data and render gra

    // Function to render activity chart
document.addEventListener("DOMContentLoaded", () => {
    loadActivityData();
});

function loadActivityData() {
    fetch('/get_api_usage', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const activitySection = document.querySelectorAll('.feature-card')[2];
            const activityContainer = activitySection.querySelector('div:nth-of-type(2)');

            if (!activityContainer) {
                console.error('Activity container not found.');
                return;
            }

            // Create the canvas if it doesn't exist
            let canvas = document.getElementById('activityChart');
            if (!canvas) {
                canvas = document.createElement('canvas');
                canvas.id = 'activityChart';
                canvas.width = 400;
                canvas.height = 200;
                activityContainer.innerHTML = ''; // clear placeholder
                activityContainer.appendChild(canvas);
            }

            renderActivityChart(data.usage);
        } else {
            console.error('Failed to load activity data:', data.message);
        }
    })
    .catch(error => {
        console.error('Error loading activity data:', error);
    });
}

function renderActivityChart(usage) {
    const ctx = document.getElementById('activityChart');
    if (!ctx) {
        console.error('Activity chart canvas not found.');
        return;
    }

    const last7Days = Array.from({ length: 7 }, (_, i) => {
        const date = new Date();
        date.setDate(date.getDate() - i);
        return date.toISOString().split('T')[0];
    }).reverse();

    const countsByDay = last7Days.reduce((acc, day) => {
        acc[day] = 0;
        return acc;
    }, {});

    usage.forEach(call => {
        const day = new Date(call.timestamp).toISOString().split('T')[0];
        if (countsByDay[day] !== undefined) {
            countsByDay[day]++;
        }
    });

    const chartData = {
        labels: last7Days.map(day => new Date(day).toLocaleDateString()),
        datasets: [{
            label: 'API Calls',
            data: Object.values(countsByDay),
            backgroundColor: 'rgba(239, 68, 68, 0.5)',
            borderColor: 'rgba(239, 68, 68, 1)',
            borderWidth: 2,
            tension: 0.2,
            fill: true
        }]
    };

    if (window.activityChart && typeof window.activityChart.destroy === 'function') {
        window.activityChart.destroy();
    }

    const context = ctx.getContext('2d');
    window.activityChart = new Chart(context, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            return tooltipItems[0].label;
                        },
                        label: function(context) {
                            const value = context.parsed.y;
                            return `${value} call${value !== 1 ? 's' : ''}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}
// Function to view API key details
function viewApiKey(apiKey) {

    const viewKeyModal = document.getElementById('viewKeyModal');
    if (!viewKeyModal) {
        // Create modal if it doesn't exist
        const modal = document.createElement('div');
        modal.id = 'viewKeyModal';
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>API Key Details</h3>
                <div style="margin: 1.5rem 0; word-break: break-all; background: rgba(0,0,0,0.05); padding: 1rem; border-radius: 0.5rem;">
                    <code id="apiKeyValue">${apiKey}</code>
                </div>
                <div class="modal-actions">
                    <button type="button" class="secondary-btn" id="closeViewKey">Close</button>
                    <button type="button" class="primary-btn" id="copyApiKey">
                        <i data-lucide="copy" style="width: 1rem; height: 1rem; margin-right: 0.5rem;"></i> Copy
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Add event listeners for new elements
        document.getElementById('closeViewKey').addEventListener('click', () => {
            document.getElementById('viewKeyModal').style.display = 'none';
        });

        document.getElementById('copyApiKey').addEventListener('click', () => {
            navigator.clipboard.writeText(apiKey)
                .then(() => {
                    const copyBtn = document.getElementById('copyApiKey');
                    copyBtn.innerHTML = '<i data-lucide="check" style="width: 1rem; height: 1rem; margin-right: 0.5rem;"></i> Copied!';
                    lucide.createIcons();
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i data-lucide="copy" style="width: 1rem; height: 1rem; margin-right: 0.5rem;"></i> Copy';
                        lucide.createIcons();
                    }, 2000);
                })
                .catch(err => {
                    console.error("Failed to copy: ", err);
                    showAlert("Failed to copy API key to clipboard", 'error');
                });
        });

        lucide.createIcons();
    } else {
        document.getElementById('apiKeyValue').textContent = apiKey;
    }

    document.getElementById('viewKeyModal').style.display = 'flex';
}

// Function to delete an API key
function deleteApiKey(keyId) {

    if (confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
        fetch('/delete_api_key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                key_id: keyId
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
        showAlert('Api Key Deleted Successfully', 'success');
        loadApiKeys(); // Refresh the list
            } else {
                alert(data.message || 'Failed to delete API key');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred while deleting the API key', 'error');
        });
    }
}


function showAlert(message, type = 'success', duration = 3000) {
    const alertBox = document.getElementById('customAlert');
    const alertMessage = document.getElementById('alertMessage');

    // Set the message and type-specific styles
    alertMessage.textContent = message;
    alertBox.className = `custom-alert ${type}`;
    alertBox.classList.remove('hidden');

    // Automatically hide the alert after the specified duration
    setTimeout(() => {
        alertBox.classList.add('hidden');
    }, duration);
}

const accountSettingsForm = document.getElementById('accountSettingsForm');
accountSettingsForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/update_account_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Account settings updated successfully!', 'success');
        } else {
            showAlert(data.message || 'Failed to update account settings', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred while updating account settings', 'error');
    });
});