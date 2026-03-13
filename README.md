## YolHaritam

### Proje Özeti
YolHaritam, üniversite öğrencileri ve kariyerine yön vermek isteyen bireyler için tasarlanmış, **Türkçe bir yapay zeka destekli öğrenme yol haritası uygulamasıdır**.  
Uygulama, kullanıcının mevcut beceri seviyelerini ve hedef rolünü alarak, önkoşul ilişkilerini de dikkate eden **4 haftalık, sade ve uygulanabilir bir öğrenme planı** üretir.

### Çözmeye Çalıştığı Problem
- Hedef role gitmek için hangi becerilerin eksik olduğunu bilmemek  
- Eksik becerileri **hangi sırayla** çalışması gerektiğini kestirememek  
- Haftalık çalışma süresine göre **gerçekçi** bir plan çıkaramamak  
- Planın arkasındaki mantığı ve **“Bu sıra neden böyle?”** sorusunun cevabını görememek  

YolHaritam AI, bu soruları cevaplayan küçük ama anlamlı bir karar destek aracı sunar.

### Hedef Kullanıcı Kitlesi
- Veri bilimi, yapay zeka, frontend gibi alanlara yönelmek isteyen **üniversite öğrencileri**  
- Bootcamp / patika / online kurs programlarına hazırlanan katılımcılar  
- Kariyer geçişi yapmak isteyen junior geliştiriciler  
- Kendi kendine öğrenen, **yapılandırılmış bir öğrenme planı** arayan herkes

### Temel Değer Önerisi
- Hedef role göre **kişiselleştirilmiş** beceri boşluğu analizi  
- Önkoşulları gözeten **anlaşılır ve açıklanabilir** bir algoritma  
- Haftalık saat kısıtına uygun, **4 haftalık odaklı bir plan**  
- Tamamen yerel çalışabilen, **API anahtarı gerektirmeyen** bir MVP

### Özellikler
- Hedef rol seçimi (AI Engineer, Data Analyst, Frontend Developer)  
- Rol bazlı beceri gereksinimleri (1–5 seviye, rol ağırlığı ile birlikte)  
- Kullanıcının mevcut beceri seviyelerini (0–5) hızlıca girebilmesi  
- Beceri boşluğu analizi:
  - Mevcut seviye – hedef seviye farkı
  - Rol ağırlığı
  - Öncelik skoru
  - Eksik önkoşul uyarıları  
- 4 haftalık öğrenme yol haritası:
  - Haftada en fazla 2 odak beceri
  - Tahmini çalışma süresi
  - Her beceri için 2–4 mini görev
  - Türkçe, sade açıklamalar  
- Opsiyonel OpenAI entegrasyonu ile geliştirilmiş açıklama modu (varsa)

### Kullanılan Teknolojiler
- **Python 3.11+**  
- **Streamlit** – tek sayfalı, hızlı MVP arayüzü  
- **pandas** – tablo ve veri gösterimi  
- **Plotly** – etkileşimli grafik (beceri seviyeleri görselleştirme)  
- **networkx** – beceri önkoşul grafı ve sıralama mantığı  
- **python-dotenv** – `.env` yönetimi  
- **openai (opsiyonel)** – geliştirilmiş açıklama metinleri için

### Kullanılan AI Araçları
- Çekirdek planlama mantığı **kural tabanlı ve açıklanabilir** şekilde tasarlanmıştır; herhangi bir model eğitimi yapılmamaktadır.  
- İsteğe bağlı olarak, eğer `.env` dosyasında `OPENAI_API_KEY` tanımlıysa:
  - OpenAI Chat Completion API üzerinden, algoritma çıktısını özetleyen ek bir Türkçe açıklama üretilebilir.
  - API hatası veya anahtar yokluğu durumunda sistem otomatik olarak **deterministik moda geri döner**.

### Algoritma Mantığı
1. **Rol gereksinimlerinin yüklenmesi**  
   - Her rol için: gerekli beceriler, hedef seviye (1–5) ve rol ağırlığı tanımlıdır.  
2. **Kullanıcı profili**  
   - Kullanıcı aynı beceri seti için kendi seviyesini 0–5 arası girer.  
3. **Boşluk hesabı**  
   - `gap = required_level - current_level`  
   - Sadece `gap > 0` olan beceriler dikkate alınır.  
4. **Öncelik skoru**  
   \[
   \text{priority\_score} = (\text{gap} \times \text{role\_weight}) + \text{unlock\_bonus} + \text{quick\_win\_bonus}
   \]
   - `role_weight`: Rol için önem katsayısı  
   - `unlock_bonus`: Pek çok becerinin önkoşulu olan becerilere ek puan  
   - `quick_win_bonus`: Öğrenmesi görece kolay, motivasyon arttırıcı becerilere küçük ek puan  
5. **Bağımlılık grafı ve sıralama**  
   - `networkx.DiGraph` ile beceriler arası “önkoşul -> beceri” kenarları kurulup,  
   - Topolojik sıralama benzeri bir yöntemle, hem bağımlılıklar hem de öncelik skoru gözetilerek liste elde edilir.  
6. **Haftalık planlama**  
   - Haftalık çalışma saati ve beceri zorluğu kullanılarak tahmini süre hesaplanır.  
   - Haftada **en fazla 2 odak beceri** olacak şekilde, zorluk ve saat yükü dengelenir.  

### Uygulama Ekranları
- **Hedef ve Profil**  
  - Rol seçimi, haftalık çalışma saati, süre (varsayılan 4 hafta)  
  - İlgili beceriler için seviye slider’ları  
  - “Yol Haritasını Oluştur” butonu  
- **Beceri Boşluğu Analizi**  
  - Eksik beceriler tablosu  
  - Mevcut – Hedef seviye grafiği (Plotly)  
  - Öncelik skorları ve eksik önkoşul uyarıları  
  - Özet metrik kartları  
- **Öğrenme Yol Haritası**  
  - Haftalık plan (1–4. hafta)  
  - Her hafta için odak beceriler, tahmini saat, mini görevler  
  - “Bu Sıra Neden Önerildi?” ve “4 Hafta Sonunda Beklenen Kazanımlar” açıklamaları

### Kurulum ve Çalıştırma
1. Depoyu klonlayın veya projeyi bir klasöre indirin.  
2. Sanal ortam oluşturmanız tavsiye edilir:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. (İsteğe bağlı) `.env` dosyasını oluşturun:
   ```bash
   copy .env.example .env  # Windows için
   ```
   Ardından `.env` içine kendi `OPENAI_API_KEY` değerinizi ekleyebilirsiniz; eklemezseniz uygulama **deterministik modda** sorunsuz çalışır.
5. Uygulamayı başlatın:
   ```bash
   streamlit run app.py
   ```

### Projede AI Nasıl Kullanıldı?
- Planlama algoritması tamamen **kural tabanlı ve şeffaf** olacak şekilde Python ile yazıldı.  
- Önkoşul ilişkileri ve rol ağırlıkları, açıklanabilir bir veri modeli üzerinden yönetiliyor (`data/skills.json`, `data/roles.json`).  
- Opsiyonel OpenAI entegrasyonu sayesinde:
  - Aynı algoritma çıktısı, daha anlatımsal bir Türkçe ile açıklanabiliyor.
  - Bu katman başarısız olsa bile çekirdek fonksiyonellik bozulmuyor.

### Prompt Kütüphanesi
Projede kullanılan önemli prompt örnekleri ve varyasyonları `prompt-logbook.md` ve `docs/ui_promptlari.md` dosyalarında belgelendi:
- Proje fikri ve problem tanımı promptları  
- Algoritma tasarımı ve veri modeli promptları  
- UI tasarımına ilham veren ekran promptları  
- İyileştirme ve refaktör önerileri için kullanılan promptlar  

### Gelecek Vizyonu
- Daha fazla hedef rol eklenmesi (Backend Developer, MLOps Engineer vb.)  
- Kullanıcının geçmiş planlarını saklayan basit bir ilerleme günlüğü (isteğe bağlı veri katmanı ile)  
- Haftalık görevlerin gerçek kurs/video/link önerileriyle zenginleştirilmesi  
- Beceri seviyesini otomatik ölçen mini quiz veya proje değerlendirmeleri  
- Topluluk tabanlı “örnek yol haritaları” paylaşım alanı

### Proje Klasör Yapısı
```text
YolHaritam-AI/
  app.py
  requirements.txt
  .env.example
  .gitignore
  README.md
  prompt-logbook.md
  data/
    roles.json
    skills.json
  src/
    __init__.py
    algorithm.py
    planner.py
    explainer.py
    data_loader.py
    ui_helpers.py
  docs/
    vize_paketi.md
    ui_promptlari.md
  assets/
    placeholder.txt
```



