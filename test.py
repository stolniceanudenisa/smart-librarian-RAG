# from openai import OpenAI

# # Put your API key here
# api_key = 




# if not api_key or not api_key.startswith("sk-"):
#     raise ValueError("❌ Please provide a valid OpenAI API key (must start with sk-).")

# # Init client
# client = OpenAI(api_key=api_key)

# # Simple test prompt
# resp = client.chat.completions.create(
#     model="gpt-4o-mini",  # small/lightweight 4o model
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Write a one-sentence summary of The Hobbit."}
#     ],
#     max_tokens=50
# )

# print("✅ API call successful!")
# print("Assistant:", resp.choices[0].message.content.strip())
