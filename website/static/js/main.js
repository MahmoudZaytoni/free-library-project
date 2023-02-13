'use strict';
const activePage = window.location;

const sidebarLinks = document.querySelectorAll(".sidebar ul li a").forEach(link => {
  if (link.href == activePage.href) {
    link.classList.add('active');
  } else {
    link.classList.remove('active')
  }
})

