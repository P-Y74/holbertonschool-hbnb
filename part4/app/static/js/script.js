let allPlaces = [];

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const path = window.location.pathname;
  const token = getCookie('token');

  if (path.includes('place')) {
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(token, placeId);
  }

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
  const path = window.location.pathname;
  const loginLink = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-button');
  const addReviewSection = document.getElementById('add-review');

  if (logoutButton) {
    logoutButton.addEventListener('click', () => {
      document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
      window.location.href = 'login';
    });
  }

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
    if (logoutButton) logoutButton.style.display = 'none';
    if (addReviewSection) addReviewSection.style.display = 'none';
    if (path.includes('index')) {
      fetchPlaces();
    }

  } else {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutButton) logoutButton.style.display = 'block';
    if (addReviewSection) addReviewSection.style.display = 'block';
    // Fetch places data if the user is authenticated
    if (path.includes('index')) {
      fetchPlaces(token);
    }
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
  // Include the token in the Authorization header
  try {
    let headers = {};
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }
    const response = await fetch('http://localhost:5000/api/v1/places', {
      headers: headers
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // Handle the response and pass the data to displayPlaces function
    const data = await response.json();
    allPlaces = data;
    displayPlaces(allPlaces);
  } catch (error) {
    console.error('Error:', error);
  }
}


function displayPlaces(places) {
  // Clear the current content of the places list
  // Iterate over the places data
  // For each place, create a div element and set its content
  // Append the created element to the places list
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';

    const heading = document.createElement('h1');
    heading.textContent = place.title;

    const paragraph = document.createElement('p');
    paragraph.textContent = 'Price per night: ' + place.price + ' €';

    const a = document.createElement('a');
    a.href = `/place?id=${place.id}`;
    a.className = 'details-button';
    a.textContent = 'View Details';

    const button = document.createElement('button');
    button.className = 'details-button';
    button.textContent = 'View Details';

    div.appendChild(heading);
    div.appendChild(paragraph);
    div.appendChild(a);
    placesList.appendChild(div);
  });
}

const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
  document.getElementById('price-filter').addEventListener('change', (event) => {
    // Get the selected price value
    // Iterate over the places and show/hide them based on the selected price
    const selectedValue = event.target.value;

    if (selectedValue === 'All') {
      displayPlaces(allPlaces);
    } else {
      const filtered = allPlaces.filter(place => place.price <= parseFloat(selectedValue))
      displayPlaces(filtered);
    }
  });
}



function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  let placeId = new URLSearchParams(window.location.search);
  return placeId.get('id');
}


async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaceDetails function
  try {
    let headers = {};
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: headers
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // Handle the response and pass the data to displayPlaces function
    const placeDetail = await response.json();
    displayPlaceDetails(placeDetail);
  } catch (error) {
    console.error('Error:', error);
  }
}

function displayPlaceDetails(place) {
  console.log(place);
  const details = document.getElementById('place-details');
  details.innerHTML = '';

  if (place) {
    const div1 = document.createElement('div');
    const heading = document.createElement('h1');
    heading.id = 'title-page';
    heading.textContent = place.title;

    const div2 = document.createElement('div');
    div2.className = 'place-details place-info';

    const para1 = document.createElement('p');
    para1.textContent = 'Owner: ' + place.owner?.first_name + ' ' + place.owner?.last_name;

    const para2 = document.createElement('p');
    para2.textContent = 'Price: ' + place.price + ' €';

    const para3 = document.createElement('p');
    para3.textContent = 'Description: ' + place.description;

    const para4 = document.createElement('p');
    para4.textContent = 'Amenities: ' + place.amenities;

    div1.appendChild(heading);
    div2.appendChild(para1);
    div2.appendChild(para2);
    div2.appendChild(para3);
    div2.appendChild(para4);
    details.appendChild(div1);
    details.appendChild(div2);
  }
}
