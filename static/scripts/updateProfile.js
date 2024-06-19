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
let message = document.getElementById("quickmessage");

function emailValid() {
  let email = document.getElementById("email").value;
  if (!email) {
    message.innerHTML = "Please enter your email address";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else {
    // let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // old is right too but only doing gmail for now
    const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    if (!emailRegex.test(email)) {
      submitButton.style.cursor = "not-allowed";
      message.innerHTML =
        "Invalid email. Please enter a valid email address (only @gmail.com supported)";
      submitButton.disabled = true;
    } else {
      message.innerHTML = "";
      submitButton.style.cursor = "pointer";
      submitButton.disabled = false;
    }
  }
}

function handleFileChange(input) {
  const file = input.files[0];
  const errorMessage = document.getElementById("error-message");
  const imagePreview = document.getElementById("image-preview");
  const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;

  if (file && !allowedExtensions.exec(file.name)) {
    errorMessage.style.display = "block";
    input.value = "";
    imagePreview.innerHTML = "";
  } else {
    errorMessage.style.display = "none";
    displayImage(input);
  }
}

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
