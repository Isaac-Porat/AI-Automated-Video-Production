import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/6.1.1_5/bin/ffmpeg"
from moviepy.editor import VideoFileClip
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

class Object:

  """
  Initialize the Object class with the video URL and set the root download path, sub root video path, and edited videos output path.
  :param video_url: The URL of the video to be processed.
  """
  def __init__(self, video_url: str) -> None:
    self.video_url: str = video_url
    self._root_download_path: str = 'output'
    self._sub_root_video_path: str = self._create_sub_root_folder()
    self._edited_videos_output_path: str = f'{self._sub_root_video_path}/edited_videos'


  """
  Create a sub root folder for the video download.
  """
  def _create_sub_root_folder(self) -> str:
    try:
      youtube_object: YouTube = YouTube(self.video_url)

      title_of_video: str = youtube_object.title
    except Exception as e:
      print('Error accessing pytube: %s' % e)

    folder_path: str = f'{self._root_download_path}/{title_of_video}'

    if not os.path.exists(folder_path):
      os.makedirs(folder_path, exist_ok=True)

    return folder_path

  """
  Download the transcript of the video.
  """
  def download_transcript(self) -> str:
    video_id: str = self.video_url.split('=')[1]

    try:
      transcript: list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
      print('Error accessing YouTubeTranscriptApi: %s' % e)

    transcript_download_path: str = f'{self._root_download_path}/{self._sub_root_video_path.split("output/")[1]}/transcript.txt'

    with open(transcript_download_path, 'w') as f:
      for i in transcript:
        text: str = i['text']
        start_time: str = i['start']
        duration_time: str = i['duration']
        f.write(f'{start_time} | {text}\n')

      return transcript_download_path

  """
  Download the video in mp4 format.
  """
  def download_mp4(self) -> str:
    download_path: str = f"{self._sub_root_video_path}"

    try:
      youtube_object: YouTube = YouTube(self.video_url)

      youtube_object: YouTube = youtube_object.streams.get_highest_resolution()

      youtube_object.download(output_path=download_path)
    except Exception as e:
      print('Error accessing pytube: %s' % e)

    return download_path

  """
  Edit the video based on the provided video cuts.
  :param video_cuts: A list of dictionaries, each containing the start and end time of a video segment to be cut.
  :return: A list of paths to the edited video segments.
  """
  def edit_video(self, video_cuts: list[dict]) -> list[str]:
    video_download_path: str = self.download_mp4

    video_paths: list[str] = []

    try:
      video: VideoFileClip = VideoFileClip(video_download_path)

      for i, clips in enumerate(video_cuts):
        segment: dict = clips['segment']

        desc: str = clips['desc']

        clip: VideoFileClip = video.subclip(segment['startTime'], segment['endTime'])

        video_out_path: str = f'{self.edited_videos_output_path}/{i}_video.mp4'

        clip.write_videofile(video_out_path, threads=4, fps=24, codec='libx264', preset='slow', ffmpeg_params=["-crf",'24'])

        video_paths.append(video_out_path)

      video.close()
    except Exception as e:
      print('Error accessing moviepy: %s' % e)

    return video_paths


