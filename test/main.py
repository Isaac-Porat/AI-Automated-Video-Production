import os, logging, sys
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/6.1.1_5/bin/ffmpeg"
from moviepy.editor import *
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

class TestFunnel:
  def __init__(self, video_url: str):
    self.video_url = video_url
    self.mp4_downloads_path = 'test/downloads/mp4'
    self.transcript_downloads_path = '/Users/zakporat/Desktop/ChatGPT-YT-Transcript/test/downloads/transcripts'
    self.edited_output_path = 'test/downloads/edited-outputs'

  def get_video_url(self) -> str:
    return self.video_url

  def get_video_transcript_to_file(self) -> str:
    video_url = self.get_video_url()
    video_id = video_url.split('=')[1]

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    try:
      with open(f'{self.transcript_downloads_path}/{video_id}.txt', 'w') as f:
        for i in transcript:
          text = i['text']
          start_time = i['start']
          # duration_time = i['duration']

          f.write(f'{start_time} | {text}\n')

      return f'{self.transcript_downloads_path}/{video_id}.txt'

    except Exception as e:

      print(f'Error: ', e)

  def access_transcript_captions(self, time_segments) -> str:
    file_path = self.get_video_transcript_to_file()
    captions = ""

    with open(file_path, 'r') as f:
      lines = f.readlines()
      for line in lines:
        for segment in time_segments:
          start_time, duration_time = line.split(' | ')[:2]
          if float(start_time) >= segment['start_time'] and float(start_time) + float(duration_time) <= segment['end_time']:
            captions += line
    return captions

  def cut_video_into_segments(self, input_video_download: str, video_cuts: list[dict]) -> bool:
    video = VideoFileClip(input_video_download)
    clips = []

    for cut in video_cuts:
      print(cut)
      segment = cut['segment']
      desc = cut['desc']
      clip = video.subclip(segment['start_time'], segment['end_time'])
      clips.append(clip)

      # Access segment numbers from transcript file and add captions

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(f'{self.edited_output_path}/edited_video.mp4', threads=4, fps=24, codec='libx264', preset='slow', ffmpeg_params=["-crf",'24'])

    video.close()

run = TestFunnel('https://www.youtube.com/watch?v=9Gwp-bqzxwQ')
file_path = run.get_video_transcript_to_file()
# captions = run.access_transcript_captions()
[31.92, 50.52]

