var counter = 0;
var allImg = document.querySelectorAll(".each-img");
var imgCount = allImg.length;
var autoSlideInterval; // Variable to store the interval ID

allImg.forEach(function (eachimg, index) {
    eachimg.style.left = `${index * 100}%`;
});

function slideImg() {
    allImg.forEach(function (eachImg) {
        eachImg.style.transform = `translateX(-${counter * 100}%)`;
    });

    // Show/hide Prev and Next buttons
    document.getElementById("prevbtn").style.display =
        counter === 0 ? "none" : "block";
    document.getElementById("nextbtn").style.display =
        counter === imgCount - 1 ? "none" : "block";
}
function nextSlide() {
    counter = (counter + 1) % imgCount;
    slideImg();
}
function prevSlide() {
    counter = Math.max(counter - 1, 0);
    slideImg();
}

function startAutoSlide() {
    autoSlideInterval = setInterval(function () {
        nextSlide();
    }, 5000); //carousel auto change interval
}

function pauseAutoSlide() {
    clearInterval(autoSlideInterval);
}

document.querySelector("#nextbtn").addEventListener("click", function () {
    nextSlide();
    pauseAutoSlide(); // Pause auto-slide when user interacts with the slideshow
});

document.querySelector("#prevbtn").addEventListener("click", function () {
    prevSlide();
    pauseAutoSlide(); // Pause auto-slide when user interacts with the slideshow
});

// Initially hide the Prev button
document.getElementById("prevbtn").style.display = "none";

// Start auto-slide initially
startAutoSlide();