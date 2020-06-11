# import all the necessary packages
import numpy as np
import cv2
from tkinter import *

root = Tk()

# load the images
pic1 = PhotoImage(file="face1.png")
pic2 = PhotoImage(file="face2.png")

# add labels
label1 = Label(root, image=pic1)
label2 = Label(root, image=pic2)

# add button for morphing
b = Button(root, text="morphing")

# allign the labels and button
label1.pack(side=LEFT)
label2.pack(side=RIGHT)
b.pack(side=BOTTOM)

# for static output
root.mainloop()

def readPoints(path) :
    # Create an array of points.
    points = []
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))

    return points

# Define affine transform 
def applyAffineTransformation(src, srcTri, destinationTri, size) :

    # find the affine transform.
    warpmatrix = cv2.getAffineTransform( np.float32(srcTri), np.float32(destinationTri) )

    # Apply the Affine Transform 
    destination = cv2.warpAffine( src, warpmatrix, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return destination


# Warps and alpha blends triangular regions from pic1 and pic2 to img
def morphingATriangle(pic1, pic2, img, p1, p2, p, alpha) :

    # rectangle foreach triangle
    q1 = cv2.boundingRect(np.float32([p1]))
    q2 = cv2.boundingRect(np.float32([p2]))
    q = cv2.boundingRect(np.float32([p]))


    # Offset points
    p1Rect = []
    p2Rect = []
    pRect = []


    for i in range(0, 3):
        pRect.append(((p[i][0] - q[0]),(p[i][1] - q[1])))
        p1Rect.append(((p1[i][0] - q1[0]),(p1[i][1] - q1[1])))
        p2Rect.append(((p2[i][0] - q2[0]),(p2[i][1] - q2[1])))


    # Get mask by filling triangle
    mask = np.zeros((q[3], q[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(pRect), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    pic1Rect = pic1[q1[1]:q1[1] + q1[3], q1[0]:q1[0] + q1[2]]
    pic2Rect = pic2[q2[1]:q2[1] + q2[3], q2[0]:q2[0] + q2[2]]

    size = (q[2], q[3])
    warpImage1 = applyAffineTransformation(pic1Rect, p1Rect, pRect, size)
    warpImage2 = applyAffineTransformation(pic2Rect, p2Rect, pRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[q[1]:q[1]+q[3], q[0]:q[0]+q[2]] = img[q[1]:q[1]+q[3], q[0]:q[0]+q[2]] * ( 1 - mask ) + imgRect * mask


if __name__ == '__main__' :

    file1 = 'face1.png'
    file2 = 'face2.png'
    alpha = 0.5

    # Read images
    pic1 = cv2.imread(file1)
    pic2 = cv2.imread(file2)

    # Convert Mat to float data type
    pic1 = np.float32(pic1)
    pic2 = np.float32(pic2)

    # Read array of corresponding points
    pt1 = readPoints(file1 + '.txt')
    pt2 = readPoints(file2 + '.txt')
    points = []

    # Compute average point coordinates
    for i in range(0, len(pt1)):
        a = ( 1 - alpha ) * pt1[i][0] + alpha * pt2[i][0]
        b = ( 1 - alpha ) * pt1[i][1] + alpha * pt2[i][1]
        points.append((a,b))


    # Give the space for final output
    imgMorph = np.zeros(pic1.shape, dtype = pic1.dtype)

    # Read triangles from triangle.txt
    with open("triangle.txt") as file :
        for line in file :
            x,y,z = line.split()

            x = int(x)
            y = int(y)
            z = int(z)

            p1 = [pt1[x], pt1[y], pt1[z]]
            p2 = [pt2[x], pt2[y], pt2[z]]
            p = [ points[x], points[y], points[z] ]

            # Morph one triangle at a time.
            morphingATriangle(pic1, pic2, imgMorph, p1, p2, p, alpha)


    # Display the Result
    cv2.imshow("Morphed Face", np.uint8(imgMorph))
    cv2.waitKey(0)
