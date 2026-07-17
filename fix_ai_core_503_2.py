with open("ai_core.py", "r") as f:
    code = f.read()

# Remove google.api_core and replace it with generic exception catch because we don't have google.api_core installed (google-genai is a different package).
code = code.replace("from google.api_core.exceptions import ServiceUnavailable, InternalServerError", "")

with open("ai_core.py", "w") as f:
    f.write(code)

print("Updated ai_core.py")
