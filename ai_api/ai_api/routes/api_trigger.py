from workflow.interface import *
import json
from flask import current_app as app
from flask import request
from ai_api.decorators.login_required import login_required
from ai_api.response.response import Success, Failure
import sys
import os
import io
from pathlib import Path
from flask import Flask, render_template, request

current_path = os.path.dirname(os.path.abspath(__file__))
dti_path = str(Path(current_path).parent.parent.parent)


@app.route('/detect_emoji', methods = ['POST'])
#@login_required
def detect_emoji():
    try:
        emoji_input = request.form['emoji_input']
        print('Emoji Input: {0}'.format(emoji_input))
        emoji_image = detect_emotion(emoji_input)
        print('Emoji path: {0}'.format(emoji_image))

        return Success({'message':'Completed.', 'data': emoji_image})
    except Exception as error:
        return Failure({ 'message': str(error) }, debug = True )


@app.route("/upload_speech", methods=['POST'])
def upload_speech():
    try:
        if request.method == "POST":
            filepath = dti_path + '\\ai_engine\\data\\file.wav'
            audit_file = request.files["audio_data"]
            with open(filepath, 'wb') as audio:
                audit_file.save(audio)
            print('file uploaded successfully')

            emotion_results = process_speech(filepath)

            result = ''
            for emotion_result in emotion_results:
                result = result + emotion_result + ';'

        return Success({'message': 'Completed.', 'data': result})
    except Exception as error:
        return Failure({'message': str(error)}, debug=True)


@app.route("/", methods = ["POST"])
def choose_upload():
    try:
        if request.method == "POST":
            file = request.files["file"]
            file.save(os.path.join("ai_api",file.filename))

            emotion_results = process_speech('D:/IDE/PythonProject/emojidetect2/ai_api/ai_api/' + file.filename)

            result = ''
            for emotion_result in emotion_results:
                result = result + emotion_result + ';'

            if emotion_results[1] == 'weak sad':
                return render_template("weaksad.html", message="success")
            elif emotion_results[1] == 'mid sad':
                return render_template("midsad.html", message="success")
            elif emotion_results[1] == 'very sad':
                return render_template("verysad.html", message="success")
            elif emotion_results[1] == 'weak fear':
                return render_template("weakfear.html", message="success")
            elif emotion_results[1] == 'mid fear':
                return render_template("midfear.html", message="success")
            elif emotion_results[1] == 'very fear':
                return render_template("veryfear.html", message="success")


            #return Success({'message': 'Completed.', 'data': result})
            return render_template("result.html", message="success", )
            #return Success({'message': 'Completed.', 'data': result})

    except Exception as error:
        return Failure({'message': str(error)}, debug=True)



"""def process():
    emotion_results = process_speech('D:/IDE/PythonProject/emojidetect2/ai_api/ai_api/templates/' + file.filename)
    result = ''
    for emotion_result in emotion_results:
        result = result + emotion_result + ';'"""
