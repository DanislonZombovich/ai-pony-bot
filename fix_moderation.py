import requests

with open("moderation.py", "r") as f:
    mod_code = f.read()

# Add add_role and remove_role tools
new_mod_tools = """
    add_role = types.FunctionDeclaration(
        name="add_role",
        description="Add a role to a user. You must provide the exact role name or ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person."
                ),
                "role_name": types.Schema(
                    type=types.Type.STRING,
                    description="The exact name of the role to add."
                )
            },
            required=["user_id", "role_name"]
        )
    )

    remove_role = types.FunctionDeclaration(
        name="remove_role",
        description="Remove a role from a user. You must provide the exact role name or ID.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "user_id": types.Schema(
                    type=types.Type.STRING,
                    description="The Discord user ID of the person."
                ),
                "role_name": types.Schema(
                    type=types.Type.STRING,
                    description="The exact name of the role to remove."
                )
            },
            required=["user_id", "role_name"]
        )
    )
"""

# Inject before return types.Tool(...)
mod_code = mod_code.replace("return types.Tool(function_declarations=[kick_user, ban_user, timeout_user])",
new_mod_tools + "\n    return types.Tool(function_declarations=[kick_user, ban_user, timeout_user, add_role, remove_role])")

# Inject execution logic
new_exec_logic = """
            elif call.name == "add_role":
                role_name = args.get("role_name")
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    # try by ID
                    try:
                        role = guild.get_role(int(role_name))
                    except:
                        pass
                if not role:
                    return f"Роль {role_name} не найдена на сервере."
                await member.add_roles(role)
                return f"Роль {role.name} выдана пользователю {member.name}."

            elif call.name == "remove_role":
                role_name = args.get("role_name")
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    try:
                        role = guild.get_role(int(role_name))
                    except:
                        pass
                if not role:
                    return f"Роль {role_name} не найдена на сервере."
                await member.remove_roles(role)
                return f"Роль {role.name} снята с пользователя {member.name}."
"""

# We'll inject this before "except discord.Forbidden:"
mod_code = mod_code.replace("except discord.Forbidden:", new_exec_logic + "\n        except discord.Forbidden:")

with open("moderation.py", "w") as f:
    f.write(mod_code)

print("Updated moderation.py")
