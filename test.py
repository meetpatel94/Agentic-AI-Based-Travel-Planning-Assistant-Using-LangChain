from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="gpt2"
)

response = pipe(
    "Hello",
    max_length=50
)

print(response)