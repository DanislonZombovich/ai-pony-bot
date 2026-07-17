with open("ai_core.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("    async def _process_attachments"):
        new_lines.insert(len(new_lines)-1, "class AICore:\n")
        new_lines.append(line)
    elif line == "class AICore:\n" and len(new_lines) > 0 and new_lines[-1] == "class AICore:\n":
        pass
    else:
        new_lines.append(line)

with open("ai_core.py", "w") as f:
    f.writelines(new_lines)
