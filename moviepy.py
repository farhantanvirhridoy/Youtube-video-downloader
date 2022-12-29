# Import everything needed to edit video clips
from moviepy.editor import *

def merge(video, audio):
    clip = VideoFileClip(video)
    audioclip = AudioFileClip("allwell.mp3")
    videoclip = clip.set_audio(audioclip)
    videoclip.ipython_display()

import moviepy.editor as mp
clip = mp.VideoFileClip("movie.mp4")
clip_resized = clip.resize(height=360) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
clip_resized.write_videofile("movie_resized.mp4")