document.addEventListener('DOMContentLoaded', () => {
    // Helper function to display messages
    const displayMessage = (elementId, message, isError = false) => {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.style.color = isError ? 'red' : 'green';
    };

    // Register user
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('register-username').value.trim();
        const password = document.getElementById('register-password').value.trim();

        try {
            const response = await fetch('/api/v1/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const result = await response.json();
            if (response.ok) {
                displayMessage('register-message', 'Registration successful!');
            } else {
                displayMessage('register-message', result.detail || 'Registration failed.', true);
            }
        } catch (error) {
            displayMessage('register-message', 'Error connecting to the server.', true);
        }
    });

    // Login user
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value.trim();

        try {
            const response = await fetch('/api/v1/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const result = await response.json();
            if (response.ok) {
                localStorage.setItem('access_token', result.access_token);
                displayMessage('login-message', 'Login successful!');
            } else {
                displayMessage('login-message', result.detail || 'Login failed.', true);
            }
        } catch (error) {
            displayMessage('login-message', 'Error connecting to the server.', true);
        }
    });

    // Gemini API request
    document.getElementById('gemini-request').addEventListener('click', async () => {
        const token = localStorage.getItem('access_token');
        const text = document.getElementById('gemini-text').value.trim();

        if (!token) {
            displayMessage('gemini-response', 'Please log in first.', true);
            return;
        }

        if (!text) {
            displayMessage('gemini-response', 'Please enter text for the API request.', true);
            return;
        }

        try {
            const response = await fetch('/api/v1/gemini/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ text }),
            });

            const result = await response.json();
            if (response.ok) {
                displayMessage('gemini-response', result.gemini_response || 'Request successful!');
            } else {
                displayMessage('gemini-response', result.detail || 'Request failed.', true);
            }
        } catch (error) {
            displayMessage('gemini-response', 'Error connecting to the server.', true);
        }
    });
});
