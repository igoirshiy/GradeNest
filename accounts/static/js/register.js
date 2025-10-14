document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");

  const firstname = document.getElementById("firstname");
  const lastname = document.getElementById("lastname");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const terms = document.getElementById("terms");

  const firstnameError = document.getElementById("firstnameError");
  const lastnameError = document.getElementById("lastnameError");
  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");
  const confirmPasswordError = document.getElementById("confirmPasswordError");
  const termsError = document.getElementById("termsError");

  const togglePassword = document.getElementById("togglePassword");

  // Toggle show/hide password
  togglePassword.addEventListener("click", () => {
    password.type = password.type === "password" ? "text" : "password";
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    let valid = true;

    // Reset error states
    [firstnameError, lastnameError, emailError, passwordError, confirmPasswordError, termsError].forEach(err => {
      err.style.display = "none";
    });
    [firstname, lastname, email, password, confirmPassword].forEach(input => input.classList.remove("input-error"));

    const namePattern = /^[A-Za-z\s]+$/;

    // First Name validation
    if (firstname.value.trim() === "") {
      firstnameError.innerText = "First name is required";
      firstnameError.style.display = "block";
      firstname.classList.add("input-error");
      valid = false;
    } else if (!namePattern.test(firstname.value.trim())) {
      firstnameError.innerText = "Please enter a valid first name";
      firstnameError.style.display = "block";
      firstname.classList.add("input-error");
      valid = false;
    }

    // Last Name validation
    if (lastname.value.trim() === "") {
      lastnameError.innerText = "Last name is required";
      lastnameError.style.display = "block";
      lastname.classList.add("input-error");
      valid = false;
    } else if (!namePattern.test(lastname.value.trim())) {
      lastnameError.innerText = "Please enter a valid last name";
      lastnameError.style.display = "block";
      lastname.classList.add("input-error");
      valid = false;
    }

    // Email validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,}$/;
    if (email.value.trim() === "") {
      emailError.innerText = "Email is required";
      emailError.style.display = "block";
      email.classList.add("input-error");
      valid = false;
    } else if (!email.value.match(emailPattern)) {
      emailError.innerText = "Please enter a valid email address";
      emailError.style.display = "block";
      email.classList.add("input-error");
      valid = false;
    }

    // Password validation
    const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
    if (password.value.trim() === "") {
      passwordError.innerText = "Password is required";
      passwordError.style.display = "block";
      password.classList.add("input-error");
      valid = false;
    } else if (!password.value.match(passwordPattern)) {
      passwordError.innerText = "Password should have 8+ chars, 1 uppercase, 1 number, 1 special char";
      passwordError.style.display = "block";
      password.classList.add("input-error");
      valid = false;
    }

    // Confirm Password
    if (confirmPassword.value.trim() === "") {
      confirmPasswordError.innerText = "Confirm Password is required";
      confirmPasswordError.style.display = "block";
      confirmPassword.classList.add("input-error");
      valid = false;
    } else if (password.value !== confirmPassword.value) {
      confirmPasswordError.innerText = "Passwords don't match";
      confirmPasswordError.style.display = "block";
      confirmPassword.classList.add("input-error");
      valid = false;
    }

    // Terms checkbox
    if (!terms.checked) {
      termsError.innerText = "You must accept the terms and conditions to register an account.";
      termsError.style.display = "block";
      valid = false;
    }

    if (valid) {
    form.submit();  // sends the form data to Django
}


    // ✅ Submit form to Django backend
    form.submit();


  });
});
