import os

import cv2
from moviepy.editor import VideoFileClip,concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



def find_faces(img):
    eys_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = eys_cascade.detectMultiScale(gray, 1.3, 5)
    return faces


def find_durations(clip):

    duration_list = []  
    start_time = 0   
    end_time = 0      
    for i, img in enumerate(clip.iter_frames(fps=20)):
        faces = find_faces(img)

        if len(faces) > 1 and start_time == 0:
            start_time = i / 20

        if start_time > 0 and len(faces) == 0:
            end_time = i / 20
            duration_list.append([start_time, end_time])

            start_time = end_time = 0

    return duration_list


 
def extract_subclip(filename,durations):

    dir_name = filename.split(".")[0]

    for d in durations:
        start_t, end_t = d
        ffmpeg_extract_subclip(filename, start_t, end_t)

    return dir_name


def concatenate_subclip(filepath):

    clips = []

    for root,_,files in os.walk(filepath):
        files.sort()

        for file in files:
            if os.path.splitext(file)[1] == ".mp4":
                filePath = os.path.join(root,file)
                video = VideoFileClip(filePath)
                clips.append(video)

    final_clip =  concatenate_videoclips(clips)

    
    final_clip.write_videofile("./target.mp4", fps=24, remove_temp=False)


if __name__ == "__main__":
    filename = "data/Heavenly Days/Heavenly Days MV.mp4"

    clip = VideoFileClip(filename)
    durations = find_durations(clip)
    dir_path = extract_subclip(filename,durations)

    concatenate_subclip("data/Heavenly Days/")