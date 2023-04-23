import os
import sys
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(ROOT, 'pages')
POSTS_DIR = os.path.join(ROOT, 'posts')
TEMPLATES_DIR = os.path.join(ROOT, 'templates')

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def get_pages():
    pages = []
    for page_name in os.listdir(PAGES_DIR):
        if page_name.endswith('.md'):
            with open(os.path.join(PAGES_DIR, page_name), 'r') as page_file:
                page_content = page_file.read()
                page_html = markdown.markdown(page_content)
                pages.append({
                    'name': page_name.replace('.md', ''),
                    'html': page_html
                })
    return pages

def get_posts():
    posts = []
    for post_name in os.listdir(POSTS_DIR):
        if post_name.endswith('.md'):
            with open(os.path.join(POSTS_DIR, post_name), 'r') as post_file:
                post_content = post_file.read()
                post_html = markdown.markdown(post_content)
                post_frontmatter = yaml.load(post_content.split('---')[1])
                post_date = post_frontmatter.get('date')
                posts.append({
                    'name': post_name.replace('.md', ''),
                    'html': post_html,
                    'date': post_date
                })
    return posts

