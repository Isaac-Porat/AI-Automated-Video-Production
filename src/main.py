# #!/usr/bin/env python3

import json
from youtubeFunctions import Object
from chatModel import Model
from llama_index.llms.openai import OpenAI

with open('prompts/general.json', 'r') as file:
  prompt_data = json.load(file)

gpt4 = OpenAI(temperature=0.9, model='gpt-4')
gpt3 = OpenAI(temperature=0.9, model='gpt-3.5-turbo-0125')

if __name__ == "__main__":
  yt = Object('https://www.youtube.com/watch?v=Frsonaaz858')
  md = Model(gpt4)

  # Downloads transcript.txt and returns transcript file path
  transcript: str = yt.download_transcript()

  # Downloads mp4 of video and returns download path
  mp4: str = yt.download_mp4()

  # Load index of LLM with transcript
  index = md.load_index(transcript)

  # Query the LLM with prompt and summary of transcript
  summary_of_data = 'Transcription of YouTube video'

  prompt = str(prompt_data)

  response = md.query(index, prompt, summary_of_data)

  print(response)

  # Edit the video with segment cuts from LLM
  response_json = json.loads(response)

  yt.edit_video(response_json)








