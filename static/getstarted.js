// Sign-in form submission
document.getElementById("signinForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const username = document.getElementById("signinUsername").value;
    const password = document.getElementById("signinPassword").value;
    const output = document.getElementById("signinOutput");
    output.innerHTML = "<p>Processing...</p>";

    try {
        const response = await fetch('/signin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const result = await response.json();
        if (result.success) {
            // Redirect to the dashboard
            window.location.href = "/dashboard";
        } else {
            output.innerHTML = `<p style="color: red;">${result.message || "Signin failed!"}</p>`;
        }
    } catch (error) {
        output.innerHTML = `<p style="color: red;">Server error. Please try again later.</p>`;
    }
});

// Sign-up form submission
document.getElementById("signupForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const username = document.getElementById("signupUsername").value;
    const password = document.getElementById("signupPassword").value;
    const otp = document.getElementById("otp").value;
    const output = document.getElementById("signupOutput");
    output.innerHTML = "<p>Processing...</p>";

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, username, password, otp })
        });
        const result = await response.json();
        if (result.success) {
            window.location.href = "/dashboard";
        } else {
            output.innerHTML = `<p style="color: red;">${result.message || "Signup failed!"}</p>`;
        }
    } catch (error) {
        output.innerHTML = `<p style="color: red;">Server error. Please try again later.</p>`;
    }
});

function showSignUp() {
    document.getElementById('sign-in-form').classList.add('hidden');
    document.getElementById('sign-up-form').classList.remove('hidden');
}

function showSignIn() {
    document.getElementById('sign-up-form').classList.add('hidden');
    document.getElementById('sign-in-form').classList.remove('hidden');
}

function sendOtp() {
    const email = document.getElementById('email').value;
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;

    if (email && username && password) {
        // Send OTP request to the server
        fetch('/send_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, username: username, password: password })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                document.getElementById('otp').classList.remove('hidden');
                document.getElementById('sendOtpButton').classList.add('hidden');
                document.getElementById('signupButton').classList.remove('hidden');
            } else {
                document.getElementById('signupOutput').innerText = data.message;
            }
        }).catch(error => {
            document.getElementById('signupOutput').innerText = 'Failed to send OTP. Please try again.';
        });
    } else {
        document.getElementById('signupOutput').innerText = 'Please fill in all fields.';
    }
}