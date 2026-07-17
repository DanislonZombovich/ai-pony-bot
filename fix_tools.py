import requests

with open("ai_core.py", "r") as f:
    code = f.read()

# We'll just define the new tool logic in `moderation.py` to keep tools centralized, 
# or since it's voice related, maybe `live_voice.py` or just `bot.py`.
# Wait, the tools need to be defined somewhere. Let's add them to `moderation.py` but call them server tools.

with open("moderation.py", "r") as f:
    mod_code = f.read()

voice_tools = """
    join_voice = types.FunctionDeclaration(
        name="join_voice",
        description="Join a specific voice channel by its name or ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "channel_name": types.Schema(
                    type=types.Type.STRING,
                    description="The name of the voice channel to join."
                )
            },
            required=["channel_name"]
        )
    )

    leave_voice = types.FunctionDeclaration(
        name="leave_voice",
        description="Leave the voice channel.",
    )
"""

mod_code = mod_code.replace("return types.Tool(function_declarations=[kick_user, ban_user, timeout_user, add_role, remove_role])",
    voice_tools + "\n    return types.Tool(function_declarations=[kick_user, ban_user, timeout_user, add_role, remove_role, join_voice, leave_voice])")

with open("moderation.py", "w") as f:
    f.write(mod_code)

print("Updated moderation.py with voice tools")
