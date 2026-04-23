# LuminaLane AI: Lane Detection Engine


---

## 🌐 Language / Dil
- [English (#english)]
- [Türkçe (#türkçe)]

---

<a name="english"></a>
## [EN] Technical Overview

This project implements an efficient lane detection pipeline using the **Ultra-Fast-Lane-Detection (UFLD)** architecture combined with a custom stabilization layer.

### ⚙️ How it Works
1.  **Row-based Classification:** Unlike pixel-wise segmentation, the model treats lane detection as a row-selection problem. It predicts the most likely "cell" (column) for each horizontal row anchor. This reduces computational cost significantly.
2.  **Temporal Smoothing:** A custom `LaneSmoothing` engine is used to maintain consistency between frames.
    - **EMA Filter:** Smooths noise between frames.
    - **Polynomial Fitting:** Connects predicted points with a 2nd-degree parabolic curve to handle dashed lines and stability.
3.  **GUI:** A `CustomTkinter` desktop interface manages inference in a separate thread to keep the application responsive.

### 🚀 Setup
```bash
chmod +x setup_project.sh launch_app.sh
./setup_project.sh
./launch_app.sh
```

### 🎓 Academic Context & Disclaimer
- **Context:** This project was developed as a **course assignment** for a Computer Vision class.

---

<a name="türkçe"></a>
## [TR] Teknik Detaylar

Bu proje, **Ultra-Fast-Lane-Detection (UFLD)** mimarisini temel alan ve üzerine eklenmiş özel bir stabilizasyon katmanı içeren verimli bir şerit algılama sistemidir.

### ⚙️ Nasıl Çalışır?
1.  **Satır Bazlı Sınıflandırma:** Model, yolu piksellerle taramak yerine, belirli yatay satırlarda (row anchors) şeridin en olası olduğu sütunu seçerek ilerler. Bu sayede işlem yükü azalır ve aşırı hızlı çalışır.
2.  **Zamansal Yumuşatma:** Kareler arasındaki titremeleri önlemek için özel bir `LaneSmoothing` motoru kullanılmıştır.
    - **EMA Filtresi:** Kareler arasındaki gani gürültüleri temizler.
    - **Polinom Uyumu:** Tespit edilen noktaları 2. dereceden bir eğri (parabol) ile birleştirerek süreklilik sağlar.
3.  **GUI:** `CustomTkinter` ile hazırlanan masaüstü arayüzü, yapay zeka işlemlerini ayrı bir iş parçacığında yöneterek donma yapmadan çalışır.

### 🚀 Kurulum
```bash
chmod +x setup_project.sh launch_app.sh
./setup_project.sh
./launch_app.sh
```

### 🎓 Akademik Bağlam ve Feragatname
- **Bağlam:** Bu proje, bir Bilgisayarlı Görü (Computer Vision) **ders ödevi** kapsamında geliştirilmiştir.

---

### 🖼️ Result Preview / Örnek Çıktı
![Example Detection](assets/demo_result.png)
