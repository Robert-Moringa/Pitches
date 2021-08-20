from flask import render_template, redirect, url_for,abort,request
from . import main
from .. import db, photos
from ..models import Downvote_Pitch, Upvote_Pitch, User,Pitch,Comment
from flask_login import login_required, current_user
from .form import UpdateProfile,PitchForm,CommentForm


@main.route('/')
def index():
    pitches = Pitch.query.all()
    business = Pitch.query.filter_by(category = 'Business').all() 
    leadership = Pitch.query.filter_by(category = 'Leadership').all()
    environment = Pitch.query.filter_by(category = 'Environment').all()
    title= 'Welcome to your one stop Pitches Website'
    return render_template('index.html', title = title, pitches= pitches, business = business, leadership=leadership, environment=environment)

@main.route('/about')
def about():
    tittle = 'About Myners Pitches'
    return render_template('about.html', tittle = tittle)


@main.route('/add_pitch', methods = ['POST','GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_pitch_object = Pitch(post=post, user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_pitch()
        return redirect(url_for('main.index'))
        
    return render_template('add_pitch.html', form = form)

@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def add_comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.add_coment()
        return redirect(url_for('.add_comment', pitch_id = pitch_id))
    return render_template('comment_pitch.html', comment_form =form, pitch = pitch, all_comments=all_comments)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id
    posts = Pitch.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)


@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_profile_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))


@main.route('/upvote/<int:id>',methods = ['POST','GET'])
@login_required
def upvote(id):
    get_pitches = Upvote_Pitch.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote_Pitch(user = current_user, pitch_id=id)
    new_vote.save_upvote()
    return redirect(url_for('main.index',id=id))


@main.route('/downvote/<int:id>',methods = ['POST','GET'])
@login_required
def downvote(id):
    pitch = Downvote_Pitch.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote_Pitch(user = current_user, pitch_id=id)
    new_downvote.save_downvote()
    return redirect(url_for('main.index',id = id))
