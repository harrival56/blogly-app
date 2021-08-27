from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql.functions import user
from models import db, connect_db, User, Post, PostTag, Tag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://:5433/blogly2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "harrison"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)



@app.route('/')
def list_users():
    """shows list os users in db"""
    users = User.query.all()
    return render_template('list_user.html', users=users)

@app.route("/add_user")
def new_user_form():

    return render_template('new_user.html')

@app.route('/', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    position = request.form["position"]
    origin = request.form["origin"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url, position=position, c_of_origin=origin)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/{new_user.id}")

@app.route('/delete/<int:user_id>', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

@app.route('/edit/<int:user_id>')
def edit_(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/edit/<int:user_id>/go', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    user.position = request.form["position"]
    user.c_of_origin = request.form["origin"]
    db.session.add(user)
    db.session.commit()
    return redirect(f"/{user.id}")

@app.route('/<int:user_id>')
def show_user(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("detail.html", user=user, tags=tags)


@app.route('/<int:user>/post', methods=["POST"])
def new_post(user):
    user = User.query.get_or_404(user)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'], content=request.form['content'], user=user, hashtag=tags)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/{user}")

@app.route('/<int:user_id>/<int:post_id>')
def post_detail(user_id, post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)


@app.route("/<user_id>/<post_id>", methods=["POST"])
def updated_post(user_id, post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content =request.form["content"]
    db.session.add(post)
    db.session.commit()
    return redirect(f"/{user_id}/{post_id}")


@app.route('/<int:user_id>/delete/<int:post_id>', methods=["POST"])
def delete_post(user_id, post_id):
    del_post = Post.query.get(post_id)
    db.session.delete(del_post)
    db.session.commit()
    return redirect(f"/{user_id}")

@app.route("/<int:user_id>/add_tag", methods=["POST"])
def add_tag(user_id):
    name = request.form["create_tag"]
    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(f"/{user_id}")


@app.route("/tag/<int:tag_id>")
def show_tags(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template("tag_and_post.html", tag=tag)

@app.route("/edit/<int:tag_id>", methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form["edit_tag_form"]
    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tag/{tag_id}")