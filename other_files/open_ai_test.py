from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    # model="gpt-5.1",
    model='gpt-5-nano',
    input="Tell me a short joke about a fish"
)

print(response.output_text)
