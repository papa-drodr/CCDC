import os

import cv2 as cv
import numpy as np

video_file = "chessboard.mp4"
K = np.array(
    [
        [685.09216986, 0.0, 966.21132282],
        [0.0, 690.91696396, 559.4759299],
        [0.0, 0.0, 1.0],
    ]
)
dist_coeff = np.array([-0.00965545, -0.00626342, -0.00048078, 0.00610018, 0.01461627])


# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), "Cannot read the given input, " + video_file

# Run distortion correction
show_rectify = True
map1, map2 = None, None
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    img_original = img.copy()

    # Rectify geometric distortion
    info = "Original"
    if show_rectify:
        if map1 is None or map2 is None:
            map1, map2 = cv.initUndistortRectifyMap(
                K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1
            )
        img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
        info = "Rectified"
    cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    cv.imshow("Geometric Distortion Correction", img)
    key = cv.waitKey(10)
    if key == ord(" "):  # Space: Pause
        key = cv.waitKey()
    if key == 27:  # ESC: Exit
        break
    elif key == ord("\t"):  # Tab: 원본 <-> 보정 토글
        show_rectify = not show_rectify
    elif key == ord("c"):  # C: 원본 & 보정 이미지 저장
        os.makedirs("data", exist_ok=True)
        # 보정 이미지 생성 (map이 없으면 새로 만들기)
        if map1 is None or map2 is None:
            map1, map2 = cv.initUndistortRectifyMap(
                K,
                dist_coeff,
                None,
                None,
                (img_original.shape[1], img_original.shape[0]),
                cv.CV_32FC1,
            )
        img_rectified = cv.remap(
            img_original, map1, map2, interpolation=cv.INTER_LINEAR
        )
        cv.imwrite("data/original.png", img_original)
        cv.imwrite("data/rectified.png", img_rectified)
        print("Saved: data/original.png, data/rectified.png")

video.release()
cv.destroyAllWindows()
