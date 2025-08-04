// Place larger daisies asymmetrically in the background
const positions = [
  { left: '5%', top: '10%' },
  { left: '80%', top: '15%' },
  { left: '20%', top: '75%' },
  { left: '60%', top: '55%' },
  { left: '35%', top: '35%' },
];

const container = document.createElement('div');
container.className = 'daisy-container';
document.body.appendChild(container);

positions.forEach(pos => {
  const daisy = document.createElement('img');
  daisy.src = '/static/Daisy.svg';
  daisy.className = 'daisy';
  daisy.style.left = pos.left;
  daisy.style.top = pos.top;
  container.appendChild(daisy);
});
