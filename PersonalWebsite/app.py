from flask import Flask, render_template, url_for
import markdown
import os
import yaml

app = Flask(__name__)
ARTICLES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'articles')
print(ARTICLES_FOLDER)

class Article:
    def __init__(self, id, title, summary, content):
        self.id = id
        self.title = title
        self.summary = summary
        self.content = content

def load_articles():
    articles = []
    for file_name in os.listdir(ARTICLES_FOLDER):
        if file_name.endswith('.md'):
            with open(os.path.join(ARTICLES_FOLDER, file_name), 'r', encoding='utf-8') as f:
                content = f.read()
                metadata, body = content.split('---\n', 1)
                metadata = yaml.safe_load(metadata)
                article_id = os.path.splitext(file_name)[0]
                article = {
                    'id': article_id,
                    'title': metadata['title'],
                    'summary': metadata['summary'],
                    'body': markdown.markdown(body)
                }
                articles.append(article)
    # Add these print statements
    print("Article folder:", ARTICLES_FOLDER)
    print("Files in the article folder:", os.listdir(ARTICLES_FOLDER))
    print("Processed articles:", articles)
    return articles


@app.route('/')
def about():
    return render_template('index.html')

@app.route('/blog')
def blog():
    articles = load_articles()
    print("Loaded articles:", articles)  # Add this line to print loaded articles
    return render_template('blog.html', articles=articles)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/article/<article_id>')
def view_article(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == article_id), None)
    if article:
        return render_template('viewArticle.html', article=article)
    else:
        return "Article not found", 404

if __name__ == '__main__':
    app.run(debug=True)
