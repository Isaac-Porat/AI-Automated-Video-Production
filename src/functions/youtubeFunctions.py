import os, logging, sys
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/6.1.1_5/bin/ffmpeg"
from moviepy.editor import VideoFileClip, concatenate_videoclips
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def save_transcript_to_file(transcript, video_id, transcript_downloads_path: str) -> str:
  try:
    with open(f'{transcript_downloads_path}/{video_id}.txt', 'w') as f:
      for i in transcript:
        text = i['text']
        start_time = i['start']
        duration_time = i['duration']
        f.write(f'{start_time} | {text}\n')
    return f'{transcript_downloads_path}/{video_id}.txt'
  except Exception as e:
    print(f'Error: ', e)

def get_video_transcript_to_file(video_url: str, transcript_downloads_path: str) -> str:
  video_id = video_url.split('=')[1]
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  return save_transcript_to_file(transcript, video_id, transcript_downloads_path)

def download_video_mp4(video_url: str, mp4_downloads_path: str):
  youtube_object = YouTube(video_url)
  youtube_object = youtube_object.streams.get_highest_resolution()
  title_of_video = youtube_object.title

  title_of_video = title_of_video.replace(':', '')

  try:
    youtube_object.download(output_path=f"{mp4_downloads_path}")
  except:
    print(f"Error occured downloading mp4 video")
  print("Download is completed successfully")
  # return f"{mp4_downloads_path}/{title_of_video}.mp4"
  return title_of_video

def edit_video(input_video_download: str, video_cuts: list[dict], edited_output_path: str) -> bool:
  video = VideoFileClip(input_video_download)
  for cut in video_cuts:
    print(cut)
    segment = cut['segment']
    print(segment)
    desc = cut['desc']
    print(desc)
    clip = video.subclip(segment['startTime'], segment['endTime'])
    clip.write_videofile(f'{edited_output_path}/{desc[0:10]}.mp4', threads=4, fps=24, codec='libx264', preset='slow', ffmpeg_params=["-crf",'24'])
  video.close()

# Example:
# if __name__ == "__main__":
#   video_url = 'https://www.youtube.com/watch?v=qHDAKevRrvw'
#   transcript_downloads_path = 'transcripts'
#   mp4_downloads_path = 'videos'
#   edited_output_path = 'edited_videos'
#   video_cuts = [{'segment': {'startTime': 10, 'endTime': 20}, 'desc': 'First cut'}, {'segment': {'startTime': 30, 'endTime': 40}, 'desc': 'Second cut'}]

#   video_url = get_video_url(video_url)
#   transcript_file = get_video_transcript_to_file(video_url, transcript_downloads_path)
#   video_download = download_video_mp4(video_url, mp4_downloads_path)
#   edited_videos = edit_video(video_download, video_cuts, edited_output_path)