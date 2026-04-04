import os
from github import Github

token = os.environ.get("ACCESS_TOKEN") or os.environ.get("GITHUB_TOKEN")
g = Github(token)

user = g.get_user("kanakaero")

repos = user.get_repos()

stars = 0
forks = 0
total_size = {}
contributions = 0

for repo in repos:
    if repo.fork:
        continue
    stars += repo.stargazers_count
    forks += repo.forks_count

    langs = repo.get_languages()
    for k, v in langs.items():
        total_size[k] = total_size.get(k, 0) + v

# simple SVG output
os.makedirs("generated", exist_ok=True)

with open("generated/overview.svg", "w") as f:
    f.write(f"""
<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0d1117" rx="10"/>
  <text x="20" y="40" fill="#ff79c6" font-size="18">Kanak Agarwal's GitHub Stats</text>
  <text x="20" y="80" fill="#8be9fd">Stars: {stars}</text>
  <text x="20" y="110" fill="#8be9fd">Forks: {forks}</text>
</svg>
""")

with open("generated/languages.svg", "w") as f:
    y = 40
    content = ""
    for lang, size in sorted(total_size.items(), key=lambda x: -x[1])[:6]:
        content += f'<text x="20" y="{y}" fill="#8be9fd">{lang}</text>'
        y += 25

    f.write(f"""
<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0d1117" rx="10"/>
  <text x="20" y="20" fill="#ff79c6">Languages</text>
  {content}
</svg>
""")
