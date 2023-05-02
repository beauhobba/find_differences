import cv2
import numpy as np
import math

if __name__ == '__main__':
    vn = input('Video Name or type * to run on a whole directory:  ')
    if '*' in vn:
        print('This feature is not supported yet')
    if '.' in vn:
        vidcap = cv2.VideoCapture('./data/'+vn)
    else:
        vidcap = cv2.VideoCapture('./data/'+vn+'.MP4')

    success, image = vidcap.read()
    fr = math.ceil(vidcap.get(cv2.CAP_PROP_FPS))
    count = 0
    calibration = None
    # Get the first frame
    r = []
    r_timer = []
    thresehold = 0.05
    t_sum = 0

    with open('roi.txt', 'r') as f:
        for val in f:
            r.append(int(val))

    with open('roi_timer.txt', 'r') as f:
        for val in f:
            r_timer.append(int(val))

    while success:
        success, image = vidcap.read()
        if count == 0:
            # crop the image
            calibration = image[int(r[1]):int(
                r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            count += 1
            continue
        try:
            selection = image[int(r[1]):int(r[1]+r[3]),
                              int(r[0]):int(r[0]+r[2])]
            diff = 255 - cv2.absdiff(calibration, selection)
            data = np.asarray(diff, dtype="int32")
            sum_ = (diff.sum())
            if count == 1:
                t_sum = sum_
                count += 1
                continue
            count += 1
            if ((sum_ > t_sum+t_sum*thresehold) or (sum_ < t_sum-t_sum*thresehold)):
                timer = image[int(r_timer[1]):int(
                    r_timer[1]+r_timer[3]), int(r_timer[0]):int(r_timer[0]+r_timer[2])]
                print(f'Occured at time: {count/fr}s, Occured on frame: {count}, Detected Frame Rate: {fr}')
                cv2.imshow("Image", selection)
                cv2.imshow("timer", timer)
                cv2.waitKey(1)
                inp = input('Type y to confirm this is correct: ')
                if (inp == 'y'):
                    break

        except:
            print("failed img reading")
