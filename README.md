# Nakil Takip Sistemi V3

Bu program, E-Okul üzerinden okul nakil kontenjanlarını otomatik olarak takip eden ve değişiklik olduğunda Telegram üzerinden bildirim gönderen bir uygulamadır.

## Özellikler

- Modern ve kullanıcı dostu GUI arayüzü (CustomTkinter)
- Otomatik nakil kontenjan kontrolü
- Telegram üzerinden bildirim sistemi
- Ayarları kaydetme ve yükleme
- Koyu/Açık tema desteği

## Kurulum

1. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

2. `config.py` dosyasını düzenleyin:

- Telegram bot token ve chat ID'nizi girin
- Varsayılan ayarları düzenleyin

3. Programı çalıştırın:

```bash
python main.py
```

## Kullanım

1. Program arayüzünden gerekli bilgileri girin:

   - Okul türü
   - İl
   - İlçe
   - Okul adı
   - Sınıf
   - Kontrol süresi
2. "Başlat" butonuna tıklayın
3. Program otomatik olarak kontrolleri yapmaya başlayacak
4. Kontenjan değişikliği olduğunda Telegram üzerinden bildirim alacaksınız

## Geliştirici

@regularowner

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
