## YolHaritam – UI Promptları

Bu dosya, üç temel ekran için hazırlanmış **görsel tasarım promptlarını** içerir. Amaç, tasarımcıya veya görsel üretim modeline net ve tutarlı bir yönlendirme sunmaktır.

> Not: Bu promptlar yalnızca metindir, proje kapsamında gerçek görsel üretimi yapılmamıştır.

---

### 1. Açılış / Profil Belirleme Ekranı

#### 1.1 İlk Prompt
> “A clean, modern web dashboard screen for a Turkish education app called ‘YolHaritam’. Left side has a vertical sidebar with three simple navigation items. Main area shows a title ‘Hedef ve Profil’, a short paragraph of explanatory text in Turkish, and a card with dropdowns and sliders for selecting a target role, weekly study hours, and skill levels. Use soft, calm colors, lots of white space, rounded cards, and simple icons. No data table yet, just input widgets and explanation text.”

#### 1.2 İyileştirilmiş Prompt
> “Minimalist and modern UI for a Turkish Streamlit-like web app named ‘YolHaritam’. Use a light background with subtle gradients and a vertical sidebar on the left containing three items: ‘Hedef ve Profil’, ‘Beceri Boşluğu Analizi’, ‘Öğrenme Yol Haritası’. In the main content area, place a clear heading ‘Hedef ve Profil’ with a short Turkish description explaining that the user will choose a target role and current skills. Below, show a responsive card layout: on the left, a dropdown for selecting target role (AI Engineer, Data Analyst, Frontend Developer) and numeric inputs for weekly hours and duration; on the right, several horizontal sliders representing skill levels (0–5) with labels. Use rounded cards, soft blue and purple accents, high contrast for text, and readable sans-serif typography (e.g. Inter or Roboto). Keep the layout airy with generous padding and avoid clutter.”

#### 1.3 Tasarım Kararı Notu
- İlk prompt genel yapıyı tarif etse de, **navigasyon etiketleri**, **renk paleti** ve **tipografi** konusunda net değildi.  
- İyileştirilmiş promptta:
  - Türkçe menü isimleri açıkça belirtildi.  
  - Streamlit benzeri sade, bloklu bir düzen istendi.  
  - Sliders ve input kartlarının hangi tarafta konumlanacağı tanımlandı.  

#### 1.4 Renk / Tipografi / Yerleşim Mantığı
- **Renk:** Açık arka plan, yumuşak mavi/mor vurgu renkleri (butonlar ve aktif menü için).  
- **Tipografi:** Sans-serif, okunabilir ve modern (Inter, Roboto vb.). Başlıklar biraz daha kalın, metinler orta kalınlıkta.  
- **Yerleşim:** Sol dikey menü, sağda geniş içerik alanı. İçerik alanı içinde iki sütunlu kart düzeni (rol & saat bilgisi / beceri slider’ları).  

---

### 2. Beceri Boşluğu Analizi Ekranı

#### 2.1 İlk Prompt
> “An analytics dashboard screen showing a skills gap analysis. There is a page title in Turkish, a descriptive text, a table listing skills with current and target levels, and a bar chart comparing them. The design should be clean and minimal, with a light background and a focus on readability. Use subtle card shadows and consistent spacing.”

#### 2.2 İyileştirilmiş Prompt
> “Modern analytics dashboard UI for a skills gap analysis screen in a Turkish app. The top section includes a heading ‘Beceri Boşluğu Analizi’ and a short Turkish sentence explaining that this page compares current vs target skills for a chosen role. Below, place a full-width card containing a scrollable table with columns: ‘Beceri’, ‘Kategori’, ‘Mevcut Seviye’, ‘Hedef Seviye’, ‘Boşluk’, ‘Öncelik Skoru’. Under the table, show a Plotly-style grouped bar chart that compares ‘Mevcut Seviye’ vs ‘Hedef Seviye’ per skill with a legend. On the right or below, show three compact KPI cards with metrics such as total missing skills, average gap, and number of high-priority skills. Use a white background, soft gray table lines, blue/orange chart colors, and small rounded corners. Typography should be clean and data-focused, similar to a modern BI tool.”

#### 2.3 Tasarım Kararı Notu
- İlk tanım genel bir analitik ekran çiziyordu; ancak bu projeye özgü **kolon başlıkları** ve **KPI kartları** net değildi.  
- İyileştirilmiş promptta:
  - Tablo kolonları birebir isimlendirildi.  
  - Grafiğin türü (grouped bar) ve renkleri belirtildi.  
  - Üç metrik kartı ile üst seviye özet sağlanması istendi.  

#### 2.4 Renk / Tipografi / Yerleşim Mantığı
- **Renk:** Açık arka plan, tablo için gri çizgiler, bar grafikte mavi ve turuncu seri renkleri.  
- **Tipografi:** Sayı ve metinlerin kolay okunabildiği, BI araçlarına yakın bir stil. Başlıklarda hafif ağırlık, tablo metninde normal ağırlık.  
- **Yerleşim:** Üstte başlık ve açıklama, altında geniş tablo + grafik, sağda veya altta üç küçük KPI kartı. Ekran kalabalıklaşmaması için bol beyaz boşluk.  

---

### 3. Yol Haritası Ekranı

#### 3.1 İlk Prompt
> “A roadmap view showing a 4-week learning plan. Each week is a card with title, list of focus skills, estimated hours, and bullet points for mini tasks. The style should feel friendly and motivating, with soft colors and iconography for weeks.”

#### 3.2 İyileştirilmiş Prompt
> “Visually engaging roadmap UI for a 4-week learning plan screen in a Turkish app. The page title is ‘Öğrenme Yol Haritası’. Display four stacked or horizontally scrollable cards, one for each week (1. Hafta, 2. Hafta, etc.), each card showing: total estimated study hours, 1–2 focus skills with short descriptions, and 3–4 mini tasks as bullet points in Turkish. Below the weekly cards, add two text sections titled ‘Bu Sıra Neden Önerildi?’ and ‘4 Hafta Sonunda Beklenen Kazanımlar’, styled as explanation boxes. Use a light background with pastel accent colors per week (e.g. week 1 blue, week 2 green, week 3 orange, week 4 purple), rounded card corners, and playful but still professional icons. Typography should be motivational but clean, with clear hierarchy between week titles, skill names, and task bullets.”

#### 3.3 Tasarım Kararı Notu
- İlk prompt yol haritası fikrini veriyordu ancak, bu projeye özel iki önemli metin bloğu (“Bu Sıra Neden Önerildi?” ve “Beklenen Kazanımlar”) atlanmıştı.  
- İyileştirilmiş sürümde:
  - Bu iki metin alanı açıkça belirtildi.  
  - Haftalık kartların Türkçe başlıkları ve içerik yapısı netleştirildi.  
  - Haftalar arasında görsel ayrım için pastel renk paleti önerildi.  

#### 3.4 Renk / Tipografi / Yerleşim Mantığı
- **Renk:** Her hafta için farklı pastel vurgu rengi; arka planda nötr açık ton. Kartların arka planı hafif gölgeli ve yuvarlatılmış.  
- **Tipografi:** Hafta başlıklarında daha büyük ve kalın font; beceri isimlerinde orta büyüklükte; mini görevlerde standart, okunabilir puntolar.  
- **Yerleşim:** Dikeyde veya yatay kaydırmalı dört hafta kartı; alt tarafta iki açıklama kutusu. Aralarda yeterli boşluk bırakılarak, öğrencinin gözüne “yapılabilir” bir plan hissi verilmesi hedeflenir.  

---

Bu prompt seti, tasarımcıya veya görsel üretim aracına verildiğinde, YolHaritam’ın üç temel ekranının **tutarlı bir görsel dil** ile üretilmesini amaçlar. Böylece hem ders sunumlarında hem de olası gelecek geliştirmelerde tek bir tasarım rehberi işlevi görür.

