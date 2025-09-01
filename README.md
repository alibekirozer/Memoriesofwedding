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

Yüklenen dosyalar varsayılan olarak `static/uploads/` klasörüne kaydedilir.
Her fotoğraf benzersiz bir adla saklanır; böylece aynı dosya adını kullanan
farklı yüklemeler önceki fotoğrafların üzerine yazılmaz.

## Firebase Storage Ayarları

Web arayüzünden Firebase Storage'a yükleme yapabilmek için proje ayarlarını girmelisiniz. Bu bilgileri almak için:

1. [Firebase Console](https://console.firebase.google.com/) üzerinden projenizi açın.
2. Sol üstten **Project settings** (Proje ayarları) menüsüne gidin.
3. **General** sekmesinde "Your apps" bölümünden web uygulamanızı seçin veya yeni bir web uygulaması ekleyin.
4. Çıkan "Firebase SDK snippet" kısmından `apiKey`, `authDomain`, `projectId`, `storageBucket`, `messagingSenderId` ve `appId` değerlerini kopyalayın.

Bu değerleri sunucunuzda ortam değişkeni olarak tanımlayın:

```bash
export FIREBASE_API_KEY="<apiKey>"
export FIREBASE_AUTH_DOMAIN="<authDomain>"
export FIREBASE_PROJECT_ID="<projectId>"
export FIREBASE_STORAGE_BUCKET="<storageBucket>"
export FIREBASE_MESSAGING_SENDER_ID="<messagingSenderId>"
export FIREBASE_APP_ID="<appId>"
```

Uygulama bu değişkenleri kullanarak `templates/upload.html` içerisinde Firebase SDK'sını yapılandırır.

Frontend üzerinden yapılan yüklemeler Firebase Storage içinde `uploads/` klasöründe benzersiz adlarla saklanır; böylece aynı ada sahip dosyalar çakışmaz.

## QR Kod Oluşturma

QR kod oluşturmak için [qr-code-generator.com](https://www.qr-code-generator.com/)
gibi ücretsiz servisleri kullanabilir ve hedef URL olarak yukarıdaki adresi
belirtebilirsiniz.

## Dosyalar

- `app.py`: Fotoğraf yükleme servisini çalıştıran Flask uygulaması.
- `templates/`: HTML şablonları.
- `requirements.txt`: Gerekli Python paketleri.
