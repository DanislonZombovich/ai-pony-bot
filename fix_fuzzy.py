with open("moderation.py", "r") as f:
    code = f.read()

# Update tool descriptions to remove strict requirement on exact name
code = code.replace(
    'description="Add a role to a user. You must provide the exact role name or ID."',
    'description="Add a role to a user. You can provide an approximate role name or ID."'
)
code = code.replace(
    'description="Remove a role from a user. You must provide the exact role name or ID."',
    'description="Remove a role from a user. You can provide an approximate role name or ID, or say \'all\' to remove all roles."'
)

code = code.replace(
    'description="The exact name of the role to add."',
    'description="The approximate name of the role to add."'
)
code = code.replace(
    'description="The exact name of the role to remove."',
    'description="The approximate name of the role to remove, or \'all\'."'
)

# We also need a fuzzy match logic
fuzzy_logic = """
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
"""

code = code.replace("class ModerationHandler:", fuzzy_logic + "\nclass ModerationHandler:")

# Replace execution logic for add_role / remove_role
add_exec = """
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
"""

import re
import sys

# Replace the old logic
code = re.sub(
    r'elif call.name == "add_role":.*?return f"Роль \{role.name\} снята с пользователя \{member.name\}\."',
    add_exec.strip(),
    code,
    flags=re.DOTALL
)

with open("moderation.py", "w") as f:
    f.write(code)

print("Updated moderation.py with fuzzy matching")
