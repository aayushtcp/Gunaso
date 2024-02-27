// Script to stop bad comments and check content length
const badWords = [
  "badword",
  "fuck",
  "bitch",
  "dick",
  "ass",
  "asshole",
  "pussy",
  "lado",
  "puti",
  "chikne",
  "machikne",
  "machikney",
  "machikni",
  "randi",
  "radi",
];
// validation for group name
function validateGroupName() {
  const contentValue = document.querySelector("#groupName").value.toLowerCase();
  const messageElement = document.querySelector("#messagejs");
  const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces from length

  if (contentLength <= 0) {
    messageElement.innerText = "";
    document.querySelector(".groupbtn").style.cursor = "not-allowed";
    document.querySelector(".groupbtn").disabled = true;
  } else if (contentLength < 4 || contentLength > 30) {
    messageElement.innerText = "Group Name must be  04 - 30 characters";
    document.querySelector(".groupbtn").style.cursor = "not-allowed";
    document.querySelector(".groupbtn").disabled = true;
  } else {
    const hasBadWord = badWords.some((word) =>
      new RegExp(`\\b${word}\\b`).test(contentValue)
    );

    if (hasBadWord) {
      messageElement.innerText = "Bad Word Detected";
      document.querySelector(".groupbtn").style.cursor = "not-allowed";
      document.querySelector(".groupbtn").disabled = true;
    } else {
      messageElement.innerText = "";
      document.querySelector(".groupbtn").style.cursor = "pointer";
    }
  }
}
// validation for group intro
function validateGroupIntro() {
  const contentValue = document
    .querySelector("#groupIntro")
    .value.toLowerCase();
  const messageElement = document.querySelector("#messagejs");
  const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces from length

  if (contentLength <= 0) {
    messageElement.innerText = "";
    document.querySelector(".groupbtn").style.cursor = "not-allowed";
    document.querySelector(".groupbtn").disabled = true;
  } else if (contentLength < 6 || contentLength > 36) {
    messageElement.innerText = "Group Name must be  06 - 36 characters";
    document.querySelector(".groupbtn").style.cursor = "not-allowed";
    document.querySelector(".groupbtn").disabled = true;
  } else {
    const hasBadWord = badWords.some((word) =>
      new RegExp(`\\b${word}\\b`).test(contentValue)
    );

    if (hasBadWord) {
      messageElement.innerText = "Bad Word Detected";
      document.querySelector(".groupbtn").style.cursor = "not-allowed";
      document.querySelector(".groupbtn").disabled = true;
    } else {
      messageElement.innerText = "";
      document.querySelector(".groupbtn").style.cursor = "pointer";
    }
  }
}

// Full form validation of group
function submitCreateGroup() {
  const groupName = document
    .querySelector("#groupName")
    .value.trim()
    .toLowerCase();
  const groupIntro = document
    .querySelector("#groupIntro")
    .value.trim()
    .toLowerCase();

  if (!groupName || !groupIntro) {
    alert("Please fill in both Group Name and Intro before submitting.");
    return false;
  } else {
    return true;
  }
}

// to display image in div
function displayImage(input) {
  var file = input.files[0];
  if (file) {
    var reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById("imagecontainer").style.backgroundImage =
        "url(" + e.target.result + ")";
    };
    reader.readAsDataURL(file);
  }
}
