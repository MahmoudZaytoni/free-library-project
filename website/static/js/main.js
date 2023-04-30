'use strict';
const activePage = window.location;

const sidebarLinks = document
  .querySelectorAll('.sidebar ul li a')
  .forEach(link => {
    if (link.href == activePage.href) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

// select the like button element
const btnFavourite = document.querySelector('#favorite--button');

if (btnFavourite) {
  const updateFavourite = function (bookId, likeAction) {
    // send an AJAX request to the Flask route using fetch
    fetch(`/book/${bookId}/${likeAction}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then(data => {
        // update the like count on the page
        console.log(`${data.likes} Likes`);
      })
      .catch(error => {
        // handle errors
        console.error(error);
      });
  };

  // listen for the click event on the like button
  btnFavourite.addEventListener('click', function (e) {
    e.preventDefault();

    // get the book id from a data attribute on the like button
    const bookId = btnFavourite.dataset.bookId;
    const heartIcon = btnFavourite.querySelector('.fa-heart');

    if (btnFavourite.dataset.favor === 'False') {
      heartIcon.classList.remove('far');
      heartIcon.classList.add('fas');
      btnFavourite.dataset.favor = 'True';
      updateFavourite(bookId, 'like');
    } else {
      heartIcon.classList.remove('fas');
      heartIcon.classList.add('far');
      btnFavourite.dataset.favor = 'False';
      updateFavourite(bookId, 'unlike');
    }
  });
}
