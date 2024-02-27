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

function onKeystory() {
  const contentValue = document
    .querySelector("#storycontent")
    .value.toLowerCase();
  const messageElement = document.querySelector("#messagejs");
  const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces from length

  if (contentLength < 50) {
    messageElement.innerText = "Story must be above 50 characters";
    document.querySelector(".storypostbtn").style.cursor = "not-allowed";
  } else {
    const hasBadWord = badWords.some((word) =>
      new RegExp(`\\b${word}\\b`).test(contentValue)
    );

    if (hasBadWord) {
      messageElement.innerText = "Bad Word Detected";
      document.querySelector(".storypostbtn").style.cursor = "not-allowed";
    } else {
      messageElement.innerText = "";
      document.querySelector(".storypostbtn").style.cursor = "pointer";
    }
  }
}

function validateForm() {
  const contentValue = document
    .querySelector("#storycontent")
    .value.toLowerCase();
  const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces

  if (contentLength < 50) {
    document.querySelector("#messagejs").innerText =
      "Confession must be above 50 characters";
    document.querySelector(".storypostbtn").style.cursor = "not-allowed";
    return false;
  }
  if (badWords.some((word) => contentValue.includes(word))) {
    document.querySelector("#messagejs").innerText = "Bad Word Detected";
    document.querySelector(".storypostbtn").style.cursor = "not-allowed";
    return false;
  }
  return true;
}

// to validate the subject of story
function storySubjectValid() {
  let subject = document.getElementById("subject").value.toLowerCase();
  let trimmedSubject = subject.trim();
  const subjectLength = subject.replace(/\s/g, "").length;
  if (!trimmedSubject) {
    document.querySelector("#messagejs").innerText =
      "Please enter your subject";
    document.querySelector(".storypostbtn").disabled = true;
    document.querySelector(".storypostbtn").style.cursor = "not-allowed";
  } else if (subjectLength < 4) {
    document.querySelector("#messagejs").innerHTML =
      "Subject must be at least 4 characters";
    document.querySelector(".storypostbtn").disabled = true;
    document.querySelector(".storypostbtn").style.cursor = "not-allowed";
  } else {
    document.querySelector("#messagejs").innerHTML = "";
    document.querySelector(".storypostbtn").disabled = false;
    document.querySelector(".storypostbtn").style.cursor = "pointer";
  }
}

// Full form validation of story
function validateStoryForm() {
  const subjectValue = document
    .querySelector("#subject")
    .value.trim()
    .toLowerCase();
  const contentValue = document
    .querySelector("#storycontent")
    .value.trim()
    .toLowerCase();

  if (!subjectValue || !contentValue) {
    alert("Please fill in both subject and content before submitting.");
    return false;
  } else {
    return true;
  }
}
