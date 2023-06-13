const stars = document.querySelectorAll('.stars span');
const ratingValue = document.querySelector('.stars').getAttribute('data-rating');
const rating = document.querySelector('#calificacion');

stars.forEach((star, index) => {
  if (index < ratingValue) {
    star.classList.add('active');
  }

  star.addEventListener('click', () => {
    rating.value = index + 1;
    let ratingValue2 = rating.value;

    stars.forEach((star, index) => {

      if (index < ratingValue2) {
        star.classList.add('stars_active');
      } else {
        star.classList.remove('stars_active');
      }
    });
  });
});