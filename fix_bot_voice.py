with open("bot.py", "r") as f:
    code = f.read()

# We need to execute `join_voice` and `leave_voice` from bot.py or moderation.py.
# moderation.py handles execution via `mod_handler.execute_call`. Let's pass the bot and voice_manager there, or handle it in bot.py directly.
# Handling in bot.py directly:

exec_logic = """
        if function_calls:
            for call in function_calls:
                if call.name == "join_voice":
                    channel_name = call.args.get("channel_name")
                    channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                    if channel:
                        success = await voice_manager.join_channel_direct(channel, message.guild)
                        if success:
                            final_response += f"\\n*Действие:* Зашел в канал {channel.name}."
                        else:
                            final_response += f"\\n*Действие:* Ошибка входа в канал {channel.name}."
                    else:
                        final_response += f"\\n*Действие:* Канал {channel_name} не найден."
                elif call.name == "leave_voice":
                    await voice_manager.leave_channel_direct(message.guild)
                    final_response += "\\n*Действие:* Покинул голосовой канал."
                else:
                    result = await mod_handler.execute_call(call, message.guild, message.author)
                    final_response += f"\\n*Действие:* {result}"
"""

code = code.replace(
"""        if function_calls:
            for call in function_calls:
                result = await mod_handler.execute_call(call, message.guild, message.author)
                final_response += f"\\n*Действие:* {result}\"""",
exec_logic
)

with open("bot.py", "w") as f:
    f.write(code)

print("Updated bot.py")
