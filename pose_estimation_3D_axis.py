import os

import cv2 as cv
import numpy as np

# The given video and calibration data
video_file = "chessboard.mp4"
K = np.array(
    [
        [1.12415948e03, 0.0, 6.40625897e02],
        [0.0, 1.12449519e03, 3.52677124e02],
        [0.0, 0.0, 1.0],
    ]
)
dist_coeff = np.array([0.25212485, -1.01833791, 0.0017293, -0.00147241, 0.84109214])
board_pattern = (10, 7)
board_cellsize = 0.025
board_criteria = (
    cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK
)

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), "Cannot read the given input, " + video_file

# Prepare 3D axis points for AR (origin + X/Y/Z endpoints)
axis_len = board_cellsize * 3
axis_points = np.array(
    [
        [0, 0, 0],  # origin
        [axis_len, 0, 0],  # X end
        [0, axis_len, 0],  # Y end
        [0, 0, -axis_len],
    ],
    dtype=np.float32,
)  # Z end (upward)

# Prepare 3D points on a chessboard
obj_points = board_cellsize * np.array(
    [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
)

# Run pose estimation
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Halve high resolution images to detect (scaled with K)
    scale = 0.5
    img_small = cv.resize(img, (0, 0), fx=scale, fy=scale)
    K_small = K * scale
    K_small[2, 2] = 1.0

    # Estimate the camera pose
    success, img_points = cv.findChessboardCorners(
        img_small, board_pattern, board_criteria
    )
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K_small, dist_coeff)

        # Project 3D axis points onto the image
        pts, _ = cv.projectPoints(axis_points, rvec, tvec, K_small, dist_coeff)
        origin = tuple(pts[0].flatten().astype(int))
        x_end = tuple(pts[1].flatten().astype(int))
        y_end = tuple(pts[2].flatten().astype(int))
        z_end = tuple(pts[3].flatten().astype(int))

        # Draw X (red), Y (green), Z (blue) axes with arrows
        cv.arrowedLine(img_small, origin, x_end, (0, 0, 255), 3, tipLength=0.2)
        cv.arrowedLine(img_small, origin, y_end, (0, 255, 0), 3, tipLength=0.2)
        cv.arrowedLine(img_small, origin, z_end, (255, 0, 0), 3, tipLength=0.2)

        # Draw X, Y, Z text labels at each axis end
        cv.putText(img_small, "X", x_end, cv.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)
        cv.putText(img_small, "Y", y_end, cv.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 2)
        cv.putText(img_small, "Z", z_end, cv.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 2)

        # Print the camera position
        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f"XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]"
        cv.putText(img_small, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow("Pose Estimation (Chessboard)", img_small)
    key = cv.waitKey(10)
    if key == ord(" "):
        key = cv.waitKey()
    if key == 27:  # ESC: Exit
        break
    elif key == ord("c") and success:  # C: Save screenshot
        os.makedirs("data", exist_ok=True)
        cv.imwrite("data/ar_result.png", img_small)
        print("Saved: data/ar_result.png")

video.release()
cv.destroyAllWindows()
