import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import json
from config import SETTINGS, TELEGRAM, SAHIP
import requests
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image
import os

class NakilTakip(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Pencere ayarları
        self.title("Nakil Takip Sistemi")
        self.geometry("800x700")
        
        # Tema modu
        ctk.set_appearance_mode(SETTINGS["tema_modu"])
        ctk.set_default_color_theme("blue")
        
        # Ana frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Başlık
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Nakil Takip Sistemi", 
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Ayarlar frame'i
        self.settings_frame = ctk.CTkFrame(self.main_frame)
        self.settings_frame.pack(padx=10, pady=10, fill="x")
        
        # Okul türü
        self.type_var = ctk.StringVar(value=SETTINGS["Türü"])
        self.type_label = ctk.CTkLabel(self.settings_frame, text="Okul Türü:")
        self.type_label.grid(row=0, column=0, padx=5, pady=5)
        self.type_entry = ctk.CTkEntry(self.settings_frame, textvariable=self.type_var)
        self.type_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # İl
        self.il_var = ctk.StringVar(value=SETTINGS["İL"])
        self.il_label = ctk.CTkLabel(self.settings_frame, text="İl:")
        self.il_label.grid(row=1, column=0, padx=5, pady=5)
        self.il_entry = ctk.CTkEntry(self.settings_frame, textvariable=self.il_var)
        self.il_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # İlçe
        self.ilce_var = ctk.StringVar(value=SETTINGS["İlce"])
        self.ilce_label = ctk.CTkLabel(self.settings_frame, text="İlçe:")
        self.ilce_label.grid(row=2, column=0, padx=5, pady=5)
        self.ilce_entry = ctk.CTkEntry(self.settings_frame, textvariable=self.ilce_var)
        self.ilce_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Okul
        self.okul_var = ctk.StringVar(value=SETTINGS["okul"])
        self.okul_label = ctk.CTkLabel(self.settings_frame, text="Okul:")
        self.okul_label.grid(row=3, column=0, padx=5, pady=5)
        self.okul_entry = ctk.CTkEntry(self.settings_frame, textvariable=self.okul_var)
        self.okul_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Sınıf seçimi (ComboBox olarak değiştirildi)
        self.sinif_var = ctk.StringVar(value=str(SETTINGS["sınıf"]))
        self.sinif_label = ctk.CTkLabel(self.settings_frame, text="Sınıf:")
        self.sinif_label.grid(row=4, column=0, padx=5, pady=5)
        self.sinif_combo = ctk.CTkComboBox(
            self.settings_frame,
            values=["9", "10", "11", "12"],
            variable=self.sinif_var
        )
        self.sinif_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # Kontrol süresi (ComboBox olarak değiştirildi)
        self.sure_var = ctk.StringVar(value=str(SETTINGS["kontrol_süresi"]))
        self.sure_label = ctk.CTkLabel(self.settings_frame, text="Kontrol Süresi:")
        self.sure_label.grid(row=5, column=0, padx=5, pady=5)
        self.sure_combo = ctk.CTkComboBox(
            self.settings_frame,
            values=["300", "600", "1800", "3600", "7200"],
            variable=self.sure_var
        )
        self.sure_combo.grid(row=5, column=1, padx=5, pady=5)
        
        # Arkaplan modu
        self.background_var = ctk.BooleanVar(value=False)
        self.background_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Arkaplanda Çalış",
            variable=self.background_var,
            command=self.toggle_background_mode
        )
        self.background_switch.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        # Chrome arkaplanda çalıştırma seçeneği
        self.chrome_headless_var = ctk.BooleanVar(value=False)
        self.chrome_headless_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Chrome'u Arkaplanda Çalıştır",
            variable=self.chrome_headless_var
        )
        self.chrome_headless_switch.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        
        # Telegram ayarları
        self.telegram_frame = ctk.CTkFrame(self.main_frame)
        self.telegram_frame.pack(padx=10, pady=10, fill="x")
        
        self.telegram_label = ctk.CTkLabel(
            self.telegram_frame, 
            text="Telegram Ayarları",
            font=("Helvetica", 16, "bold")
        )
        self.telegram_label.pack(pady=5)
        
        # Bot token
        self.token_var = ctk.StringVar(value=TELEGRAM["bot_token"])
        self.token_label = ctk.CTkLabel(self.telegram_frame, text="Bot Token:")
        self.token_label.pack()
        self.token_entry = ctk.CTkEntry(self.telegram_frame, textvariable=self.token_var, width=300)
        self.token_entry.pack(pady=5)
        
        # Chat ID
        self.chat_var = ctk.StringVar(value=TELEGRAM["chat_id"])
        self.chat_label = ctk.CTkLabel(self.telegram_frame, text="Chat ID:")
        self.chat_label.pack()
        self.chat_entry = ctk.CTkEntry(self.telegram_frame, textvariable=self.chat_var, width=300)
        self.chat_entry.pack(pady=5)
        
        # Durum mesajı
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Durum: Bekleniyor...",
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=10)
        
        # Buton frame'i
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10, fill="x")
        
        # Buton frame'i için grid yapılandırması
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)
        
        # İlk işlem butonu
        self.first_check_button = ctk.CTkButton(
            self.button_frame,
            text="İlk Durum Kontrolü",
            command=self.first_check,
            fg_color="#28a745",  # Yeşil renk
            hover_color="#218838",  # Koyu yeşil
            width=150,
            height=40,
            font=("Helvetica", 12, "bold")
        )
        self.first_check_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Sürekli kontrol butonu
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="Sürekli Kontrol",
            command=self.start_checking,
            fg_color="#007bff",  # Mavi renk
            hover_color="#0056b3",  # Koyu mavi
            width=150,
            height=40
        )
        self.start_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Durdur butonu
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="Durdur",
            command=self.stop_checking,
            state="disabled",
            fg_color="#dc3545",  # Kırmızı renk
            hover_color="#c82333",  # Koyu kırmızı
            width=150,
            height=40
        )
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Ayarları kaydet butonu
        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Ayarları Kaydet",
            command=self.save_settings,
            fg_color="#17a2b8",  # Turkuaz renk
            hover_color="#138496",  # Koyu turkuaz
            width=150,
            height=40
        )
        self.save_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Kontrol değişkenleri
        self.checking = False
        self.driver = None
        self.tray_icon = None
        
        # Pencere kapatma olayını yakala
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def toggle_background_mode(self):
        """Arkaplan modunu aç/kapat"""
        if self.background_var.get():
            self.withdraw()  # Pencereyi gizle
            self.create_tray_icon()
        else:
            self.deiconify()  # Pencereyi göster
            if self.tray_icon:
                self.tray_icon.stop()
                self.tray_icon = None
                
    def create_tray_icon(self):
        """Sistem tepsisi ikonu oluştur"""
        # İkon için basit bir görüntü oluştur
        image = Image.new('RGB', (64, 64), color='red')
        
        menu = Menu(
            MenuItem('Göster', self.show_window),
            MenuItem('Çıkış', self.quit_app)
        )
        
        self.tray_icon = Icon(
            'nakil_takip',
            image,
            'Nakil Takip',
            menu
        )
        
        self.tray_icon.run()
        
    def show_window(self):
        """Pencereyi göster"""
        self.deiconify()
        self.background_var.set(False)
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
            
    def quit_app(self):
        """Uygulamadan çık"""
        self.stop_checking()
        if self.tray_icon:
            self.tray_icon.stop()
        self.quit()
        
    def on_closing(self):
        """Pencere kapatıldığında"""
        if self.background_var.get():
            self.withdraw()
        else:
            self.quit_app()
            
    def save_settings(self):
        """Ayarları config dosyasına kaydet"""
        try:
            settings = {
                "Türü": self.type_var.get(),
                "İL": self.il_var.get(),
                "İlce": self.ilce_var.get(),
                "okul": self.okul_var.get(),
                "sınıf": int(self.sinif_var.get()),
                "kontrol_süresi": int(self.sure_var.get()),
                "tema_modu": SETTINGS["tema_modu"]
            }
            
            telegram = {
                "bot_token": self.token_var.get(),
                "chat_id": self.chat_var.get()
            }
            
            config_content = f"""# Varsayılan ayarlar
SETTINGS = {json.dumps(settings, indent=4, ensure_ascii=False)}

# Telegram bot ayarları
TELEGRAM = {json.dumps(telegram, indent=4, ensure_ascii=False)}

# Program sahibi
SAHIP = "{SAHIP}"
"""
            
            with open("config.py", "w", encoding="utf-8") as f:
                f.write(config_content)
                
            self.status_label.configure(text="Durum: Ayarlar başarıyla kaydedildi!")
            print("Ayarlar kaydedildi:", config_content)
            
        except Exception as e:
            hata_mesaji = f"Hata: Ayarlar kaydedilemedi - {str(e)}"
            self.status_label.configure(text=hata_mesaji)
            print(hata_mesaji)
        
    def send_telegram_message(self, message):
        """Telegram üzerinden mesaj gönder"""
        token = self.token_var.get()
        chat_id = self.chat_var.get()
        
        if token and chat_id:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                data = {
                    "chat_id": chat_id,
                    "text": message
                }
                requests.post(url, json=data)
                return True
            except Exception as e:
                self.status_label.configure(text=f"Telegram Hatası: {str(e)}")
                return False
        return False
        
    def check_nakil(self):
        """Nakil kontrolü yapan ana fonksiyon"""
        driver = None
        try:
            print("Chrome başlatılıyor...")
            service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            
            # Chrome arkaplanda çalışsın mı kontrolü
            if self.chrome_headless_var.get():
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-notifications")
            
            # Driver'ı başlat
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 30)  # Bekleme süresini 30 saniyeye çıkardık
            
            print("E-Okul sayfası açılıyor...")
            driver.get("https://e-okul.meb.gov.tr/OrtaOgretim/OKL/OOK06006.aspx")
            time.sleep(5)  # Sayfa yüklenme süresini artırdık
            
            # Sayfanın yüklendiğinden emin ol
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.chosen-container")))
                print("Sayfa başarıyla yüklendi")
            except Exception as e:
                print("Sayfa yüklenemedi:", str(e))
                raise Exception("E-Okul sayfası yüklenemedi!")
            
            # Okul türü seçimi
            try:
                print("Okul türü seçimi başlıyor...")
                okul_turu_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.chosen-container a.chosen-single")))
                driver.execute_script("arguments[0].click();", okul_turu_dropdown)
                time.sleep(2)
                
                okul_turu_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.chosen-container.chosen-with-drop .chosen-search input[type='text']")))
                okul_turu_input.clear()
                okul_turu_input.send_keys(self.type_var.get())
                time.sleep(1)
                
                # Seçenek listesini bekle ve seç
                okul_turu_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
                okul_turu_option.click()
                time.sleep(2)
                print("Okul türü seçildi")
                
            except Exception as e:
                print(f"Okul türü seçimi hatası: {str(e)}")
                self.status_label.configure(text=f"Hata: Okul türü seçilemedi! - {str(e)}")
                return
            
            # İl seçimi
            try:
                print("İl seçimi başlıyor...")
                # İl dropdown'ını bekle ve tıkla
                il_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlIl_chosen .chosen-single")))
                print("İl dropdown bulundu")
                
                # Sayfayı il dropdown'a kaydır
                driver.execute_script("arguments[0].scrollIntoView(true);", il_dropdown)
                time.sleep(2)
                
                # Dropdown'ı aç
                driver.execute_script("arguments[0].click();", il_dropdown)
                time.sleep(2)
                print("İl dropdown açıldı")
                
                # İl listesinin yüklenmesini bekle
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIl_chosen .chosen-results")))
                print("İl listesi yüklendi")
                
                # İl arama kutusunu bul
                il_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIl_chosen .chosen-search input")))
                il_input.clear()
                print(f"Aranacak il: {self.il_var.get()}")
                
                # İli yavaşça yaz
                for karakter in self.il_var.get():
                    il_input.send_keys(karakter)
                    time.sleep(0.1)
                time.sleep(2)
                print("İl adı yazıldı")
                
                # Sonuçların yüklenmesini bekle
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIl_chosen .chosen-results li")))
                time.sleep(1)
                
                # İlk eşleşen sonucu seç
                il_options = driver.find_elements(By.CSS_SELECTOR, "#ddlIl_chosen .chosen-results li")
                if len(il_options) > 0:
                    for option in il_options:
                        if option.text.strip().upper() == self.il_var.get().strip().upper():
                            print(f"İl seçeneği bulundu: {option.text}")
                            driver.execute_script("arguments[0].click();", option)
                            break
                    else:
                        raise Exception(f"İl seçeneği bulunamadı: {self.il_var.get()}")
                else:
                    raise Exception("İl seçenekleri yüklenemedi")
                
                time.sleep(2)
                print("İl seçildi")
                
                # İl seçiminin başarılı olduğunu kontrol et
                il_secili = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIl_chosen .chosen-single span")))
                print(f"Seçilen il: {il_secili.text}")
                if il_secili.text.strip().upper() != self.il_var.get().strip().upper():
                    raise Exception(f"İl seçimi doğrulanamadı. Beklenen: {self.il_var.get()}, Seçilen: {il_secili.text}")
                print("İl seçimi başarılı")
                
            except Exception as e:
                print(f"İl seçimi hatası: {str(e)}")
                self.status_label.configure(text=f"Hata: İl seçilemedi! - {str(e)}")
                if driver:
                    try:
                        # Hata durumunda sayfanın ekran görüntüsünü al
                        driver.save_screenshot("il_secimi_hatasi.png")
                        print("Hata ekran görüntüsü kaydedildi: il_secimi_hatasi.png")
                    except:
                        pass
                return
            
            # İlçe seçimi
            try:
                print("İlçe seçimi başlıyor...")
                ilce_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlIlce_chosen")))
                driver.execute_script("arguments[0].scrollIntoView(true);", ilce_dropdown)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", ilce_dropdown)
                time.sleep(2)
                
                ilce_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIlce_chosen .chosen-search input")))
                ilce_input.clear()
                ilce_input.send_keys(self.ilce_var.get())
                time.sleep(2)
                
                ilce_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIlce_chosen .chosen-results li.active-result")))
                ilce_option.click()
                time.sleep(2)
                print("İlçe seçimi başarılı")
                
            except Exception as e:
                print(f"İlçe seçimi hatası: {str(e)}")
                self.status_label.configure(text=f"Hata: İlçe seçilemedi! - {str(e)}")
                return
            
            # Okul seçimi
            try:
                print("Okul seçimi başlıyor...")
                okul_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlOkul_chosen")))
                driver.execute_script("arguments[0].scrollIntoView(true);", okul_dropdown)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", okul_dropdown)
                time.sleep(2)
                
                okul_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlOkul_chosen .chosen-search input")))
                okul_input.clear()
                okul_input.send_keys(self.okul_var.get())
                time.sleep(2)
                
                okul_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlOkul_chosen .chosen-results li.active-result")))
                okul_option.click()
                time.sleep(2)
                print("Okul seçimi başarılı")
                
            except Exception as e:
                print(f"Okul seçimi hatası: {str(e)}")
                self.status_label.configure(text=f"Hata: Okul seçilemedi! - {str(e)}")
                return
            
            # Gönder butonu
            try:
                print("Form gönderiliyor...")
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.SubmitButton")))
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", submit_button)
                time.sleep(3)
                print("Form gönderildi")
                
            except Exception as e:
                print(f"Form gönderme hatası: {str(e)}")
                self.status_label.configure(text=f"Hata: Form gönderilemedi! - {str(e)}")
                return
            
            # Sınıfa göre veri çekimi
            sinif = int(self.sinif_var.get())
            xpath_map = {
                9: './td[3]',
                10: './td[4]',
                11: './td[5]',
                12: './td[6]'
            }
            
            while self.checking:
                try:
                    print("Veri çekimi başlıyor...")
                    # Tablo yüklenmesini bekle
                    table = wait.until(EC.presence_of_element_located((By.ID, "dgListe")))
                    
                    bilgi = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dgListe"]/tbody/tr[1]')))
                    deger = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dgListe"]/tbody/tr[2]')))
                    
                    anabilgi = bilgi.find_element(By.XPATH, xpath_map[sinif]).text
                    anadeger = deger.find_element(By.XPATH, xpath_map[sinif]).text
                    
                    print(f"Çekilen veriler - Bilgi: {anabilgi}, Değer: {anadeger}")
                    
                    durum = f"Durum:\n{anabilgi}\n{anadeger}"
                    self.status_label.configure(text=durum)
                    
                    try:
                        anadeger_sayi = int(anadeger)
                        if anadeger_sayi > 0:
                            mesaj = f"‼️ NAKİL KONTROL UYARISI ‼️\n\n{durum}"
                            self.send_telegram_message(mesaj)
                    except ValueError:
                        print(f"Sayıya çevirme hatası: {anadeger}")
                        self.status_label.configure(text="Hata: Kontenjan değeri sayıya çevrilemedi!")
                    
                    # Kontrol süresi kadar bekle
                    for _ in range(int(self.sure_var.get()) // 10):
                        if not self.checking:
                            break
                        time.sleep(10)
                    
                    if self.checking:
                        print("Sayfa yenileniyor...")
                        driver.refresh()
                        time.sleep(3)
                except Exception as e:
                    print(f"Veri çekimi hatası: {str(e)}")
                    self.status_label.configure(text=f"Kontrol Hatası: {str(e)}")
                    if not self.checking:
                        break
                    time.sleep(10)
                    try:
                        driver.refresh()
                        time.sleep(3)
                    except:
                        break
                    continue
                
        except Exception as e:
            print(f"Genel hata: {str(e)}")
            self.status_label.configure(text=f"Başlatma Hatası: {str(e)}")
            self.stop_checking()
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            
    def start_checking(self):
        """Kontrol işlemini başlat"""
        try:
            # Gerekli alanların dolu olduğunu kontrol et
            if not all([
                self.type_var.get(),
                self.il_var.get(),
                self.ilce_var.get(),
                self.okul_var.get(),
                self.sinif_var.get(),
                self.sure_var.get()
            ]):
                self.status_label.configure(text="Hata: Lütfen tüm alanları doldurun!")
                return
            
            # Önceki thread'in tamamen durduğundan emin ol
            if hasattr(self, 'check_thread') and self.check_thread.is_alive():
                self.checking = False
                self.check_thread.join(timeout=5)
            
            self.checking = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # Yeni thread'de kontrol işlemini başlat
            self.check_thread = threading.Thread(target=self.check_nakil)
            self.check_thread.daemon = True
            self.check_thread.start()
            
        except Exception as e:
            self.status_label.configure(text=f"Başlatma Hatası: {str(e)}")
        
    def stop_checking(self):
        """Kontrol işlemini durdur"""
        try:
            self.checking = False
            time.sleep(1)  # Thread'in durması için bekle
            
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_label.configure(text="Durum: Durduruldu")
        except Exception as e:
            self.status_label.configure(text=f"Durdurma Hatası: {str(e)}")

    def first_check(self):
        """İlk durum kontrolünü yap ve Telegram'a gönder"""
        driver = None
        try:
            # Gerekli alanların dolu olduğunu kontrol et
            if not all([
                self.type_var.get(),
                self.il_var.get(),
                self.ilce_var.get(),
                self.okul_var.get(),
                self.sinif_var.get()
            ]):
                self.status_label.configure(text="Hata: Lütfen tüm alanları doldurun!")
                return

            self.status_label.configure(text="Durum: İlk kontrol yapılıyor...")
            
            # Chrome'u başlat
            service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            
            # Chrome arkaplanda çalışsın mı kontrolü
            if self.chrome_headless_var.get():
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 10)
            
            try:
                driver.get("https://e-okul.meb.gov.tr/OrtaOgretim/OKL/OOK06006.aspx")
                time.sleep(2)
                
                # Okul türü seçimi
                try:
                    okul_turu_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".chosen-single")))
                    okul_turu_dropdown.click()
                    time.sleep(1)
                    
                    okul_turu_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".chosen-search input")))
                    okul_turu_input.send_keys(self.type_var.get())
                    okul_turu_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                except:
                    self.status_label.configure(text="Hata: Okul türü seçilemedi!")
                    return
                
                # İl seçimi
                try:
                    il_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlIl_chosen")))
                    il_dropdown.click()
                    time.sleep(1)
                    
                    il_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIl_chosen .chosen-search input")))
                    il_input.send_keys(self.il_var.get())
                    il_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                except:
                    self.status_label.configure(text="Hata: İl seçilemedi!")
                    return
                
                # İlçe seçimi
                try:
                    ilce_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlIlce_chosen")))
                    ilce_dropdown.click()
                    time.sleep(1)
                    
                    ilce_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlIlce_chosen .chosen-search input")))
                    ilce_input.send_keys(self.ilce_var.get())
                    ilce_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                except:
                    self.status_label.configure(text="Hata: İlçe seçilemedi!")
                    return
                
                # Okul seçimi
                try:
                    okul_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ddlOkul_chosen")))
                    okul_dropdown.click()
                    time.sleep(1)
                    
                    okul_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ddlOkul_chosen .chosen-search input")))
                    okul_input.send_keys(self.okul_var.get())
                    okul_input.send_keys(Keys.ENTER)
                    time.sleep(1)
                except:
                    self.status_label.configure(text="Hata: Okul seçilemedi!")
                    return
                
                # Gönder butonu
                try:
                    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".SubmitButton")))
                    submit_button.click()
                    time.sleep(2)
                except:
                    self.status_label.configure(text="Hata: Form gönderilemedi!")
                    return
                
                # Sınıfa göre veri çekimi
                sinif = int(self.sinif_var.get())
                xpath_map = {
                    9: './td[3]',
                    10: './td[4]',
                    11: './td[5]',
                    12: './td[6]'
                }
                
                try:
                    bilgi = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dgListe"]/tbody/tr[1]')))
                    deger = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dgListe"]/tbody/tr[2]')))
                    
                    anabilgi = bilgi.find_element(By.XPATH, xpath_map[sinif]).text
                    anadeger = deger.find_element(By.XPATH, xpath_map[sinif]).text
                    
                    durum = f"📊 İLK DURUM KONTROLÜ 📊\n\nOkul: {self.okul_var.get()}\nSınıf: {sinif}\n\n{anabilgi}\n{anadeger}"
                    
                    # Telegram'a gönder
                    if self.send_telegram_message(durum):
                        self.status_label.configure(text=f"Durum: İlk kontrol tamamlandı ve Telegram'a gönderildi\n{anabilgi}\n{anadeger}")
                    else:
                        self.status_label.configure(text="Hata: Telegram mesajı gönderilemedi! Lütfen bot token ve chat ID'nizi kontrol edin.")
                except:
                    self.status_label.configure(text="Hata: Veriler alınamadı!")
                    return
                
            finally:
                if driver:
                    driver.quit()
                    
        except Exception as e:
            self.status_label.configure(text=f"İlk Kontrol Hatası: {str(e)}")
            if driver:
                driver.quit()

if __name__ == "__main__":
    app = NakilTakip()
    app.mainloop() 