import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GEMINI_API_KEY', ''))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="precise and concise outputs",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "How many pizza shopw in New York",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I need to be more specific to give you an exact number.  The number of pizza shops in New York will vary greatly depending on if you mean:\n\n* **New York City:** This will have the highest concentration of pizza places. \n* **New York State:** This will include a wide range of areas, from cities to small towns.\n\nTo get an accurate number, please tell me:\n\n* **Do you want the number for New York City or New York State?** \n \nOnce I know this, I can do a better job finding the information you need! 🍕 \n",
      ],
    },
  ]
)

response = chat_session.send_message("essay on ai")

print(response.text)
