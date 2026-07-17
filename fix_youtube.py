# Add yt-dlp to requirements
with open("requirements.txt", "a") as f:
    f.write("\nyt-dlp>=2023.11.16\nPyNaCl>=1.5.0\n")

print("Added yt-dlp to requirements")
