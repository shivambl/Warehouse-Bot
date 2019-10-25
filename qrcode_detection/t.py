from test_framework import TestRunner as tr
import cv2, math, sys
import numpy as np
import pyzbar.pyzbar as pyzbar
def euclidean_distance(p1, p2):
    #! WARNING: Returns square of actual euclidean distance
    return ((p1[1] - p2[1]) ** 2 + (p1[0] - p2[0]) ** 2)
    
def normal_distance(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    yield np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
    dx = (p2[0] - p1[0])
    dy = (p2[1] - p1[1])
    if dx == 0:
        yield 0, 1
    else:
        yield dy/dx, 0

def find_moments(c):
    mu = cv2.moments(c, False)
    return ((mu['m10'] / (mu['m00'] + 1e-5)), (mu['m01'] / (mu['m00'] + 1e-5)))

def find_top(contours, heirarchy):
    # heirarchy ~~ [Next, Previous, First_Child, Parent]
    markers = [] # Stores TL, TR, BL markers
    for i in range(len(contours)):
        k = i
        c = 0
        while heirarchy[k][2] != -1:
            k = heirarchy[k][2]
            c += 1
        if heirarchy[k][2] != -1:
            c += 1
        if c >= 2:
            markers.append(i)
    markers = list(set(markers))
    pp(len(markers), i="length of markers")
    assert len(markers) == 3
    m1 = find_moments(contours[markers[0]])
    m2 = find_moments(contours[markers[1]])
    m3 = find_moments(contours[markers[2]])
    # print(m1, m2, m3)
    ab = euclidean_distance(m1, m2)
    bc = euclidean_distance(m2, m3)
    ca = euclidean_distance(m3, m1)
    m = max((ab, m3), (bc, m1), (ca, m2))
    # print(m)
    return m[1]

def testdata(i, d, t):
    return cv2.imread(d, cv2.IMREAD_GRAYSCALE)

def desc(i, d, t):
    # return i
    return f"{i} of {t} - {d}"
#qr = cv2.QRCodeDetector()

def solve(data, desc):
    desc = str(desc)
    original_gray = data
    #original_gray = cv2.resize(original_gray, dsize=None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR_EXACT)
    show(original_gray, True, f'{desc} Original Gray', 'gray')
    inverted_gray = cv2.bitwise_not(original_gray)
    #data, bbox, _ = qr.detectAndDecode(original_gray)
    qrcodes = pyzbar.decode(original_gray)
    assert len(qrcodes)==1
    x,y,h,w = qrcodes[0].rect
    #bbox=[]
    #bbox = [(x,y),(x+h,y),(x+h,y+w),(x,y+w)]
    #assert bbox is not None
    #x, y, h, w = cv2.boundingRect(bbox)
    _, contours, heirarchy= cv2.findContours(inverted_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cs in contours:
        q,w,e,r = cv2.boundingRect(cs)
        cv2.rectangle(original_gray, (q,w), (q+e,w+r), 127, 2)
    heirarchy = heirarchy[0]
    top = find_top(contours, heirarchy)
    #cx, cy = 0, 0
    #for pts in bbox:
    #    cx, cy = cx+pts[0][0], cy+pts[0][1]
    #    center = (cx/4, cy/4)
    center = (x + h/2, y+ w/2)
    pp(top, i='top')
    pp(center, i='centre')
    disp = cv2.cvtColor(np.copy(original_gray), cv2.COLOR_GRAY2RGB)
    cv2.circle(disp, (int(top[0]), int(top[1])), 10, (255,0,0), -1)
    cv2.circle(disp, (int(center[0]), int(center[1])), 10, (255,0,0), -1)
    show(disp, False, desc + " Features Extracted", None)

    dy = top[1] - center[1]
    dx = top[0] - center[0]
    slope = dy / dx
    deg  = math.degrees(math.atan(slope))
    pp(slope, i='slope')
    pp(dy, i='dy')
    pp(dx, i='dx')


show, pp, test, _ = tr("test_images", "qr_0*.png", solve, testdata, desc, True)

# print(_)
#solve(cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE), "")
test()
