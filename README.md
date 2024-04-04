```
mkdir -p downloads/{edited-outputs,mp4,transcripts}
python3 -m venv venv
touch .env
^ add OPENAI_API_KEY = ""
```

File structure:
- downloads -> all output from functions
- functions -> reusable function code
- prompts -> chat prompts in json format
- test -> function testing funnel

TODO:
- [ ] Test prompts for specific video types
- [ ] Add caption support
