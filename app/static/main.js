console.log(window.innerWidth);
const menuToggle = document.querySelector('.menu-toggle');
const navList = document.querySelector('.nav-list');

menuToggle.addEventListener('click', () => {
navList.classList.toggle('active');
});

function resize() {
  img = document.querySelector('img');
  maxwidth = 600;
  currentWidth = window.innerWidth;
  if (currentWidth < maxwidth && img.src !== 'static/Add_a_heading_1.png') {
    img.removeAttribute('src');
    img.setAttribute('src', 'static/Add_a_heading_1.png');
  }
  else if (img.src !== 'static/Add_a_heading.png' && currentWidth > maxwidth){
    img.removeAttribute('src');
    img.setAttribute('src', 'static/Add_a_heading.png');         
  };
}
resize();
window.addEventListener('resize', resize)
