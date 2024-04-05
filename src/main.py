# #!/usr/bin/env python3

import json
from youtubeFunctions import Object
from chatModel import init_openai, init_model, load_index, query

with open('prompts/general.json', 'r') as file:
  prompt_data = json.load(file)

if __name__ == "__main__":
  yt = Object('https://www.youtube.com/watch?v=Frsonaaz858')

  # Downloads transcript.txt and returns transcript file path
  transcript: str = yt.download_transcript()

  # Downloads mp4 of video and returns download path
  mp4: str = yt.download_mp4()


#   gpt4, gpt3 = init_openai()

#   file_path, gpt4, gpt3 = init_model(file_path_transcript, gpt4, gpt3)

#   index = load_index(file_path, gpt4)

#   summary_of_data = "Transcription of YouTube video."

#   prompt = str(prompt_data)

#   response = query(index, prompt, summary_of_data, gpt4)

#   print(response)

#   response_json = json.loads(response)

#   edit_video(f"{mp4_downloads_path}/{file_path_mp4}.mp4", response_json, output_path)



