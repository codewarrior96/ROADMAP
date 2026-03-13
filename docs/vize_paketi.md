## YolHaritam – Vize Sunum Paketi

### 1. Problem Tanımı
Günümüzde öğrenciler ve kariyer değiştirmek isteyen bireyler için en büyük sorunlardan biri, **hangi becerileri hangi sırayla öğrenmeleri gerektiğini bilememeleri**dir.  
Online kaynak bol olsa da:
- Beceriler arasındaki **önkoşul ilişkileri** genellikle görünmezdir.
- Hedef role (örneğin Data Analyst veya Frontend Developer) göre neye odaklanılması gerektiği belirsizdir.
- Kişinin haftalık zamanına göre gerçekçi bir **öğrenme planı** çıkarmak zordur.

YolHaritam, bu problemi küçük ama etkili bir MVP ile adresleyen bir araçtır.

---

### 2. Hedef Kullanıcı Profili
- Lisans / yüksek lisans öğrencileri  
- Veri, yapay zeka, frontend gibi alanlara yönelmek isteyen junior geliştiriciler  
- Bootcamp ve online programlara hazırlanan katılımcılar  
- Kendi kendine öğrenen, ama “nereden başlamalıyım?” sorusuna cevap arayan bireyler  

Bu kullanıcıların ortak ihtiyacı: **net, uygulanabilir ve kısa vadede sonuç üreten** bir öğrenme planı.

---

### 3. User Journey
1. Kullanıcı uygulamayı açar ve kendini kısaca tanımlar:  
   - Hedef rolünü seçer (AI Engineer, Data Analyst, Frontend Developer).  
   - Haftalık ayırabileceği çalışma saatini girer.  
2. Seçilen role göre önemli görülen beceriler ekrana gelir; kullanıcı 0–5 arası mevcut seviyesini slider ile işaretler.  
3. “Yol Haritasını Oluştur” butonuna bastığında sistem:  
   - Beceri boşluklarını hesaplar,  
   - Önkoşul ilişkilerine göre bir beceri sırası üretir,  
   - 4 haftalık planı oluşturur (haftada en fazla 2 odak beceri).  
4. Kullanıcı “Beceri Boşluğu Analizi” sayfasında tablo ve grafiklerle durumunu görür.  
5. “Öğrenme Yol Haritası” sayfasında ise haftalık görevleri ve açıklamaları inceler.

---

### 4. MVP Özellikleri
- Türkçe arayüz, Streamlit tabanlı tek sayfalı uygulama  
- Üç temel hedef rol: AI Engineer, Data Analyst, Frontend Developer  
- JSON tabanlı beceri ve rol veri modeli (kolay genişletilebilir)  
- Kural tabanlı, açıklanabilir beceri boşluğu ve öncelik analizi  
- 4 haftalık, haftada en fazla 2 odak beceri içeren öğrenme planı  
- Opsiyonel OpenAI desteği ile gelişmiş açıklama (anahtar yoksa deterministik mod)

---

### 5. Kullanıcı Akış Özeti
1. **Giriş ve Profil Belirleme**  
   - Rol seçimi  
   - Haftalık çalışma saati  
   - Plan süresi (varsayılan 4 hafta)  
   - Beceri seviyelerinin girilmesi  
2. **Analiz Ekranı**  
   - Eksik beceriler tablosu  
   - Mevcut vs hedef beceri seviyeleri grafiği  
   - Önkoşul uyarıları ve özet metrikler  
3. **Yol Haritası Ekranı**  
   - Hafta bazlı görevler ve açıklamalar  
   - “Bu sıra neden önerildi?” açıklaması  
   - “4 hafta sonunda beklenen kazanımlar” özeti  

---

### 6. 3 Temel Ekran Açıklaması

#### 6.1 Hedef ve Profil Ekranı
- Projenin giriş noktasıdır.  
- Kullanıcıdan çok fazla bilgi istemeden, sadece gerçekten gerekli parametreler alınır:
  - Rol
  - Haftalık saat
  - Plan süresi
  - Rolle ilişkili beceri seviyeleri  
- Böylece hem **form yorgunluğu azaltılır**, hem de ilk adımdan itibaren hedef odaklı bir deneyim sunulur.

#### 6.2 Beceri Boşluğu Analizi Ekranı
- Algoritmanın ürettiği boşluk ve öncelik skorları görselleştirilir.  
- Kullanıcı:
  - Hangi becerilerde daha çok boşluğu olduğunu,
  - Bu boşluğun hangi seviyeden kaynaklandığını,
  - Hangi becerilerin önkoşul içerdiğini,
  - Kısa özet metrikleri (toplam eksik beceri, ortalama boşluk, yüksek öncelikli başlıklar)
  tek ekranda görebilir.  

#### 6.3 Yol Haritası Ekranı
- Haftalara bölünmüş, uygulanabilir bir plan sunar:  
  - Her hafta için 1–2 odak beceri  
  - Tahmini saat  
  - Mini görevler (küçük uygulamalar, not çıkarma, analiz denemeleri vb.)  
- Ayrıca iki önemli açıklama alanı içerir:
  - “Bu Sıra Neden Önerildi?” → Kullanıcının plana güven duymasını sağlar.  
  - “4 Hafta Sonunda Beklenen Kazanımlar” → Motivasyonu destekler.  

---

### 7. Tasarım Kararları
- **Streamlit Kullanımı:**  
  - Hızlı prototipleme, kolay kurulum ve basit dağıtım imkânı sağladığı için tercih edildi.  
  - UI karmaşıklığını azaltarak algoritma ve veri modeline odaklanmamıza izin verdi.  

- **JSON Veri Modeli:**  
  - Her beceri ve rol, `data/skills.json` ve `data/roles.json` dosyalarında tutulur.  
  - Önkoşul ve ağırlık değişiklikleri, kod değiştirmeden yapılabilir.  

- **Kural Tabanlı Algoritma:**  
  - Ders kapsamında **açıklanabilirlik** önemli olduğu için, herhangi bir “kara kutu” model yerine basit ve anlaşılır formüller kullanıldı.  

- **4 Haftalık Sınırlı Plan:**  
  - Hem vize/final projesi sunumuna uygun, hem de öğrencinin gözünde “denenebilir” bir zaman aralığı sunar.  

---

### 8. Kullanılacak AI Araçları
- **Deterministik Katman:**  
  - Tüm planlama ve sıralama mantığı Python içinde, kural tabanlıdır.  
  - Bu katman, her zaman ve her ortamda (API anahtarı olmadan) çalışır.  

- **Opsiyonel OpenAI Katmanı:**  
  - Eğer `.env` içinde `OPENAI_API_KEY` varsa, plan ve boşluk analizi özetlenerek daha zengin Türkçe açıklama üretilir.  
  - Hata durumunda sistem otomatik olarak deterministik moda döner.  

---

### 9. Geliştirme İş Akışı
1. Klasör yapısı ve veri modellerinin (JSON) tanımlanması  
2. Veri yükleyici modüllerin (`data_loader.py`) yazılması  
3. Çekirdek algoritma (`algorithm.py`) ve haftalık planlayıcı (`planner.py`) geliştirilmesi  
4. Açıklama katmanı (`explainer.py`) ve UI yardımcı fonksiyonlarının (`ui_helpers.py`) eklenmesi  
5. Streamlit ana uygulamasının (`app.py`) yazılması ve sayfaların bağlanması  
6. Dokümantasyon (`README.md`, `vize_paketi.md`, `ui_promptlari.md`, `prompt-logbook.md`) ile ders teslimine hazır hale getirilmesi  

---

### 10. Bu Proje Neden Özgün?
- Tamamen **Türkçe kullanıcı deneyimi** ve eğitim odaklı bir senaryoya göre tasarlanmıştır.  
- Rol bazlı beceri, seviye ve önkoşul modellemesi, küçük bir JSON veri setiyle açıklanabilir hale getirilmiştir.  
- Hem **deterministik** hem de **opsiyonel LLM destekli** açıklama katmanına sahip olması, projeyi ders kapsamında tartışmaya elverişli kılar:
  - “AI olmadan ne yapabiliyoruz?”  
  - “AI ekleyince ne değişiyor?”  
- Kapsamı kontrollü tutulmuş, ancak genişletmeye açık bir mimariyle tasarlanmıştır:
  - Yeni rol/beceri eklemek için yalnızca JSON’u güncellemek yeterlidir.  
  - UI ve algoritma modüler biçimde ayrı dosyalardadır.  

Bu özellikler sayesinde YolHaritam, hem **vize** hem de **final** sunumu için örnek gösterilebilecek, küçük ama düşünülmüş bir eğitim teknolojisi projesi niteliği taşır.

