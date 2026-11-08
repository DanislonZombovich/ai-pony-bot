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

    
    add_role = types.FunctionDeclaration(
        name="add_role",
        description="Add a role to a user. You can provide an approximate role name or ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person."
                ),
                "role_name": types.Schema(
                    type=types.Type.STRING,
                    description="The approximate name of the role to add."
                )
            },
            required=["user_id", "role_name"]
        )
    )

    remove_role = types.FunctionDeclaration(
        name="remove_role",
        description="Remove a role from a user. You can provide an approximate role name or ID, or say 'all' to remove all roles.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person."
                ),
                "role_name": types.Schema(
                    type=types.Type.STRING,
                    description="The approximate name of the role to remove, or 'all'."
                )
            },
            required=["user_id", "role_name"]
        )
    )

    
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

    return types.Tool(function_declarations=[kick_user, ban_user, timeout_user, add_role, remove_role, join_voice, leave_voice, play_youtube, stop_youtube])


def find_best_role(guild, search_term):
    if not search_term: return None
    search_term = search_term.lower()
    for role in guild.roles:
        if str(role.id) == search_term:
            return role
        if role.name.lower() == search_term:
            return role
    
    # Partial match
    for role in guild.roles:
        if search_term in role.name.lower():
            return role
    return None

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
                
        
            elif call.name == "add_role":
                role_name = args.get("role_name", "")
                role = find_best_role(guild, role_name)
                if not role:
                    return f"Роль похожая на '{role_name}' не найдена на сервере."
                await member.add_roles(role)
                return f"Роль {role.name} выдана пользователю {member.name}."

            elif call.name == "remove_role":
                role_name = args.get("role_name", "")
                if role_name.lower() == "all" or role_name.lower() == "все":
                    roles_to_remove = [r for r in member.roles if r != guild.default_role]
                    if roles_to_remove:
                        await member.remove_roles(*roles_to_remove)
                        return f"Все роли сняты с пользователя {member.name}."
                    return f"У пользователя {member.name} нет ролей."
                    
                role = find_best_role(guild, role_name)
                if not role:
                    return f"Роль похожая на '{role_name}' не найдена на сервере."
                await member.remove_roles(role)
                return f"Роль {role.name} снята с пользователя {member.name}."

        except discord.Forbidden:
            return "У меня нет прав для выполнения этого действия. Проверьте мою роль (она должна быть выше роли пользователя)."
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"
            
        return "Неизвестная команда."
