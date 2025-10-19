document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");

  const fullname = document.getElementById("fullname");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const terms = document.getElementById("terms");

  const fullnameError = document.getElementById("fullnameError");
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

    [fullnameError, emailError, passwordError, confirmPasswordError, termsError].forEach(err => {
      err.style.display = "none";
    });
    [fullname, email, password, confirmPassword].forEach(input => input.classList.remove("input-error"));

    // Full Name validation
    const namePattern = /^[A-Za-z\s]+$/;
    if (fullname.value.trim() === "") {
      fullnameError.innerText = "Full name is required";
      fullnameError.style.display = "block";
      fullname.classList.add("input-error");
      valid = false;
    } else if (!namePattern.test(fullname.value.trim())) {
      fullnameError.innerText = "Please enter a valid name";
      fullnameError.style.display = "block";
      fullname.classList.add("input-error");
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
      emailError.innerText = "Please enter a valid email";
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

    // Confirm Password validation
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

    // Terms
    if (!terms.checked) {
      termsError.innerText = "You must agree to the terms and conditions";
      termsError.style.display = "block";
      valid = false;
    }

    if (valid) {
      form.submit();
    }
  });
});
