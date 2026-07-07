const menuhamburger = document.querySelector('.menu-hamburger')
const navsec = document.querySelector('.navbar-secondaire')
const navprin = document.querySelector('.navbar-principale')
menuhamburger.addEventListener('click',() => {
    navprin.classList.toggle('mobile-menu')
    navsec.classList.toggle('mobile-menu')
})