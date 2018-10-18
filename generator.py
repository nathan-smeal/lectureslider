# this file generates slides and potentially flash cards for GAtech udacity courses.
# It takes in SRT files and matching video files and performs lookup and gets the still for the last timestamp for each subtitle entry.

input_srt = './inputs/229 - Overview of Lectures on Graph Algorithms - lang_en_vs1.srt'
input_vid = './inputs/1 - Overview of Lectures on Graph Algorithms.mp4'


import cv2
import pysrt
import datetime
import time


cap = cv2.VideoCapture(input_vid)
fps = cap.get(cv2.CAP_PROP_FPS)

# TODO: combine several caption images into 1 if they are similar enough
# meaning if they earlier image matches enough.... then combine.  idk that's a little touhg
# really intesting problem though

# TODO: also take the text and text multiline, handle the longer ones.

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,100)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

print(fps)
def totalTime(end_time: datetime.time):
    return end_time.hour * 3600000 + end_time.second * 1000 + end_time.microsecond / 1000
timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
calc_timestamps = [0.0]
subs = pysrt.open(input_srt)
for sub in subs:
    print(sub)
#  test : pysrt.SubRipItem..end
isubs = iter(subs)
next_sub = next(isubs)  # type:  pysrt.SubRipItem
mstime = totalTime(next_sub.end.to_time())
# datetime.time.hou
# print(next_sub.te)
print(next_sub.end.to_time().microsecond * 1000)
# print(time.mktime(next_sub.end))
while(cap.isOpened()):
    frame_exists, curr_frame = cap.read()
    if frame_exists:
        # print(mstime)
        # print(cap.get(cv2.CAP_PROP_POS_MSEC))
        # print(abs(mstime - cap.get(cv2.CAP_PROP_POS_MSEC)))
        # if len(timestamps) == 30:
        #     exit(1)
        if abs(mstime - cap.get(cv2.CAP_PROP_POS_MSEC)) < fps:
            print('Found')
            img = curr_frame
            img = cv2.putText(img,next_sub.text, 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.imshow("img",img)
            cv2.waitKey(0)
            next_sub = next(isubs)
            mstime = totalTime(next_sub.end.to_time())
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        calc_timestamps.append(calc_timestamps[-1] + 1000/fps)
    else:
        break

cap.release()

# for i, (ts, cts) in enumerate(zip(timestamps, calc_timestamps)):
#     print('Frame %d difference:'%i, abs(ts - cts))