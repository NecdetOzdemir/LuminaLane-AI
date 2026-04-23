# LuminaLane AI: Ultra-Fast & Stable Lane Detection 🛣️🚀

LuminaLane AI is a premium desktop application for real-time lane detection in videos. It leverages state-of-the-art Deep Learning models and advanced temporal smoothing to provide rock-solid performance on diverse road conditions.

## ✨ Key Features
- **Ultra-Fast Performance:** Uses the "Row-based Classification" architecture, capable of 300+ FPS.
- **Premium GUI:** Modern, dark-themed interface built with `CustomTkinter`.
- **Advanced Stability:** Custom-built `LaneSmoothing` engine using Polynomial Fitting and EMA filters.
- **Auto-Play Integration:** Automatically opens processed videos in your system's default player.
- **Easy Deployment:** Native Linux desktop shortcut for one-click access.

## 🛠️ Technical Architecture
### 1. The Core AI (UFLD)
The project is built on the **Ultra-Fast-Lane-Detection (UFLD)** framework. Unlike traditional pixel-wise segmentation, UFLD treats lane detection as a row-selection problem, making it significantly more efficient for high-speed driving scenarios.

### 2. Stabilization Layer
To handle the "flicker" and noise inherent in real-world videos, we implemented a custom **Smoothing Engine**:
- **Point-based Outlier Rejection:** Discards aberrant detections.
- **Polynomial Fitting:** Generates a consistent 2nd-degree curve for better visualization.
- **Temporal EMA:** Maintains smooth transitions between frames.

## 🚀 Installation for New Users

To use LuminaLane AI on a new computer:

1.  **Clone with Git LFS:**
    ```bash
    git clone https://github.com/NecdetOzdemir/LuminaLane-AI.git
    cd LuminaLane-AI
    ```
2.  **Run the Setup Script:**
    This will create the virtual environment and install all dependencies.
    ```bash
    chmod +x setup_project.sh launch_app.sh
    ./setup_project.sh
    ```
3.  **Start the App:**
    ```bash
    ./launch_app.sh
    ```

## 📁 Project Structure
- `gui_app.py`: Desktop application interface and threading logic.
- `video_process.py`: AI inference engine and smoothing algorithms.
- `weights/`: Pre-trained ResNet weights for lane detection.
- `venv/`: Pre-configured virtual environment with all dependencies.

## 🎓 Academic Credit
This project was developed/enhanced for a **Computer Vision** course to demonstrate the integration of modern deep learning architectures with practical software engineering and UI design.

---
*Developed with precision for high-performance lane detection.*
