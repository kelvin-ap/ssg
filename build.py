import os
import markdown
from jinja2 import Environment, FileSystemLoader
import yaml
from datetime import datetime

# Stel de paden in
TEMPLATES_DIR = "./templates"
PAGES_DIR = "./pages"
POSTS_DIR = "./posts"
OUTPUT_DIR = "./docs"

# Maak een Jinja2 omgeving
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
env.filters["date"] = datetime.strptime

# Lijst van pagina's en posts om te genereren
pages = []
fm_pages = []
posts = []
fm_posts = []

# Loop door alle bestanden in de 'posts' map
for filename in os.listdir(POSTS_DIR):

    # Zorg ervoor dat het een Markdown-bestand is
    if filename.endswith(".md"):

        # Open het bestand en lees de inhoud
        with open(os.path.join(POSTS_DIR, filename), "r") as file:
            content = file.read()

        # Parse de front matter en de inhoud
        front_matter, markdown_content = content.split("---")[1:]

        # Parse de YAML en sla de waarden op als variabelen
        variables = yaml.safe_load(front_matter)
        fm_posts.append(variables)

        # Converteer de inhoud van Markdown naar HTML
        html_content = markdown.markdown(markdown_content)
        
        # Kies het juiste template voor de pagina
        template = env.get_template(variables.get("template", "post.html"))

        # Maak een nieuwe HTML-string met behulp van de template en de variabelen
        html_output = template.render(title=variables.get("title"), paginas=fm_pages, content=html_content, post=fm_posts)

        # Bepaal het uitvoerbestand voor de pagina
        output_file = os.path.join(OUTPUT_DIR, filename.replace(".md", ".html"))

        # Als het de startpagina is, sla deze op als 'index.html'
        if variables.get("url") == "/":
            output_file = os.path.join(OUTPUT_DIR, "index.html")

        # Voeg de pagina toe aan de lijst van pagina's om te genereren
        posts.append((output_file, html_output))

# Loop door alle bestanden in de 'pages' map
for filename in os.listdir(PAGES_DIR):

    if filename.endswith(".md"):

        with open(os.path.join(PAGES_DIR, filename), "r") as file:
            content = file.read()

        front_matter, markdown_content = content.split("---")[1:]

        variables = yaml.safe_load(front_matter)
        fm_pages.append(variables)

        html_content = markdown.markdown(markdown_content)

        template = env.get_template(variables.get("template", "page.html"))

        html_output = template.render(title=variables.get("title"), content=html_content, pages=fm_pages, posts=fm_posts)

        output_file = os.path.join(OUTPUT_DIR, filename.replace(".md", ".html"))

        if variables.get("url") == "/":
            output_file = os.path.join(OUTPUT_DIR, "index.html")

        pages.append((output_file, html_output))

# Maak de output directory aan als deze nog niet bestaat
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Schrijf de HTML-bestanden
for output_file, html_output in pages:
    with open(output_file, "w") as file:
        file.write(html_output)

for output_file, html_output in posts:
    with open(output_file, "w") as file:
        file.write(html_output)



# def generate_posts():
#     # Lijst van posts om te genereren
#     posts = []
#     fm_posts = []

#     # Loop door alle bestanden in de 'posts' map
#     for filename in os.listdir(POSTS_DIR):

#         # Zorg ervoor dat het een Markdown-bestand is
#         if filename.endswith(".md"):

#             # Open het bestand en lees de inhoud
#             with open(os.path.join(POSTS_DIR, filename), "r") as file:
#                 content = file.read()

#             # Parse de front matter en de inhoud
#             front_matter, markdown_content = content.split("---")[1:]

#             # Parse de YAML en sla de waarden op als variabelen
#             variables = yaml.safe_load(front_matter)
#             fm_posts.append(variables)

#             # Converteer de inhoud van Markdown naar HTML
#             html_content = markdown.markdown(markdown_content)

#             # Kies het juiste template voor de pagina
#             template = env.get_template(variables.get("template", "post.html"))

#             # Maak een nieuwe HTML-string met behulp van de template en de variabelen
#             html_output = template.render(title=variables.get("title"), content=html_content, post=fm_posts)

#             # Bepaal het uitvoerbestand voor de pagina
#             output_file = os.path.join(OUTPUT_DIR, filename.replace(".md", ".html"))

#             # Als het de startpagina is, sla deze op als 'index.html'
#             if variables.get("url") == "/":
#                 output_file = os.path.join(OUTPUT_DIR, "index.html")

#             # Voeg de pagina toe aan de lijst van pagina's om te genereren
#             posts.append((output_file, html_output))

#     return posts

# #momenteel blijkt generate_posts output oke te zijn, fout zit elders

# def generate_pages(posts):
#     # Lijst van pagina's om te genereren
#     pages = []
#     fm_pages = []

#     # Loop through all files in the 'pages' directory
#     for filename in os.listdir(PAGES_DIR):
#         # Check if file is a Markdown file
#         if filename.endswith(".md"):
#             # Read the file content
#             with open(os.path.join(PAGES_DIR, filename), "r") as file:
#                 content = file.read()

#             # Split front matter and Markdown content
#             front_matter, markdown_content = content.split("---")[1:]

#             # Load front matter variables from YAML
#             variables = yaml.safe_load(front_matter)
#             fm_pages.append(variables)

#             # Convert Markdown content to HTML
#             html_content = markdown.markdown(markdown_content)

#             # Load page template and render HTML output
#             template = env.get_template(variables.get("template", "page.html"))
#             html_output = template.render(title=variables.get("title"), content=html_content, pages=fm_pages, posts=posts)

#             # Set output file name
#             output_file = os.path.join(OUTPUT_DIR, filename.replace(".md", ".html"))
#             if variables.get("url") == "/":
#                 output_file = os.path.join(OUTPUT_DIR, "index.html")

#             # Add output file and HTML content to pages list
#             pages.append((output_file, html_output))

#     # Return the pages list
#     return pages

# def build():
#     # Genereer posts en pagina's
#     posts = generate_posts()
#     pages = generate_pages(posts)

#     # Maak de output directory aan als deze nog niet bestaat
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)

#     # Schrijf de HTML-bestanden
#     for output_file, html_output in pages:
#         with open(output_file, "w") as file:
#             file.write(html_output)
    
#     for output_file, html_output in posts:
#         with open(output_file, "w") as file:
#             file.write(html_output)

# if __name__ == '__main__':
#     build()