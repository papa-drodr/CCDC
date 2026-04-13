# CCDC — Camera Calibration, Distortion Correction (& AR)

A simple tool for camera calibration, lens distortion correction, and 3D axis AR visualization using OpenCV and a chessboard pattern.

---

## Features

- **Camera Calibration** — Estimate intrinsic parameters (K) and distortion coefficients from a chessboard video
- **Distortion Correction** — Rectify lens distortion using calibration results
- **3D Axis AR** — Estimate camera pose via PnP and overlay X/Y/Z axes on the chessboard in real time

---

## Requirements

```
python >= 3.8
opencv-python
numpy
```

Install dependencies:
```bash
pip install opencv-python numpy
```

---

## Usage

### 1. Camera Calibration

```bash
python camera_calibration.py
```

- **Space**: Pause and preview detected corners
- **Enter**: Select the current frame
- **ESC**: Finish selection and run calibration

> Recommended: Select at least 20 frames from various angles for accurate results.

### 2. Distortion Correction

After calibration, paste the output `K` and `dist_coeff` values into `distortion_correction.py`, then:

```bash
python distortion_correction.py
```

- **Tab**: Toggle between Original / Rectified view
- **C**: Save both original and rectified images to `data/`
- **Space**: Pause
- **ESC**: Exit

### 3. Pose Estimation & 3D Axis AR

After calibration, paste the output `K` and `dist_coeff` values into `pose_estimation_ar.py`, then:

```bash
python pose_estimation_ar.py
```

- **C**: Save AR screenshot to `data/ar_result.png`
- **Space**: Pause
- **ESC**: Exit

> The script detects the chessboard in each frame, estimates the camera pose using `cv.solvePnP()`, and draws color-coded 3D axes (X: red, Y: green, Z: blue) with text labels on the board.

---

## Calibration Results

**Camera**: iPhone 15 Plus (Action Mode)  
**Chessboard**: 9×6 inner corners, cell size = 25mm  
**Number of selected images**: 20+  
**RMS error**: 0.8143

![CC_result](data/CC_result.png)

### Camera Matrix (K)

```
[[685.09216986,   0.          , 966.21132282],
 [  0.         , 690.91696396, 559.47592990],
 [  0.         ,   0.         ,   1.        ]]
```

| Parameter | Value |
|-----------|-------|
| fx | 685.09 px |
| fy | 690.92 px |
| cx | 966.21 px |
| cy | 559.48 px |

### Distortion Coefficients

| k1 | k2 | p1 | p2 | k3 |
|----|----|----|----|----|
| -0.00966 | -0.00626 | -0.00048 | 0.00610 | 0.01462 |

> Note: Distortion coefficients are small because iPhone applies internal lens correction before saving video. The calibration itself is valid (RMS < 1.0).

---

## Demo

### Distortion Correction (Original vs Rectified)

| Original | Rectified |
|----------|-----------|
| ![original](data/original.png) | ![rectified](data/rectified.png) |

### Pose Estimation & 3D Axis AR

![ar_result](data/ar_result.png)

---

## File Structure

```
CCDC/
├── camera_calibration.py     # Calibration script
├── distortion_correction.py  # Distortion correction script
├── pose_estimation_ar.py     # Pose estimation & 3D axis AR script
├── data/
│   ├── original.png          # Screenshot before distortion correction (press C)
│   ├── rectified.png         # Screenshot after distortion correction (press C)
│   └── ar_result.png         # AR result screenshot (press C)
└── README.md
```

---

## Known Issues

**AR axes rarely appear / position keeps shifting**

- **Cause:** iPhone Action Mode applies internal optical stabilization and lens distortion correction before saving the video. As a result, the calibrated K and distortion coefficients do not reflect the true optical characteristics of the lens, leading to unstable pose estimation.

**Planned fix:** Re-shoot the chessboard video using iPhone standard camera mode (1× lens, no Action Mode) to obtain accurate K and distortion coefficients, then re-run calibration.

**Scheduled after midterm exam (early May)**