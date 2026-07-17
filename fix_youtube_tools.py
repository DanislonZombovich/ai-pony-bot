with open("moderation.py", "r") as f:
    mod_code = f.read()

yt_tools = """
    play_youtube = types.FunctionDeclaration(
        name="play_youtube",
        description="Play audio from a YouTube video link in the current voice channel. This pauses AI live voice.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "url": types.Schema(
                    type=types.Type.STRING,
                    description="The full YouTube URL."
                )
            },
            required=["url"]
        )
    )

    stop_youtube = types.FunctionDeclaration(
        name="stop_youtube",
        description="Stop playing the YouTube video and resume AI live voice.",
    )
"""

mod_code = mod_code.replace("return types.Tool(function_declarations=[kick_user, ban_user, timeout_user, add_role, remove_role, join_voice, leave_voice])",
    yt_tools + "\n    return types.Tool(function_declarations=[kick_user, ban_user, timeout_user, add_role, remove_role, join_voice, leave_voice, play_youtube, stop_youtube])")

with open("moderation.py", "w") as f:
    f.write(mod_code)

print("Added play_youtube and stop_youtube tools")
