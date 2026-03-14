# YolHaritam 🗺️

**Rotanı keşfet, yolculuğunu planla.**

YolHaritam, kullanıcıların kariyer ve öğrenme yolculuklarını planlamalarına yardımcı olan, yapay zeka destekli web tabanlı bir uygulamadır.

---

## Proje Hakkında

YolHaritam, üniversite öğrencileri ve kariyerine yön vermek isteyen bireyler için tasarlanmış **Türkçe bir öğrenme yol haritası uygulamasıdır**. Uygulama, kullanıcının mevcut beceri seviyelerini ve hedef rolünü alarak, önkoşul ilişkilerini de dikkate alan **4 haftalık, sade ve uygulanabilir bir öğrenme planı** üretir. Kullanıcı girişi, demo hesap, beceri boşluğu analizi ve haftalık yol haritası ile kariyer planlamayı kolaylaştırır.

---

## Teknolojiler

- **Python 3.11+**
- **Streamlit** – web arayüzü (tek sayfa uygulaması)
- **HTML, CSS** – özelleştirilmiş login ve dashboard arayüzü (Syne, DM Sans fontları; koyu tema)
- **pandas** – veri işleme ve tablo gösterimi
- **Plotly** – etkileşimli grafikler (beceri seviyeleri)
- **networkx** – beceri önkoşul grafı ve sıralama algoritması
- **python-dotenv** – ortam değişkenleri (.env)
- **openai (opsiyonel)** – geliştirilmiş Türkçe açıklama metinleri
- **JSON** – rol ve beceri verileri (data/roles.json, data/skills.json)

---

## Özellikler

- **Kullanıcı girişi** – E-posta ile giriş; Google, GitHub, Apple ile giriş butonları (UI)
- **Demo hesap** – Hızlı deneme için demo@YolHaritam.com / 123456
- **Şifre sıfırlama** – “Forgot password?” bağlantısı
- **Hedef rol seçimi** – AI Engineer, Data Analyst, Frontend Developer
- **Beceri boşluğu analizi** – Eksik beceriler, öncelik skorları, önkoşul uyarıları
- **Öğrenme yolculuğu modülü** – 4 haftalık haftalık plan, mini görevler, tahmini süreler
- **Modern ve responsive tasarım** – Koyu tema, cyan/teal renk paleti, animasyonlar, mobil uyumlu

---

## Son Güncellemeler

- Login sayfası tasarımı güncellendi (grid arka plan, glow orblar, Syne/DM Sans fontları)
- Logo boyutu ve görünümü optimize edildi (myway-icon.png, 200px genişlik)
- Cyan glow efektleri eklendi (drop-shadow)
- Logo–başlık arası boşluk ve container padding iyileştirildi
- UI/UX iyileştirmeleri yapıldı (kart, form alanları, sosyal giriş butonları)

---

## Kurulum

1. **Repoyu klonlayın**
   ```bash
   git clone <repo-url>
   cd YolHaritam-AI
   ```

2. **Sanal ortam (önerilir) ve bağımlılıkları yükleyin**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Uygulamayı başlatın**
   ```bash
   streamlit run app.py
   ```

Tarayıcıda açılan adresten (genelde http://localhost:8501) uygulamaya erişebilirsiniz. Demo giriş: **demo@YolHaritam.com** / **123456**.

*(İsteğe bağlı)* Gelişmiş açıklamalar için `.env` dosyasına `OPENAI_API_KEY` ekleyebilirsiniz; yoksa uygulama deterministik modda çalışır.

---

## Ekran Görüntüleri

*(Login sayfası ve dashboard ekran görüntüleri buraya eklenebilir.)*

---

## Geliştirici

- **Ad Soyad:** [İsminizi yazın]
- **Üniversite:** [Üniversitenizi yazın]

---

# Detaylı Proje Bilgisi

### Çözmeye Çalıştığı Problem

- Hedef role gitmek için hangi becerilerin eksik olduğunu bilmemek
- Eksik becerileri **hangi sırayla** çalışması gerektiğini kestirememek
- Haftalık çalışma süresine göre **gerçekçi** bir plan çıkaramamak
- Planın arkasındaki mantığı ve **“Bu sıra neden böyle?”** sorusunun cevabını görememek

YolHaritam, bu soruları cevaplayan bir karar destek aracı sunar.

### Hedef Kullanıcı Kitlesi

- Veri bilimi, yapay zeka, frontend gibi alanlara yönelmek isteyen **üniversite öğrencileri**
- Bootcamp / online kurs programlarına hazırlanan katılımcılar
- Kariyer geçişi yapmak isteyen junior geliştiriciler
- Yapılandırılmış bir öğrenme planı arayan herkes

### Algoritma Mantığı

1. **Rol gereksinimleri** – Her rol için gerekli beceriler, hedef seviye (1–5) ve rol ağırlığı tanımlıdır.
2. **Kullanıcı profili** – Kullanıcı aynı beceri seti için kendi seviyesini 0–5 arası girer.
3. **Boşluk hesabı** – `gap = required_level - current_level`; sadece `gap > 0` olan beceriler dikkate alınır.
4. **Öncelik skoru** – Rol ağırlığı, önkoşul bonusu ve hızlı kazanım bonusu ile hesaplanır.
5. **Bağımlılık grafı** – `networkx.DiGraph` ile önkoşul ilişkileri kurulur; topolojik sıralama ile liste elde edilir.
6. **Haftalık planlama** – Haftalık çalışma saati ve beceri zorluğu ile tahmini süre; haftada en fazla 2 odak beceri.

### Uygulama Ekranları

- **Login** – Logo, e-posta/şifre, demo bilgisi, sosyal giriş butonları
- **Hedef ve Profil** – Rol seçimi, haftalık saat, beceri slider’ları, “Yol Haritasını Oluştur”
- **Beceri Boşluğu Analizi** – Eksik beceriler tablosu, Plotly grafiği, öncelik skorları
- **Öğrenme Yol Haritası** – Haftalık plan (1–4. hafta), mini görevler, açıklamalar

### Proje Klasör Yapısı

```text
YolHaritam-AI/
  app.py
  requirements.txt
  .env.example
  README.md
  data/
    roles.json
    skills.json
    modules.json
  src/
    algorithm.py
    planner.py
    explainer.py
    data_loader.py
    design_system.py
    ui_helpers.py
    auth_manager.py
    state_manager.py
    navigation_manager.py
  docs/
    ui_promptlari.md
  assets/
    images/
      myway-icon.png
```

Bu yapı, üniversite projesi için sunulabilir, anlaşılır ve genişletilebilir bir MVP niteliğindedir.
