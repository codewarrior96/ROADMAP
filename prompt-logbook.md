## YolHaritam – Prompt Günlüğü

Bu dosya, proje boyunca kullanılan önemli promptları ve bunların proje üzerindeki etkilerini özetler. Amaç, ders kapsamında hem **süreç şeffaflığını** hem de **AI ile çalışma pratiğini** belgelemektir.

---

### 1. Proje Fikri Promptu

**Amaç:** Genel proje fikrini, kapsamı ve kısıtları netleştirmek.  

**Özet Prompt:**
- Eğitim teknolojisi ve yapay zekâyı birleştiren, Türkçe bir web uygulaması  
- Kullanıcının mevcut becerilerini, hedef rol gereksinimleri ile karşılaştır  
- Beceri boşluklarını ve önkoşul ilişkilerini dikkate alan 4 haftalık bir yol haritası üret  
- Streamlit tabanlı, küçük ama ders sunumuna uygun bir MVP olsun  

**Ne İşe Yaradı?**
- Projenin tek cümlelik kimliği netleşti: “Hedef role giden 4 haftalık beceri yol haritası”  
- Fazla iddialı (örn. tam teşekküllü LMS, kullanıcı hesapları, ödeme vb.) fikirler erkenden elendi.  

**Sonradan Ne Değişti?**
- Başta 6–8 haftalık plan düşünülmüştü, ders kapsamı ve sadelik için 4 haftaya indirildi.  

---

### 2. Algoritma Tasarımı Promptu

**Amaç:** Beceri boşluğu analizi ve önceliklendirme için açıklanabilir bir kural seti oluşturmak.  

**Özet Prompt:**
- Kullanıcı seviyeleri (0–5) ve hedef rol gereksinimleri (1–5) üzerinden `gap = required - current` hesabı yap  
- Sadece `gap > 0` olan becerileri dikkate al  
- Rol ağırlığı, önkoşul sayısı ve “quick win” bilgilerini kullanarak bir öncelik skoru üret  
- networkx ile önkoşul grafı kur ve sıralamada bağımlılıkları gözet  

**Ne İşe Yaradı?**
- Tamamen **kural tabanlı** ve şeffaf bir algoritma ile hızlı şekilde çalışır bir çekirdek oluşturuldu.  
- Önkoşul ilişkileri veri modelinde (JSON) tutulduğu için yeni beceri/rol eklemek kolaylaştı.  

**Sonradan Ne Değişti?**
- `overload_penalty` başlangıçta skora doğrudan ekleniyordu; daha sonra sadece haftalık planlayıcıda yük dengeleme için kullanılmasına karar verildi (kodda sadeleştirildi).  

---

### 3. UI Promptları

**Amaç:** Üç temel ekran için sade, Türkçe ve Streamlit’e uygun bir düzen tasarlamak.  

**Özet Prompt:**
- 3 sayfa: “Hedef ve Profil”, “Beceri Boşluğu Analizi”, “Öğrenme Yol Haritası”  
- Her sayfanın zorunlu bileşenleri, metinleri ve kullanıcı akışı net tanımlı olsun  
- Fazla widget kullanmadan, geniş boşluklar ve okunaklı başlıklar tercih et  

**Ne İşe Yaradı?**
- Sayfa sayısı ve içerikleri netleşti; tek bir dosya (`app.py`) içinde sade bir gezinme yapısı kuruldu.  
- Kullanıcı, ilk sayfada planı üretip ikinci ve üçüncü sayfalarda sonucu inceleyebiliyor.  

**Sonradan Ne Değişti?**
- Başlangıçta beceri slider’larının tüm beceriler için gösterilmesi düşünülüyordu; UX sadeleştirmek için sadece seçilen role ait beceriler gösterildi.  

---

### 4. Kod Üretim Promptu

**Amaç:** Projeyi adım adım ama tek seferde teslim edilebilir hale getiren kod iskeletini oluşturmak.  

**Özet Prompt:**
- Belirli bir klasör yapısı içinde (`src`, `data`, `docs`, vb.) tüm dosyaları doldur  
- Sadece açıklama değil, **gerçek çalışan kod** üret  
- Tüm kullanıcıya bakan metinleri Türkçe yaz, algoritma ve değişken isimlerini İngilizce tut  
- Dış API anahtarı olmadan da tamamen çalışabilsin  

**Ne İşe Yaradı?**
- Proje, “yarım kalmış demo” olmaktan çıkıp, `streamlit run app.py` ile açılabilir bir seviyeye geldi.  
- Ayrı modüller (`algorithm.py`, `planner.py`, `explainer.py`) sayesinde kod okunabilirliği arttı.  

**Sonradan Ne Değişti?**
- Bazı modüller başlangıçta tek dosyada düşünülmüştü; sürdürülebilirlik için küçük modüllere ayrıldı.  

---

### 5. İyileştirme Promptları

**Amaç:** Öncelik skoru, haftalık planlama ve açıklama katmanını daha anlamlı hale getirmek.  

**Özet Prompt:**
- Haftada en fazla 2 beceri olsun, zorlu beceriler aynı haftaya yığılmasın  
- Hızlı kazanım sağlayan becerilere küçük bir bonus ver  
- Açıklama katmanında, “Bu sıra neden önerildi?” ve “4 hafta sonunda ne kazanırım?” sorularına net cevap üret  
- LLM yokken de tatmin edici metinler oluştur  

**Ne İşe Yaradı?**
- Haftalık plan çıktısı daha gerçekçi ve öğrencinin gözünden anlaşılır hale geldi.  
- Deterministik açıklama katmanı sayesinde, OpenAI anahtarı olmadan da proje anlamlı çıktı üretiyor.  

**Sonradan Ne Değişti?**
- LLM çıktısı çok uzun olabileceği için, metnin tamamı tek alan yerine kısa özet + notlar şeklinde gösterildi.  

---

### 6. Kısa Notlar: Ne İşe Yaradı, Neyi Değiştirdi?

- **Veri modelini önce tasarlamak**, sonraki tüm kod adımlarını basitleştirdi; `skills.json` ve `roles.json` etrafında düşünmek, “hangi bilgiyi gerçekten kullanıyorum?” sorusunu netleştirdi.  
- **UI’yi 3 sayfa ile sınırlamak**, projenin kapsamını kontrol altında tuttu ve ders değerlendirmesinde odak kaybını engelledi.  
- **Streamlit + Plotly kombinasyonu**, backend karmaşıklığı eklemeden, güzel bir görsel çıktı sunmayı sağladı.  
- **Deterministik açıklama katmanı**, API anahtarı olmayan kullanıcılar için bile projenin “AI yardımlı” hissini korudu.  

Bu günlük, ileride projeyi genişletmek isteyenler için de hem teknik hem de süreç açısından bir referans niteliği taşımaktadır.

