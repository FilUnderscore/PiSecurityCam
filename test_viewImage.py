# Using cv2 for view an image

import numpy as np
import cv2

img = cv2. imread ("/home/pi64/Repo/embedded_git_tutorial_repository/test.jpg")

desired_width = 100
desired_height = 200
resized_img = cv2.resize(img, (desired_width, desired_height))

cv2. imshow("Look at this!", img)
cv2. waitKey(0)
cv2.destroyAllWindows ()
