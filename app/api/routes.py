from flask import current_app
from werkzeug.utils import secure_filename
import os
from flask import Flask, Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Image, image_schema, images_schema

#api = Blueprint('api',__name__, url_prefix='/api')
api = Blueprint('api',__name__, url_prefix='/api')

#test API
@api.route('/getdata')
def getdata():
    return {'test': 'testgalleryapi'}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Add A Image
@api.route('/images', methods=['POST'])
@token_required
def create_image(current_user_token):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        image_title = request.form.get('image_title', '')
        image_url = filepath  # Now it points to an actual file
        creator_name = request.form.get('creator_name', '')
        no_of_downloads = int(request.form.get('no_of_downloads', 0))
        image_type = request.form.get('image_type', '')
        user_token = current_user_token.token

        # Check if the User Token Exists
        user = User.query.filter_by(token=user_token).first()

        # Insert User if Not Present
        if user is None:
            new_user = User(token=user_token)
            db.session.add(new_user)
            db.session.commit()

        # Insert Image Record
        image = Image(image_title, image_url, creator_name, no_of_downloads, image_type, user_token=user_token)
        db.session.add(image)
        db.session.commit()

        response = image_schema.dump(image)
        return jsonify(response)


#Get List of Images
@api.route('/images', methods = ['GET'])
@token_required
def get_image(current_user_token):
    a_user = current_user_token.token
    images = Image.query.filter_by(user_token = a_user).all()
    response = images_schema.dump(images)
    return jsonify(response)

#get details of sepcific image
@api.route('/images/<id>', methods = ['GET'])
@token_required
def get_single_image(current_user_token, id):    # Currently showing cars of other users as well 
    image = Image.query.get(id)
    response = image_schema.dump(image)
    return jsonify(response)


#Update Image details
@api.route('/images/<id>', methods = ['POST','PUT'])
@token_required
def update_image(current_user_token,id):
    image = Image.query.get(id) 
    image.image_title = request.json['image_title']
    image.image_url = request.json['image_url']
    image.creator_name = request.json['creator_name']
    image.no_of_downloads = request.json['no_of_downloads']
    image.image_type = request.json['image_type']
    image.user_token = current_user_token.token

    db.session.commit()
    response = image_schema.dump(image)
    return jsonify(response)

# Delete Specific Image
@api.route('/images/<id>', methods = ['DELETE'])
@token_required
def delete_image(current_user_token, id):
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()
    response = image_schema.dump(image)
    return jsonify(response)

