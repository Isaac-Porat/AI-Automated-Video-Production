#!/usr/bin/env python3

import json
from functions.youtubeFunctions import get_video_transcript_to_file, download_video_mp4, edit_video
from functions.chatModel import init_openai, init_model, load_index, query

with open('prompts/general.json', 'r') as file:
  prompt_data = json.load(file)

if __name__ == "__main__":

  transcripts_download_path = '/Users/zakporat/Desktop/ChatGPT-YT-Transcript/src/downloads/transcripts'
  mp4_downloads_path = '/Users/zakporat/Desktop/ChatGPT-YT-Transcript/src/downloads/mp4'
  output_path = '/Users/zakporat/Desktop/ChatGPT-YT-Transcript/src/downloads/edited-outputs'

  video_url = 'https://www.youtube.com/watch?v=Frsonaaz858'

  file_path_transcript = get_video_transcript_to_file(video_url, transcripts_download_path)

  file_path_mp4 = download_video_mp4(video_url, mp4_downloads_path)

  print(file_path_transcript)

  print(file_path_mp4)

  gpt4, gpt3 = init_openai()

  file_path, gpt4, gpt3 = init_model(file_path_transcript, gpt4, gpt3)

  index = load_index(file_path, gpt4)

  summary_of_data = "Transcription of YouTube video."

  prompt = str(prompt_data)

  response = query(index, prompt, summary_of_data, gpt4)

  print(response)

  response_json = json.loads(response)

  edit_video(f"{mp4_downloads_path}/{file_path_mp4}.mp4", response_json, output_path)



