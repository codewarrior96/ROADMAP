# YolHaritam 🗺️

**Rotanı keşfet, yolculuğunu planla.**

YolHaritam, kullanıcıların kariyer ve öğrenme yolculuklarını planlamalarına yardımcı olan, yapay zeka destekli web tabanlı bir uygulamadır. Kullanıcının mevcut beceri seviyelerini ve hedef rolünü analiz ederek önkoşul ilişkilerini dikkate alan, sade ve uygulanabilir bir öğrenme yol haritası oluşturur.

---

# Proje Hakkında

YolHaritam; üniversite öğrencileri, kariyerine yön vermek isteyen bireyler ve yapılandırılmış bir öğrenme planı arayan kullanıcılar için geliştirilmiş Türkçe bir öğrenme yol haritası uygulamasıdır.

Uygulama, kullanıcının:

- mevcut beceri seviyelerini
- hedef rolünü
- haftalık çalışma süresini

alarak beceri boşluklarını analiz eder ve buna uygun haftalık bir öğrenme planı üretir.

---

# Özellikler

### Kullanıcı Girişi
- E-posta ile giriş
- Google, GitHub ve Apple ile giriş butonları (UI)
- Modern login arayüzü

### Demo Hesap
E-posta: demo@YolHaritam.com
Şifre: 123456


### Hedef Rol Seçimi
- AI Engineer
- Data Analyst
- Frontend Developer

### Beceri Boşluğu Analizi
- Eksik becerilerin belirlenmesi
- Öncelik skorlarının hesaplanması
- Önkoşul ilişkilerinin analizi

### Öğrenme Yol Haritası
- Haftalık plan
- Mini görevler
- Tahmini süreler
- Mantıklı öğrenme sıralaması

### Modern Arayüz
- Koyu tema
- Responsive tasarım
- Özelleştirilmiş login ve dashboard

---

# Teknolojiler

- Python 3.11+
- Streamlit — web arayüzü
- HTML / CSS — özel tasarım login ve dashboard
- Pandas — veri işleme
- Plotly — etkileşimli grafikler
- NetworkX — beceri bağımlılık grafı
- python-dotenv — ortam değişkenleri
- OpenAI API (opsiyonel)
- JSON veri yapıları

---

# Çözmeye Çalıştığı Problem

Birçok kullanıcı:

- Hedef role ulaşmak için hangi becerilerin eksik olduğunu bilmiyor
- Eksik becerileri hangi sırayla çalışması gerektiğini kestiremiyor
- Haftalık çalışma süresine göre gerçekçi bir plan çıkaramıyor
- Öğrenme planının mantığını anlayamıyor

YolHaritam bu problemleri çözmek için bir **kariyer ve öğrenme planlama aracı** sunar.

---

# Hedef Kullanıcı Kitlesi

- Yapay zeka ve veri bilimi alanına yönelmek isteyen öğrenciler
- Bootcamp veya online kurs katılımcıları
- Kariyer geçişi yapmak isteyen geliştiriciler
- Yapılandırılmış bir öğrenme planı arayan herkes

---

# Algoritma Mantığı

YolHaritam aşağıdaki adımlarla çalışır:

### 1. Rol Gereksinimleri
Her rol için gerekli beceriler ve hedef seviyeler tanımlıdır.

### 2. Kullanıcı Profili
Kullanıcı kendi beceri seviyelerini 0-5 arasında girer.

### 3. Beceri Boşluğu Hesabı
gap = required_level - current_level


Sadece **gap > 0** olan beceriler analiz edilir.

### 4. Öncelik Skoru
Rol ağırlığı, önkoşullar ve hızlı kazanım faktörleri değerlendirilir.

### 5. Bağımlılık Grafı
NetworkX kullanılarak beceriler arası önkoşul ilişkileri modellenir.

### 6. Haftalık Planlama
Haftalık çalışma süresine göre uygulanabilir bir öğrenme planı oluşturulur.

---

# Uygulama Akışı

### Login
- E-posta / şifre giriş
- Demo hesap
- Sosyal giriş butonları

### Hedef ve Profil
- Hedef rol seçimi
- Haftalık çalışma süresi
- Beceri seviyeleri

### Beceri Boşluğu Analizi
- Eksik beceriler tablosu
- Grafikler
- Öncelik skorları

### Öğrenme Yol Haritası
- Haftalık plan
- Mini görevler
- Öğrenme sıralaması

---

# Kurulum

### Repoyu klonlayın

git clone https://github.com/codewarrior96/ROADMAP.git

cd YolHaritam-AI


### Sanal ortam oluşturun

Windows:

python -m venv venv
venv\Scripts\activate

### Bağımlılıkları yükleyin

pip install -r requirements.txt

shell
Kodu kopyala

### Uygulamayı çalıştırın

streamlit run app.py

css
Kodu kopyala

Tarayıcıda açılan adres:

http://localhost:8501

yaml
Kodu kopyala

---

# Demo Giriş

E-posta: demo@YolHaritam.com
Şifre: 123456

yaml
Kodu kopyala

---

# Proje Klasör Yapısı

YolHaritam-AI/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── roles.json
│ ├── skills.json
│ └── modules.json
│
├── src/
│ ├── algorithm.py
│ ├── planner.py
│ ├── explainer.py
│ ├── data_loader.py
│ ├── design_system.py
│ ├── ui_helpers.py
│ ├── auth_manager.py
│ ├── state_manager.py
│ └── navigation_manager.py
│
├── docs/
│ └── ui_promptlari.md
│
└── assets/
└── images/
└── myway-icon.png

yaml
Kodu kopyala

---

# Son Güncellemeler

- Login sayfası yeniden tasarlandı
- Logo görünümü optimize edildi
- Cyan glow efektleri eklendi
- UI/UX iyileştirmeleri yapıldı
- Beceri boşluğu analizi geliştirildi

---

# Ekran Görüntüleri

Login ekranı, dashboard ve analiz sayfalarının görüntüleri buraya eklenebilir.

Örnek:

---

# Geliştirici

**Salim**

Yapay zeka, veri bilimi ve yazılım geliştirme alanlarında kendini geliştirmeye odaklanan bir geliştirici.

---

# Not

YolHaritam küçük ama genişletilebilir bir MVP olarak tasarlanmıştır. Amaç kullanıcıya yalnızca bir liste sunmak değil, **anlaşılabilir, mantıklı ve uygulanabilir bir öğrenme rotası** oluşturmaktır.


