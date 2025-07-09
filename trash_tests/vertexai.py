from google import genai
from google.genai import types
import base64
from google.genai.types import Part
from google.genai.types import PartDict


def generate():
  client = genai.Client(
      vertexai=True,
      project="bloomia-dev",
      location="global",
  )


  model = "gemini-2.0-flash"
  contents = [
    types.Content(
      role="user",
      parts=[Part(text="I HATE GOOGLE CLOUD PLATFORM")],
    )
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 1,
    seed = 0,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    print(chunk.text, end="")

generate()