#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 27 July, 2020
"""
from flask import Flask, url_for, request, render_template
app = Flask(__name__, static_folder="static")

import model

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
    title = "Blog Posts"

    ##
    posts = model.get_posts()

    ## Add paging here
    #=>
    return render_template('blog_index.html', title=title, posts=posts)


@app.route('/<post_id>')
@app.route('/page/<post_id>', methods=['GET'])
def get_post(post_id):
    ## Get blog post contents
    post_data = model.get_page(post_id)
    
    ## If post doesn't exist, call 404
    if post_data == None:
        return '404', 404

    ##
    title, html = post_data

    ## Returned rendered template
    return render_template('page.html', title=title, html=html)


@app.route('/add_page', methods=['POST'])
@app.route('/page/<page_id>', methods=['POST'])
def add_page(page_id=None):
    """
    Post method that adds a new page to database
    """
    print(page_id)
    ## Confirm args exist
    if 'auth' not in request.form:
        return 'error'
    if 'title' not in request.form:
        return 'error'
    if 'data' not in request.form:
        return 'error'
    
    ## Check token
    if not model.check_token(request.form['auth']):
        return "Auth Error"

    ## Add New page to DB
    if page_id: ## If flagged edit existing post
        model.update_page(page_id, request.form['title'], request.form['data'])
    else: ## Not flagged add new post
        page_id = model.add_page(request.form['title'], request.form['data'])

    ## Save all posted files to static dir
    files = request.files
    for filename in files:
        files[filename].save(f"./static/{filename}")

    return page_id, 200
