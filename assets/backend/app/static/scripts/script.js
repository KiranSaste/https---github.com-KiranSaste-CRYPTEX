'use strict';


// add event on element

const addEventOnElem = function (elem, type, callback){
    if (elem.length > 1) {
        for (let i = 0; i < elem.length; i++){
            elem[i].addEventListener(type, callback);

        }
    } else{
        elem.addEventListener(type,callback);
    }
}




// navbar toggle

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");

const toggleNavbar = function () {
    navbar.classList.toggle("active");
    navToggler.classList.toggle("active");
    document.body.classList.toggle("active");
}

addEventOnElem(navToggler, "click", toggleNavbar);


// 12/02/2025  26:37 work done upto navbar 

// strat 13/02/2025 morning

const closeNavbar = function () {
    navbar.classList.remove("active");
    navToggler.classList.remove("active");
    document.body.classList.remove("active");
}

addEventOnElem(navbarLinks, "click", closeNavbar);



// header active video code
/** 
 const header = document.querySelector("[data-header]");

 
const activeHeader = function () {
    if (window.scrollY > 300){
        header.classList.add("active");

    }else {
        header.classList.remove("active");
    }    
}

addEventOnElem( window, "scroll", activeHeader);

activeHeader();
*/
// =============================================================================

// header active copilot code
const header = document.querySelector("[data-header]");

const activeHeader = () => {
    console.log("Scroll event detected"); // Debugging log
    if (window.scrollY > 300) {
        header.classList.add("active");
        console.log("Header activated"); // Debugging log
    } else {
        header.classList.remove("active");
        console.log("Header deactivated"); // Debugging log
    }
}

addEventOnElem(window, "scroll", activeHeader);

// Initial check in case the page is already scrolled
activeHeader();

/*
**toggle active on add to fav 
*/

const addToFavBtns = document.querySelectorAll("[data-add-to-fav]");

const toggleActive = function () {

    this.classList.toggle("active");
   /** OR
    * for (let i = 0; i < adToFavBtns.length; i++){
        adToFavBtns[i].classList.toggle("active");
    } */ 
}

addEventOnElem(addToFavBtns, "click", toggleActive);


/**
 * scroll revereal effect
 */

const sections = document.querySelectorAll("[data-section]");

const scrollReveal = function () {
    for (let i = 0; i < sections.length; i++){
        if(sections[i].getBoundingClientRect().top < window.innerHeight / 1.5){
            sections[i].classList.add("active");
        } else {
            sections[i].classList.remove("active");
        }

    }
}
scrollReveal();

addEventOnElem(window, "scroll", scrollReveal);

