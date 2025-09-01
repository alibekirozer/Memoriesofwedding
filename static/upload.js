// Handle file uploads to Firebase Storage
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');

form.addEventListener('submit', function (e) {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) {
    alert('Lütfen bir dosya seçin.');
    return;
  }

  const uniqueName = Date.now() + '-' + file.name;
  const storageRef = window.storage.ref(uniqueName);

  storageRef.put(file)
    .then(() => {
      alert('Dosya başarıyla yüklendi!');
      fileInput.value = '';
    })
    .catch((error) => {
      console.error('Yükleme sırasında hata:', error);
      alert('Yükleme sırasında hata: ' + error.message);
    });
});
