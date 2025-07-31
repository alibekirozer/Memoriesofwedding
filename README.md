# Memories of Wedding

Bu basit uygulama, düğüne katılan misafirlerin çektikleri fotoğrafları kolayca
size iletebilmesi için hazırlanmıştır. Misafirler QR kodu taradıklarında fotoğraf
yükleme sayfasına yönlendirilir ve cihazlarındaki fotoğrafları "Yükle" butonu
ile paylaşabilirler.

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

Uygulama 5000 portunda çalışacaktır. QR kodunuzu `http://<sunucu_adresi>:5000/upload`
adresine yönlendirebilirsiniz. Örneğin, kendi bilgisayarınızda test etmek için
`http://localhost:5000/upload` adresini kullanabilirsiniz.

## QR Kod Oluşturma

QR kod oluşturmak için [qr-code-generator.com](https://www.qr-code-generator.com/)
gibi ücretsiz servisleri kullanabilir ve hedef URL olarak yukarıdaki adresi
belirtebilirsiniz.

## Dosyalar

- `app.py`: Fotoğraf yükleme servisini çalıştıran Flask uygulaması.
- `requirements.txt`: Gerekli Python paketleri.
- `uploads/`: Yüklenen fotoğrafların kaydedildiği klasör.
