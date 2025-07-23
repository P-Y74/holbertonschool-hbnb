document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById("email");
      const password = document.getElementById("password")

      if (email.value == "" || password.value == "") {
        alert("Ensure you input a value in both fields");
      } else {
        const success = await loginUser(email.value, password.value);

        if (success) {
          email.value = "";
          password.value = "";
        }
      }
    });
  }
});

async function loginUser(email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index';

  } else {
    alert('Login failed: ' + response.statusText);
  }
}
