document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const username = document.getElementById("username");
  const password = document.getElementById("password");

  const usernameError = document.getElementById("usernameError");
  const passwordError = document.getElementById("passwordError");

  form.addEventListener("submit", function (e) {

    e.preventDefault(); // prevent default submission until validated
    let valid = true;

    // reset error states
    [usernameError, passwordError].forEach(err => err.style.display = "none");
    [username, password].forEach(input => input.classList.remove("input-error"));

    // check not empty
    if (email.value.trim() === "") {
    emailError.innerText = "Email is required";
    emailError.style.display = "block";
    email.classList.add("input-error");
    valid = false;
}

    if (password.value.trim() === "") {
      passwordError.innerText = "Password is required";
      passwordError.style.display = "block";
      password.classList.add("input-error");
      valid = false;
    }


    if (valid) {
      form.submit(); // sends POST to Django login_view

    }
  });
});
