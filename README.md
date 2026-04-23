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

## 🚀 Installation & Running

### Prerequisites
- Python 3.10+
- NVIDIA GPU with CUDA support (Recommended)

### Quick Start
1.  **Clone the project:** Ensure all files are in `Ultra-Fast-Lane-Detection/`.
2.  **Launch the App:** 
    - Double-click **`LuminaLaneAI.desktop`** on your desktop.
    - *Or run:* `./launch_app.sh`

## 📁 Project Structure
- `gui_app.py`: Desktop application interface and threading logic.
- `video_process.py`: AI inference engine and smoothing algorithms.
- `weights/`: Pre-trained ResNet weights for lane detection.
- `venv/`: Pre-configured virtual environment with all dependencies.

## 🎓 Academic Credit
This project was developed/enhanced for a **Computer Vision** course to demonstrate the integration of modern deep learning architectures with practical software engineering and UI design.

---
*Developed with precision for high-performance lane detection.*
