"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "12345"

connect_db(app)

# Looked this up, runtime errors
# with app.app_context():
#     db.create_all()

@app.route('/')
def redirect_me():
  """Redirect to list of users"""
  return redirect('/users')

@app.route('/users')
def list_users():
  """Show list of all users in db"""
  users = User.query.all()
  return render_template('list.html', users=users)

@app.route('/users/new')
def show_form():
  """Show an add form for users"""
  return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
  """Create and add new user to the database"""
  fname = request.form["first_name"]
  lname = request.form["last_name"]
  url = request.form["img_url"]

  new_user = User(first_name=fname, last_name=lname, image_url=url)

  with app.app_context():
    db.session.add(new_user)
    db.session.commit()
  
  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
  """Show details about a user"""
  user = User.query.get_or_404(user_id)
  posts = Post.query.all()
  return render_template("details.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
  """Shows the edit page for a user"""
  user = User.query.get_or_404(user_id)
  return render_template("edit_form.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
  """Process the edit form, return to the users page"""
  user = User.query.get_or_404(user_id)
  first = request.form["first_name"]
  last = request.form["last_name"]
  url = request.form["img_url"]

  # Need to do it in model to avoid error
  user.edit(first, last, url)
  
  return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
  """Delete the user"""
  user = User.query.get(user_id)
  # Needed to do it in the model to avoid calling multiple db sessions
  user.remove()
  
  return redirect('/users')

# Routes for posts below
# ----------------------

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
  """Show form to add post"""
  user = User.query.get(user_id)
  tags = Tag.query.all()
  return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
  """Create and add new post to the database"""
  title = request.form["title"]
  content = request.form["content"]
  tags = request.form.getlist('tag')

  # Get selected tags from the db
  tags_list = []
  for tag in tags:
    t = Tag.query.filter(Tag.name == tag).first()
    tags_list.append(PostTag(tag_id = t.id))

  # Put all data into a new post item then commit it
  new_post = Post(title=title, content=content, user_id=user_id, tags=tags_list)

  with app.app_context():
    db.session.add(new_post)
    db.session.commit()
  
  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
  """Show a post w/ buttons to edit and delete"""
  post = Post.query.get_or_404(post_id)
  user = post.user
  pt = post.tags
  tags = []
  for tag in pt:
    tags.append(Tag.query.get(tag.tag_id))
  return render_template("post_details.html", post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
  """Shows the edit page for a user"""
  post = Post.query.get_or_404(post_id)
  tags = Tag.query.all()
  return render_template("edit_post_form.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
  """Process the edit form, return to the post view"""
  post = Post.query.get_or_404(post_id)
  title = request.form["title"]
  content = request.form["content"]
  tags = request.form.getlist('tag')

  # Get selected tags from the db
  tags_list = []
  for tag in tags:
    t = Tag.query.filter(Tag.name == tag).first()
    tags_list.append(PostTag(tag_id = t.id, post_id = post_id))

  # Need to do it in model to avoid error
  post.edit(title, content, tags_list)
  
  return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
  """Delete the post"""
  post = Post.query.get(post_id)
  # Needed to do it in the model to avoid calling multiple db sessions
  post.remove()
  
  return redirect('/users')

# Routes for tags below
# ---------------------

@app.route('/tags')
def show_tags():
  """List all tags, with links to the tag detail page"""
  tags = Tag.query.all()
  return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def detail_tag(tag_id):
  """Show detail about a tag"""
  tag = Tag.query.get_or_404(tag_id)
  return render_template("tag_details.html", tag=tag)

@app.route('/tags/new')
def show_tags_form():
  """Shows a form to add a new tag"""
  return render_template("tag_form.html")

@app.route('/tags/new', methods=["POST"])
def create_tag():
  """Process add form, adds tag, and redirect to tag list"""
  name = request.form["name"]
  new_tag = Tag(name=name)

  with app.app_context():
    db.session.add(new_tag)
    db.session.commit()
  
  return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
  """Show edit form for a tag"""
  tag = Tag.query.get_or_404(tag_id)
  return render_template("edit_tag_form.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
  """Process edit form, edit tag, and redirects to the tags list."""
  tag = Tag.query.get_or_404(tag_id)
  name = request.form["name"]

  # Need to do it in model to avoid error
  tag.edit(name)
  
  return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
  """Delete a tag"""
  tag = Tag.query.get(tag_id)
  # Needed to do it in the model to avoid calling multiple db sessions
  tag.remove()
  
  return redirect('/tags')