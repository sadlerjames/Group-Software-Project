//this code effectively shows the menu for mobile view if a mobile is being used to access the webpage, otherwise the usual desktop view shows
        //the menu simply has the same features but as a dropdown menu
$(document).ready(function() {
    var mobileMenuBtn = document.querySelector("#mobile-menu-btn");
    var mobileMenu = document.querySelector(".mobile-menu");
    mobileMenuBtn.addEventListener("click", () => {
    if (mobileMenu.style.display === "none") {
        mobileMenu.style.display = "flex";
        mobileMenuBtn.innerHTML = "Close";
    } 
    else {
        mobileMenu.style.display = "none";
        mobileMenuBtn.innerHTML = "Menu";
    }
    });
});