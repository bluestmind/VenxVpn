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



function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" new-active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " new-active";
}

function sendPriceToFlask(button, referralCode, userEmail) {
    var planName = button.parentElement.querySelector('input[name="plan_name"]').value;
    var duration = button.parentElement.querySelector('input[name="duration"]').value;
    var price = button.parentElement.querySelector('input[name="price"]').value;

    fetch('/payment/1', {
        method: 'POST',
        mode: 'cors', // or 'no-cors' if needed
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            plan_name: planName,
            duration: duration,
            price: price,
            referral_code: referralCode,
            user_email: userEmail
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('Price sent successfully');
            // Toggle the modal after sending the price
        } else {
            console.log('Error sending price');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function myFunction() {
    // Get the text field
    var copyText = document.getElementById("copyText");

    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices

    try {
        // Copy the text inside the text field
        navigator.clipboard.writeText(copyText.value)
            .then(function() {

                // Display the success alert message
                var alertMessage = document.getElementById("alertMessage");
                alertMessage.style.display = "block";
                setTimeout(function() {
                    alertMessage.style.display = "none";
                }, 3000);
            })
            .catch(function(err) {
                console.error('Failed to copy: ', err);
                // Handle error if copying fails
            });
    } catch (err) {
        console.error('Unable to copy: ', err);
        // Fallback if Clipboard API is not supported
    }
}



function openModal() {
  const modal = document.getElementById('modal');
  modal.style.display = 'block';
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

function submitForm(userEmail) {
  // Gather form data
  const formData = new FormData(document.getElementById('supportForm'));

  // Append the user's email address to the form data
  formData.append('user_email', userEmail);
  console.log("user email",userEmail)
  // Send AJAX request to Flask route
  fetch('/submit_ticket', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.ok) {
      closeModal(); // Close modal if submission is successful
      alert('Ticket submitted successfully!');
    } else {
      alert('Failed to submit ticket. Please try again.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  });
}
