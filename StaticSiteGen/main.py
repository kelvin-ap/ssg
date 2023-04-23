import os

# Maak de "_site" map aan als die nog niet bestaat
if not os.path.exists('_site'):
    os.makedirs('_site')

# Loop door de bestanden in de "pages" map en kopieer ze naar "_site"
for filename in os.listdir('pages'):
    with open(f'pages/{filename}', 'r') as file:
        content = file.read()
    with open(f'_site/{filename}', 'w') as file:
        file.write(content)
