# Memories of Wedding

Bu basit uygulama, düğüne katılan misafirlerin çektikleri fotoğrafları kolayca
size iletebilmesi için hazırlanmıştır. Artık ana sayfada karşılayıcı bir mesaj,
fotoğraf yükleme formu ve yüklenen fotoğrafları görebileceğiniz bir galeri
bulunmaktadır. Misafirler QR kodu taradıklarında fotoğraf yükleme sayfasına
veya doğrudan ana sayfaya yönlendirilerek cihazlarındaki fotoğrafları "Yükle"
butonu ile paylaşabilirler.

## Kurulum

1. Python 3 ve `pip` yüklü olmalıdır.
2. Gerekli kütüphaneleri kurmak için aşağıdaki komutu çalıştırın:

```bash
pip install -r requirements.txt
```

3. Uygulamayı başlatmak için:

```bash
python app.py
```

Uygulama 5000 portunda çalışacaktır. Ana sayfa `http://<sunucu_adresi>:5000/`
adresinde, fotoğraf yükleme formu `http://<sunucu_adresi>:5000/upload` ve
galeri `http://<sunucu_adresi>:5000/gallery` adresinde yer alır. Örneğin, kendi
bilgisayarınızda test etmek için `http://localhost:5000/` adresini
kullanabilirsiniz.

4. Firebase Storage kullanmak için aşağıdaki ortam değişkenlerini ayarlayın:

   - `GOOGLE_APPLICATION_CREDENTIALS`: Firebase servis hesabı JSON dosyasının yolu (dosyayı depo dışına koyun ve versiyon kontrolüne eklemeyin)
   - `FIREBASE_STORAGE_BUCKET`: Firebase Storage bucket adı (örn. `proje-id.appspot.com`)

   Bu değişkenler ayarlanmazsa yüklenen dosyalar yerel olarak `static/uploads/` klasörüne kaydedilir.

## QR Kod Oluşturma

QR kod oluşturmak için [qr-code-generator.com](https://www.qr-code-generator.com/)
gibi ücretsiz servisleri kullanabilir ve hedef URL olarak yukarıdaki adresi
belirtebilirsiniz.

## Dosyalar

- `app.py`: Fotoğraf yükleme servisini çalıştıran Flask uygulaması.
- `templates/`: HTML şablonları.
- `requirements.txt`: Gerekli Python paketleri.
