// for login page starts----------------------------
function loginSubmit() {
  const logusername = document.querySelector("#logusername").value;
  const logpassword = document.querySelector("#logpassword").value;
  let clearuname = logusername.replace(/\s/g, '');
  let clearupassword = logpassword.replace(/\s/g, '');

  if (!clearuname || !clearupassword) {
    alert("Please fill your username and password");
    return false;
  }

  return true;
}
// for login page ends----------------------------


// Full form validation of signup
function onSignupSubmit() {
  // const intro = document.querySelector("#intro").value.trim();
  const username = document.querySelector("#username").value.trim();
  const email = document.querySelector("#email").value.trim();
  const password = document.querySelector("#password").value.trim();
  const cpassword = document.querySelector("#cpassword").value.trim();

  if (!username || !email || !password || !cpassword) {
    alert("Please fill all form before submitting.");
    return false;
  }

  return true;
}
// for all validation
let message = document.getElementById("quickmessage");
let submitButton = document.querySelector(".copybtn");
let editbtn = document.querySelector("#editbtn");
// to valiadte ussername
function usernameValid() {
  let username = document.getElementById("username").value.trim();
  if (!username) {
    message.innerHTML = "Please enter your username";
    submitButton.style.cursor = "not-allowed";
    submitButton.disabled = true;
  } else {
    let usernameRegex = /^[a-zA-Z][a-zA-Z0-9]*$/;
    if (!usernameRegex.test(username)) {
      submitButton.style.cursor = "not-allowed";
      message.innerHTML =
        "Invalid username. Please follow the specified rules. <ul><li>Username must start with character.</li> <li>Username should not have spaces.</li><li>Username shoud be Unique.</li><ul>";
      submitButton.disabled = true;
    } else {
      message.innerHTML = "";
      submitButton.style.cursor = "pointer";
      submitButton.disabled = false;
    }
  }
}

// to verify the intro
function introValid() {
  let intro = document.getElementById("intro").value;
  if (!intro) {
    message.innerHTML = "Please enter your intro";
    editbtn.disabled = true;
    editbtn.style.cursor = "not-allowed";
  } else if (intro.length > 40) {
    message.innerHTML = "Intro should not be more than 40 characters";
    editbtn.disabled = true;
    editbtn.style.cursor = "not-allowed";
  } else {
    message.innerHTML = "";
    editbtn.disabled = false;
    editbtn.style.cursor = "pointer";
  }
}
function introFormValid() {
  let intro = document.getElementById("intro").value;
  let clearIntro = intro.replace(/\s/g, '');
  if (!clearIntro) {
    message.innerHTML = "No intro was provided";
    return false;
  }

  return true;
}

// to verify the email
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
      message.innerHTML = "Invalid email. Please enter a valid email address (only @gmail.com supported)";
      submitButton.disabled = true;
    } else {
      message.innerHTML = "";
      submitButton.style.cursor = "pointer";
      submitButton.disabled = false;
    }
  }
}

// to verify the password
function passwordValid() {
  let password = document.getElementById("password").value;
  if (!password) {
    message.innerHTML = "Please enter your password";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else if (password.length < 8 || password.length > 32) {
    message.innerHTML = "Password must be between 8 and 32 characters";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else if (!/\d/.test(password)) {
    message.innerHTML = "Password must include at least one number";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    message.innerHTML = "Password must include at least one special character";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else if (!/[A-Z]/.test(password)) {
    message.innerHTML = "Password must include at least one capital letter";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else {
    message.innerHTML = "";
    submitButton.style.cursor = "pointer";
    submitButton.disabled = false;
  }
}

// password match validation
function passwordMatchValid() {
  let password = document.getElementById("password").value;
  let cpassword = document.getElementById("cpassword").value;
  if (password != cpassword) {
    message.innerHTML = "Password is not matching...";
    submitButton.disabled = true;
    submitButton.style.cursor = "not-allowed";
  } else {
    message.innerHTML = "";
    submitButton.style.cursor = "pointer";
    submitButton.disabled = false;
  }
}


function handleFileChange(input) {
  const file = input.files[0];
  const errorMessage = document.getElementById('error-message');
  const imagePreview = document.getElementById('image-preview');
  const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
  
  if (file && !allowedExtensions.exec(file.name)) {
      errorMessage.style.display = 'block';
      input.value = ''; 
      imagePreview.innerHTML = ''; 
  } else {
      errorMessage.style.display = 'none';
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