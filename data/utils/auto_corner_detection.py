import pytesseract
import argparse
import imutils
import cv2
import re
from imutils.perspective import four_point_transform


def auto_corner(frame):

    image = frame.copy()
    image = imutils.resize(image, width=500)
    ratio = frame.shape[1] / float(image.shape[1])
    # convert the image to grayscale, blur it slightly, and then apply edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)
    # check to see if we should show the output of our edge detection
    # find contours in the edge map and sort them by size in descending order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # initialize a contour that corresponds to the paper outline
    receiptCnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we can
        # assume we have found the outline of the paper
        if len(approx) == 4:
            receiptCnt = approx
            break
    # if the paper contour is empty then our script could not find the
    # outline and we should be notified
    if receiptCnt is None:
        raise Exception(("Could not find paper outline. "
                         "Try debugging your edge detection and contour steps."))
    # check to see if we should draw the contour of the paper on the
    # image and then display it to our screen

    output = image.copy()
    cv2.drawContours(output, [receiptCnt], -1, (0, 255, 0), 2)
    # cv2.imshow("Paper Outline", output)
    cv2.waitKey(0)
    # apply a four-point perspective transform to the *original* image to
    # obtain a top-down bird's-eye view of the paper
    receipt = four_point_transform(frame, receiptCnt.reshape(4, 2) * ratio)
    # show transformed image
    # cv2.imshow("Paper Transform", imutils.resize(receipt, width=500))
    cv2.imwrite('opencv_images/paper_outline.jpg', output)
    cv2.imwrite('opencv_images/paper_edged.jpg', edged)
    cv2.imwrite('opencv_images/paper_final.jpg', receipt)
    cv2.imwrite('opencv_images/paper_gray.jpg', gray)
    return receipt

