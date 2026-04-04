import os
from github import Github, Auth

# --- Auth ---
token = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
g = Github(auth=Auth.Token(token))

# --- User ---
user = g.get_user("kanakaero")
repos = user.get_repos()

# --- Stats ---
stars = 0
forks = 0
total_size = {}

for repo in repos:
    if repo.fork:
        continue

    stars += repo.stargazers_count
    forks += repo.forks_count

    # languages
    langs = repo.get_languages()
    for k, v in langs.items():
        try:
            total_size[k] = total_size.get(k, 0) + int(v)
        except:
            continue

# --- Ensure output dir ---
os.makedirs("generated", exist_ok=True)

# --- Overview SVG ---
with open("generated/overview.svg", "w") as f:
    f.write(f"""
<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ fill: #ff79c6; font-size: 18px; font-family: monospace; }}
    .text {{ fill: #8be9fd; font-size: 14px; font-family: monospace; }}
  </style>

  <rect width="100%" height="100%" fill="#0d1117" rx="10"/>

  <text x="20" y="40" class="title">Kanak Agarwal's GitHub Stats</text>

  <text x="20" y="80" class="text">★ Stars: {stars}</text>
  <text x="20" y="110" class="text">⑂ Forks: {forks}</text>
</svg>
""")

# --- Languages SVG ---
sorted_langs = sorted(total_size.items(), key=lambda x: -x[1])[:6]

with open("generated/languages.svg", "w") as f:
    y = 50
    content = ""

    for lang, size in sorted_langs:
        content += f'<text x="20" y="{y}" fill="#8be9fd" font-size="14" font-family="monospace">{lang}</text>'
        y += 25

    f.write(f"""
<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ fill: #ff79c6; font-size: 18px; font-family: monospace; }}
  </style>

  <rect width="100%" height="100%" fill="#0d1117" rx="10"/>

  <text x="20" y="30" class="title">Languages</text>

  {content}
</svg>
""")
