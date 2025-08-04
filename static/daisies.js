// Generate a few small floating daisies for a subtle background
const count = 8; // fewer daisies for a minimal look
for (let i = 0; i < count; i++) {
  const daisy = document.createElement('img');
  daisy.src = '/static/Daisy.svg';
  daisy.className = 'daisy';
  daisy.style.left = Math.random() * 100 + '%';
  daisy.style.top = Math.random() * 100 + '%';
  daisy.style.animationDelay = `${Math.random() * -8}s`;

  document.body.appendChild(daisy);
}
