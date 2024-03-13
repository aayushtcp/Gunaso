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

function onKey() {
  const contentValue = document.querySelector("#content").value.toLowerCase();
  const messageElement = document.querySelector("#messagejs");
  const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces from length

  if (contentLength <= 0) {
    messageElement.innerText = "";
    document.querySelector(".postbtn").style.cursor = "not-allowed";
  } else if (contentLength < 30) {
    messageElement.innerText = "Confession must be above 30 characters";
    document.querySelector(".postbtn").style.cursor = "not-allowed";
  } else {
    const hasBadWord = badWords.some((word) =>
      new RegExp(`\\b${word}\\b`).test(contentValue)
    );

    if (hasBadWord) {
      messageElement.innerText = "Bad Word Detected";
      document.querySelector(".postbtn").style.cursor = "not-allowed";
    } else {
      messageElement.innerText = "";
      document.querySelector(".postbtn").style.cursor = "pointer";
    }
  }
}

function validateForm() {
  const contentValue = document.querySelector("#content").value.toLowerCase();
  const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces
  const paddedContent = ` ${contentValue} `; // Add spaces at both ends

  if (contentLength < 30) {
    document.querySelector("#messagejs").innerText =
      "Confession must be above 30 characters";
    document.querySelector(".postbtn").style.cursor = "not-allowed";
    return false;
  }
  if (badWords.some((word) => paddedContent.includes(` ${word} `))) {
    document.querySelector("#messagejs").innerText = "Bad Word Detected";
    document.querySelector(".postbtn").style.cursor = "not-allowed";
    return false;
  }
  return true;
}


// // reply of group comments form validations
// function onKey2() {
//   const contentValue = document
//     .querySelector(".contentreply")
//     .value.toLowerCase();
//   const messageElement = document.querySelector("#messagejsreply");
//   const contentLength = contentValue.replace(/\s/g, "").length; // Exclude spaces from length

//   if (contentLength <= 0) {
//     messageElement.innerText = "";
//     document.querySelector(".replybtn").style.cursor = "not-allowed";
//     document.querySelector(".replybtn").disabled = true;
//   } else if (contentLength < 10) {
//     messageElement.innerText = "Confession Reply must be above 10 characters";
//     document.querySelector(".replybtn").style.cursor = "not-allowed";
//     document.querySelector(".replybtn").disabled = true;
//   } else {
//     const hasBadWord = badWords.some((word) =>
//       new RegExp(`\\b${word}\\b`).test(contentValue)
//     );

//     if (hasBadWord) {
//       messageElement.innerText = "Bad Word Detected";
//       document.querySelector(".replybtn").style.cursor = "not-allowed";
//       document.querySelector(".replybtn").disabled = true;
//     } else {
//       messageElement.innerText = "";
//       document.querySelector(".replybtn").style.cursor = "pointer";
//     }
//   }
// }

// for main image animation on click
// profile image click animation starts
function profileimg() {
  if (window.innerWidth >= 600) {
    document.querySelector(".profileimg").style.height = "100vh";
    document.querySelector(".profileimg").style.backgroundSize = "cover";
  }
}

function toggleProfileImg() {
  var profileImg = document.querySelector(".profileimg");
  var rightSide = document.querySelector(".rightside");

  if (profileImg.style.height === "100vh") {
    profileImg.style.height = "";
    profileImg.style.width = "";
    profileImg.style.backgroundSize = "";
  } else {
    profileimg();
  }
}
