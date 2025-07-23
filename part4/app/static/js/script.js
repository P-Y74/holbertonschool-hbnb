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
  checkAuthentication();
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


function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-button');

  if (logoutButton) {
    logoutButton.addEventListener('click', () => {
      document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
      window.location.href = 'login';
    });
  }

  if (!token) {
    loginLink.style.display = 'block';
    logoutButton.style.display = 'none';
  } else {
    loginLink.style.display = 'none';
    logoutButton.style.display = 'block';

    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }


}
function getCookie(name) {
  // Function to get a cookie value by its name
  const cookieString = document.cookie;
  const cookies = cookieString.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}


async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  try {
    const response = await fetch('http://localhost:5000/api/v1/places');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
  // Include the token in the Authorization header

  // Handle the response and pass the data to displayPlaces function
}
