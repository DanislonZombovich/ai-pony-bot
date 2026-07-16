import discord
from google.genai import types

def get_moderation_tools():
    """Returns the function declarations for moderation actions."""
    
    kick_user = types.FunctionDeclaration(
        name="kick_user",
        description="Kick a user from the server.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person to kick."
                ),
                "reason": types.Schema(
                    type=types.Type.STRING,
                    description="The reason for kicking the user."
                )
            },
            required=["user_id"]
        )
    )
    
    ban_user = types.FunctionDeclaration(
        name="ban_user",
        description="Ban a user from the server.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person to ban."
                ),
                "reason": types.Schema(
                    type=types.Type.STRING,
                    description="The reason for banning the user."
                )
            },
            required=["user_id"]
        )
    )
    
    timeout_user = types.FunctionDeclaration(
        name="timeout_user",
        description="Timeout (mute) a user for a specific duration.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person to timeout."
                ),
                "minutes": types.Schema(
                    type=types.Type.INTEGER,
                    description="Duration in minutes."
                ),
                "reason": types.Schema(
                    type=types.Type.STRING,
                    description="The reason for the timeout."
                )
            },
            required=["user_id", "minutes"]
        )
    )

    return types.Tool(function_declarations=[kick_user, ban_user, timeout_user])

class ModerationHandler:
    def __init__(self, bot, admin_id):
        self.bot = bot
        self.admin_id = admin_id
        
    async def execute_call(self, call, guild: discord.Guild, author: discord.Member):
        if author.id != self.admin_id:
            return "У вас нет прав для выполнения этой команды. Слушаюсь только Данислона."
            
        args = call.args
        user_id = int(args.get("user_id", 0))
        reason = args.get("reason", "No reason provided")
        
        member = guild.get_member(user_id)
        if not member:
            return f"Пользователь с ID {user_id} не найден на сервере."
            
        try:
            if call.name == "kick_user":
                await member.kick(reason=reason)
                return f"Пользователь {member.name} кикнут. Причина: {reason}"
                
            elif call.name == "ban_user":
                await member.ban(reason=reason)
                return f"Пользователь {member.name} забанен. Причина: {reason}"
                
            elif call.name == "timeout_user":
                import datetime
                minutes = int(args.get("minutes", 10))
                duration = datetime.timedelta(minutes=minutes)
                await member.timeout(duration, reason=reason)
                return f"Пользователь {member.name} отправлен в тайм-аут на {minutes} минут."
                
        except discord.Forbidden:
            return "У меня нет прав для выполнения этого действия. Проверьте мою роль (она должна быть выше роли пользователя)."
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"
            
        return "Неизвестная команда."
