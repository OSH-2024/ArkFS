import ollama

features = []

features.append(ollama.embeddings(model='llama3', prompt='The sky is blue because of rayleigh scattering'))

print(features)