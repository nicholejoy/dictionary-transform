import simplejson as json
from flask import Flask, request
import dictionary_transform
import bcrypt
from dictionary_db import DictionaryDB
from flask_httpauth import HTTPBasicAuth

DictionaryDB.create_db()
app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route('/output', methods=['GET'])
@auth.login_required
def get_data():
    data = DictionaryDB.get_dictionary_data(auth.current_user(), 'nested')
    return data, 200


@app.route('/input', methods=['POST'])
@auth.login_required
def upload_data():
    try:
        json_data = json.loads(request.files["file"].read())
    except json.errors.JSONDecodeError:
        return {"Error": "Incorrect input given. JSON Expected."}, 200
    DictionaryDB.insert_dictionary_data(auth.current_user(), 'raw', json_data)
    return {"Success": "Data Uploaded."}, 200


@app.route('/transform', methods=['POST'])
@auth.login_required
def create_dict():
    user_data = request.get_json()
    try:
        levels = user_data['levels']
    except KeyError:
        return {"Error": "Require at least one nesting level 0 given."}, 400
    output_dict = dictionary_transform.NestedDict(levels)
    data = DictionaryDB.get_dictionary_data(auth.current_user(), 'raw')
    if not data:
        return {"Error": "Input data not available. Upload data."}, 400
    output_dict.set_data(data)
    output_dict.parse_rows()
    DictionaryDB.insert_dictionary_data(auth.current_user(), 'dictionary_transform', output_dict.get_data())
    return {"Success": "Nested dictionary created."}, 201


@auth.verify_password
def verify_password(username, password):
    if DictionaryDB.is_user(username):
        if bcrypt.checkpw(password.encode('utf-8'), DictionaryDB.get_hashed_pw(username)["password"]):
            return username


@app.errorhandler(dictionary_transform.NestedException)
def handle_nested_exception(error):
    return {"Error": error.text}, error.code


@app.errorhandler(Exception)
def handle_generic_exception(error):
    return {"Error": str(error)}, error.code


if __name__ == '__main__':
    app.run(debug=True)
