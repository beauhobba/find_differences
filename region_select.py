import cv2
 
if __name__ == '__main__' :
    vn = input('Name of region sample file: ')
    if '.' in vn:
        vidcap = cv2.VideoCapture('./data/'+vn)
    else:
        vidcap = cv2.VideoCapture('./data/'+vn+'.MP4')

    success,image = vidcap.read()
    
    # Get the first frame 
    while success:
        cv2.imwrite("frame%d.jpg" % 0, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        break
    # Read image
    im = cv2.imread("frame0.jpg")
 
    # Select ROI
    cv2.namedWindow("select",2)
    cv2.resizeWindow("select", 600, 400)
    # cv2.resizeWindow("select", 200, 400)
    r = cv2.selectROI('select', im)
    cv2.destroyWindow('select')
    
    with open('roi.txt', 'w') as f:
        for val in r:
            f.write(str(int(val))+"\n")

    
    # Crop image
    imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
 
    # Display cropped image
    cv2.imshow("Image", imCrop)
    cv2.waitKey(0)
    
    print("Region Selected, proceed to running the other script")