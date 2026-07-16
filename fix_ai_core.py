with open("ai_core.py", "r") as f:
    code = f.read()

# Fix the bug: `parts.append(prompt)` adds a string to `parts`, but `types.Content(role="user", parts=parts)` expects `types.Part` objects.
# We should do: `parts.append(types.Part.from_text(text=prompt))`

code = code.replace("parts.append(prompt)", "parts.append(types.Part.from_text(text=prompt))")

with open("ai_core.py", "w") as f:
    f.write(code)
