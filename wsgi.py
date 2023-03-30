import sys
sys.path.append('./modules')
if True:  # noqa: E402
    import os
    from dotenv import load_dotenv
    import fileChecker as fc
    import modelTrainer as mt
    import knowledgeEntry as ke
    import helpers as h
    from flask import Flask, request, Response
    from http import HTTPStatus
    import json
    import pydub

load_dotenv()

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=os.getenv(key='PORT', default=5001),
            host=os.getenv(key='HOST', default='localhost'))


class Data:
    def __init__(self, data, message):
        self.data = data
        self.message = message


def responseFormat(data, status, message):
    return Response(json.dumps({'data': data, 'message': message}), status=status, mimetype='application/json')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            for file in os.listdir(os.getenv('TEMP_FILE_PATH')):
                if not file.endswith('.dat'):
                    os.remove(os.path.join(os.getenv('TEMP_FILE_PATH'), file))

            audioStream = request.files['audio']
            audioStreamPath = f"{os.getenv('TEMP_FILE_PATH')}/{audioStream.filename}"
            audioStream.save(audioStreamPath)

            with open(os.getenv('TEMP_FILE_PATH') + '/audioName.txt', 'w') as audioNameWriter:
                audioNameWriter.write(audioStream.filename.split('.')[0])

            fc.getWavFile(audioStreamPath, os.getenv('CONVERTED_FILE_PATH'))

            os.remove(audioStreamPath)
            prediction = mt.getPrediction(
                os.getenv('CONVERTED_FILE_PATH'),
                fc.loadDataset(os.getenv('DATASET_PATH')),
                int(os.getenv('K')),
                os.getenv('GENRES_FILE_PATH')
            )
        except FileNotFoundError:
            return responseFormat(None, HTTPStatus.NOT_FOUND, 'No file found in the temp folder. Please upload a file first.')
        except KeyError:
            return responseFormat(None, HTTPStatus.BAD_REQUEST, 'No file found in request input named "audio". Please check your request body and try again.')
        except pydub.exceptions.CouldntDecodeError as e:
            return responseFormat(None, HTTPStatus.BAD_REQUEST, f'The file provided is not a valid audio file. Error: {e}')
        except Exception as e:
            return responseFormat(None, HTTPStatus.INTERNAL_SERVER_ERROR, f'An error has occurred while trying to predict genre. Error: {e}')
    return responseFormat(prediction, HTTPStatus.OK, 'Prediction made successfully')


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        try:
            # get file name from temp/audioName.txt
            with open(os.getenv('TEMP_FILE_PATH') + '/audioName.txt', 'r') as audioNameReader:
                name = audioNameReader.read()
            genre = request.form['genre']
            audioPath = f"{os.getenv('GENRES_PATH')}/{genre}/{name}.wav"

            with open(os.getenv('CONVERTED_FILE_PATH'), 'rb') as audioReader:
                data = audioReader.read()
                with open(audioPath, 'wb') as audioWriter:
                    audioWriter.write(data)

            genres = h.getGenres(os.getenv('GENRES_FILE_PATH'))
            genreId = list(genres.keys())[list(genres.values()).index(genre)]

            ke.insertToDataset(os.getenv('DATASET_PATH'), audioPath, genreId)
        except FileNotFoundError:
            return responseFormat(None, HTTPStatus.NOT_FOUND, 'No file found in the temp folder. Please upload a file first.')
        except Exception as e:
            return responseFormat(None, HTTPStatus.INTERNAL_SERVER_ERROR, f'An error has occurred while trying to insert file in the dataset. Error: {e}')
    return responseFormat(None, HTTPStatus.OK, 'Data inserted successfully')


@app.route('/dataset/create', methods=['GET'])
def create_dataset():
    if request.method == 'GET':
        try:
            ke.createDataset(os.getenv('DATASET_PATH'), os.getenv(
                'GENRES_PATH'), os.getenv('GENRES_FILE_PATH'))
        except Exception as e:
            return responseFormat(None, HTTPStatus.INTERNAL_SERVER_ERROR, f'An error has occurred while trying to create the dataset. Error: {e}')
    return responseFormat(None, HTTPStatus.OK, 'Dataset created successfully')


@app.route('/genres', methods=['GET'])
def get_genres():
    if request.method == 'GET':
        try:
            genres = list(h.getGenres(os.getenv('GENRES_FILE_PATH')).values())
        except Exception as e:
            return responseFormat(None, HTTPStatus.INTERNAL_SERVER_ERROR, f'An error has occurred while trying to get genres. Error: {e}')
    return responseFormat(genres, HTTPStatus.OK, 'Genres retrieved successfully')
