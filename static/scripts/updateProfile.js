// to display image in div
function displayImage(input) {
  var file = input.files[0];
  if (file) {
    var reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById("profilePicContainer").style.backgroundImage =
        "url(" + e.target.result + ")";
    };
    reader.readAsDataURL(file);
  }
}

// for all validation
// let message = document.getElementById("quickmessage");
// let submitButton = document.querySelector(".copybtn");

// function updateProfileClicked() {
//   const username = document.querySelector("#username").value.trim();
//   const email = document.querySelector("#email").value.trim();
//   const password = document.querySelector("#password").value;
//   const cpassword = document.querySelector("#cpassword").value;

//   // Validate username
//   let usernameRegex = /^[a-zA-Z][a-zA-Z0-9]*$/;
//   if (!usernameRegex.test(username)) {
//     displayErrorMessage("Invalid username. Please follow the specified rules. <ul><li>Username must start with a character.</li> <li>Username should not have spaces.</li><li>Username should be unique.</li></ul>");
//     return false;
//   }

//   // Validate email
//   let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   if (!emailRegex.test(email)) {
//     displayErrorMessage("Invalid email. Please enter a valid email address");
//     return false;
//   }

//   // Validate password
//   if (
//     !password ||
//     password.length < 8 ||
//     password.length > 32 ||
//     !/\d/.test(password) ||
//     !/[!@#$%^&*(),.?":{}|<>]/.test(password) ||
//     !/[A-Z]/.test(password)
//   ) {
//     displayErrorMessage("Invalid password. Please follow the specified rules.");
//     return false;
//   }

//   // Validate password match
//   if (password !== cpassword) {
//     displayErrorMessage("Passwords do not match.");
//     return false;
//   }

//   // If all validations pass, allow form submission
//   clearErrorMessage();
//   return true;
// }


// // Display error message
// function displayErrorMessage(msg) {
//   message.innerHTML = msg;
//   submitButton.style.cursor = "not-allowed";
//   submitButton.disabled = true;
// }

// // Clear error message
// function clearErrorMessage() {
//   message.innerHTML = "";
//   submitButton.style.cursor = "pointer";
//   submitButton.disabled = false;
// }
