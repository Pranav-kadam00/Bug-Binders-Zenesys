import re

with open('artifacts/aqura/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<<<<<<< Updated upstream\n(.*?)\n=======\n.*?\n>>>>>>> Stashed changes', r'\1', content, flags=re.DOTALL)

with open('artifacts/aqura/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
