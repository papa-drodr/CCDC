import os

import cv2 as cv
import numpy as np

video_file = "chessboard.mp4"
K = np.array(
    [
        [1.10906511e03, 0.0, 6.35873599e02],
        [0.0, 1.10914402e03, 3.63121374e02],
        [0.0, 0.0, 1.0],
    ]
)
dist_coeff = np.array([0.22140421, -0.73614716, 0.0021946, -0.00156452, 0.53864716])


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
    elif key == ord("\t"):  # Tab: Toggle between Original / Rectified view
        show_rectify = not show_rectify
    elif key == ord("c"):  # C: Save original & rectified images
        os.makedirs("data", exist_ok=True)
        # Generate rectified image (create map if not yet initialized)
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
