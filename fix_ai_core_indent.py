with open("ai_core.py", "r") as f:
    code = f.read()

# Fix indentation of _process_attachments
lines = code.split("\n")
new_lines = []
for line in lines:
    if line.startswith("    async def _process_attachments(self, attachments):"):
        # We need to make sure it's 4 spaces
        pass # It is 4 spaces, but maybe the class definition wasn't closed or something?
        
    new_lines.append(line)

with open("ai_core.py", "w") as f:
    f.write("\n".join(new_lines))

