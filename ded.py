from google import genai

client = genai.Client()  # make sure GOOGLE_API_KEY is set
models = client.models.list()
for m in models:
    print(m)
