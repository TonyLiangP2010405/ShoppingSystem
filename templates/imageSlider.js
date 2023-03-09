const mainImg = document.querySelector('.sliderMainImage');
const thumb = document.querySelectorAll('.sliderThumb');
const modalImg = document.querySelector('.modalImage');

for(let i = 0; i < thumb.length; i++) {
  thumb[i].addEventListener('click', () => {
    mainImg.src = thumb[i].src;
    mainImg.classList.add('sliderFade');
    setTimeout(() => {
      mainImg.classList.remove('sliderFade');
    }, 600);
  });
}

mainImg.addEventListener('click', e => {
  modalImg.src = e.target.src;
})