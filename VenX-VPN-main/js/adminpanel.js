/*==================== SHOW NAVBAR ====================*/
const showMenu = (headerToggle, navbarId) => {
    const toggleBtn = document.getElementById(headerToggle),
          nav = document.getElementById(navbarId);

    // Function to close the menu when clicking outside of it
    const closeMenu = (event) => {
        const target = event.target;
        const isNav = target.closest('.nav');
        const isHeaderToggle = target.closest('#header-toggle');

        // Check if the click is inside the navigation or on the toggle button
        if (!isNav && !isHeaderToggle) {
            nav.classList.remove('show-menu');
            toggleBtn.classList.remove('bx-x');
        }
    };

    // Validate that variables exist
    if (headerToggle && navbarId) {
        toggleBtn.addEventListener('click', () => {
            // Toggle the 'show-menu' class
            nav.classList.toggle('show-menu');

            // Toggle the icon class
            toggleBtn.classList.toggle('bx-x');

            // Add event listener to close menu when clicking outside of it
            if (nav.classList.contains('show-menu')) {
                document.addEventListener('click', closeMenu);
            } else {
                document.removeEventListener('click', closeMenu);
            }
        });
    }
};

showMenu('header-toggle', 'navbar');


/*==================== LINK ACTIVE ====================*/
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
    linkColor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}

linkColor.forEach(l => l.addEventListener('click', colorLink))


/*==================== Slider ACTIVE ====================*/
let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}


function openModal(ticketId, userEmail, subtitle, description) {
  const modal = document.getElementById('modal');
  modal.style.display = 'block';

  // Populate ticket details in the modal
  document.getElementById('ticketId').textContent = ticketId;
  document.getElementById('userEmail').textContent = userEmail;
  document.getElementById('subtitle').textContent = subtitle;
  document.getElementById('ticketDescription').textContent = description;
}

function closeModal() {
  const modal = document.getElementById('modal');
  modal.style.display = 'none';
}

window.onclick = function(event) {
  const modal = document.getElementById('modal');
  if (event.target === modal) {
    modal.style.display = 'none';
  }
};

function submitResponse() {
  const userEmail = document.getElementById('userEmail').textContent;
  const ticketId = document.getElementById('ticketId').textContent;
  const response = document.getElementById('response').value;

  // Send AJAX request to Flask route to submit response
  fetch('/submit_response', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ ticketId: ticketId, response: response ,userEmail:userEmail})
  })
  .then(response => {
    if (response.ok) {
      closeModal(); // Close modal if submission is successful
      alert('Response submitted successfully!');
    } else {
      alert('Failed to submit response. Please try again.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  });
}



/*table*/


