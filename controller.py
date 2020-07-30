#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 27 July, 2020
"""
from flask import Flask, url_for, request, render_template, abort
app = Flask(__name__, static_folder="static")

## Import Model
import model

## Import database and static dir
from paths import db_path, static_path

@app.route('/')
def index():
    title, html = model.get_page('index')
    return render_template('page.html', title=title, html=html)

@app.route('/resume')
@app.route('/cv')
def resume():
    title, html = model.get_page('resume')
    return render_template('page.html', title=title, html=html)

@app.route('/blog')
@app.route('/projects')
def post_index():
    """ Blog index, shows all blog posts """
    title = "Blog Posts"

    ##
    posts = model.get_posts()

    ## Add paging here
    #=>
    return render_template('blog_index.html', title=title, posts=posts)

## post_id == title_id or page_id
@app.route('/<post_id>')
@app.route('/page/<post_id>', methods=['GET'])
def get_post(post_id):
    ## Get blog post contents
    post_data = model.get_page(post_id)
    
    ## If post doesn't exist, call 404
    if post_data == None:
        abort(404)

    ##
    title, html = post_data

    ## Returned rendered template
    return render_template('page.html', title=title, html=html)


@app.route('/add_page', methods=['POST'])
@app.route('/update_page/<title_id>', methods=['POST'])
def add_page(title_id=None):
    """
    Post method that adds a new page to database
    """
    ## Confirm args exist
    if 'auth' not in request.form:
        abort(401)
    if 'title' not in request.form:
        abort(406)
    if 'data' not in request.form:
        abort(406)
    
    ## Check token
    if not model.check_token(request.form['auth']):
        abort(401)


    if title_id: ## If flagged edit existing post
        title_id = model.update_page(title_id, request.form['title'], request.form['data'])

    else: ## Not flagged add new post
        page_id = model.add_page(request.form['title'], request.form['data'])

    ## Save all posted files to static dir
    files = request.files
    for filename in files:
        files[filename].save(f"{static_path}/{filename}")

    return "OK", 200



@app.errorhandler(404)
def http_404(error):
    return render_template('page.html', title="404 Not Found", html="<h1>404 Not Found</h1><hr><p>Sorry, page does not exist... <br>yet?</p>")