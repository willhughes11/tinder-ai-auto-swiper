import json
from flask import Flask, request, abort, jsonify
import logging
from services.facial_recognition import FacialRecognition
fr = FacialRecognition()
from services.attractiveness_rating import Attractiveness_Rating
ar = Attractiveness_Rating()
from PIL import Image
import requests
import numpy as np
import validators
import base64
import binascii
from io import BytesIO
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'info': 'Image Rating API'})

@app.route('/rating', methods=['POST'])
def facial_rating_services():
    args = request.args
    data = request.get_json()

    if 'images' in data:
        images = data['images']
    else:
        images = None

    if data is None or images is None or len(images) == 0 or len(images) > 10:
        abort(422)
    elif type(data) is not dict or type(images) is not list:
        abort(422)
    else:
        if 'race' in args:
            preferred_race = args['race']
            preferred_race = eval(preferred_race)
            if preferred_race is None or len(preferred_race) == 0:
                preferred_race = []
            else:
                available_races = ["asian", "white", "middle eastern", "indian", "latino", "black"]
                check = any(item in preferred_race for item in available_races)

                if not check:
                    abort(400)
        else:
            preferred_race = []
        
        if 'rating' in args:
            min_rating = float(args['rating'])
            if min_rating < 0 or min_rating > 5:
                abort(400)
        else:
            min_rating = None
        
        all_faces = []
        for image in images:
            url = validators.url(image)
            try:
                if url:
                    im = Image.open(requests.get(image, stream=True).raw).convert('RGB')
                else:
                    try:
                        base64.b64decode(image, validate=True)
                        im = Image.open(BytesIO(base64.b64decode(image))).convert('RGB')
                    except binascii.Error:
                        abort(400)
            except:
                im = None

            if im:
                identified_faces = fr.identify_faces(im)
                all_faces.append(identified_faces)

        arr = []
        if len(all_faces) > 0:
            for i in all_faces:
                for x in i:
                    arr.append(x)

        if len(arr) > 0:
            compared_faces = fr.compare_faces(arr)
            if len(preferred_race) > 0:
                face_race = fr.analyze_images(compared_faces)
            else:
                face_race = None
            vertical = np.concatenate(compared_faces, axis=0)
            cv2.imwrite('image.png',vertical)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            if len(preferred_race) == 0 or face_race in preferred_race:
                ratings = ar.attractiveness_rating(compared_faces)
                avg_rating = float(np.average(ratings))
                if min_rating is None or avg_rating >= min_rating:
                    match = True
                else:
                    match = False
            else:
                avg_rating = float(0)
                match = False

            return jsonify({
                'race': face_race,
                'rating': avg_rating,
                'match': match
            }), 200
        
        else:
            return jsonify({
                'race': None,
                'rating': None,
                'match': False
            }), 200

#----------------------------------------------------------------------------#
# Error handlers
#----------------------------------------------------------------------------#
  
@app.errorhandler(400)
def bad_request(error):
  return jsonify({
    'success': False,
    'error': 400,
    'message':'bad request'
  }), 400

@app.errorhandler(404)
def not_found(error):
  return jsonify({
    'success': False,
    'error': 404,
    'message':'resource not found'
  }), 404

@app.errorhandler(405)
def not_allowed(error):
  return jsonify({
    'success': False,
    'error': 405,
    'message':'method not allowed'
  }), 405

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
    'success': False,
    'error': 422,
    'message':'unprocessable'
  }), 422

@app.errorhandler(500)
def server_error(error):
  return jsonify({
    'success': False,
    'error': 500,
    'message':'internal server error'
  }), 500

if not app.debug:
    file_handler = logging.FileHandler('error.log')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run()