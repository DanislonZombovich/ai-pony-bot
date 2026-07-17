with open("live_voice.py", "r") as f:
    code = f.read()

# Replace the model name in live_voice.py
code = code.replace('model="models/gemini-2.0-flash-exp"', 'model="gemini-2.5-flash-native-audio-latest"')
# I might have written just 'gemini-2.0-flash-exp' earlier without 'models/' 

with open("live_voice.py", "w") as f:
    f.write(code)

print("Updated live_voice.py to use gemini-2.5-flash-native-audio-latest")
