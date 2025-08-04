// Generate a few small floating daisies for a subtle background
const count = 8; // fewer daisies for a minimal look
for (let i = 0; i < count; i++) {
  const daisy = document.createElement('div');
  daisy.className = 'daisy';
  daisy.style.left = Math.random() * 100 + '%';
  daisy.style.top = Math.random() * 100 + '%';
  daisy.style.animationDelay = `${Math.random() * -8}s`;

  for (let j = 0; j < 8; j++) {
    const petal = document.createElement('span');
    petal.className = 'petal';
    daisy.appendChild(petal);
  }

  const center = document.createElement('span');
  center.className = 'center';
  daisy.appendChild(center);

  document.body.appendChild(daisy);
}
