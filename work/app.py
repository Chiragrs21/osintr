from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
import asyncio
import bcrypt
import jwt
from datetime import datetime
from api4 import ipv6_location
from api5 import certificates
from api6 import check_domain
from read import url_results
import pandas as pd
from api7 import email_reader
from api8 import email_social_media
from api9 import email_verification
from api10 import ip_verification
from api11 import domain_search
from api12 import domain_email_search
from api13 import ip4_geolocator
from api14 import phone_lookup
import ipaddress

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'wedbjviu2e'
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase2']


async def scan_url_async(url):
    return await url_results(url)

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")


@app.route('/export_data', methods=['GET'])
def export_data():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = list(db[username].find({}, {'_id': 0}))

    if not data:
        return jsonify({'error': 'No data found'}), 404

    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)

    response = Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=data.csv"}
    )

    return response


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if db.users.find_one({'username': username}):
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    db.users.insert_one({'username': username, 'password': hashed_password})
    db.create_collection(username)

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db.users.find_one({'username': username})
    if not user or not bcrypt.checkpw(password.encode(), user['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = jwt.encode({'username': username},
                       app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200


def verify_token(token):
    try:
        data = jwt.decode(
            token.split()[1], app.config['SECRET_KEY'], algorithms=['HS256'])
        return data.get('username')
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except (jwt.InvalidTokenError, IndexError):
        return None


@app.route('/url_scanner', methods=['POST'])
def scan_url():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = request.get_json()
    url = data.get('url')
    name = data.get('name')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    results = asyncio.run(scan_url_async(url))
    results2 = certificates(url)
    results3 = check_domain(url)
    results4 = domain_search(url)
    form_data = {
        'name': name,
        'query': url,
        'status': 'completed',
        "date": formatted_datetime,
        'json_data': results,
        'certificates': results2,
        "check": results3,
        "domain_search": results4
    }
    db[username].insert_one(form_data)
    return jsonify(results)


# Email
@app.route('/email', methods=['POST'])
def Email_id():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = request.get_json()
    email = data.get('url')
    name = data.get('name')

    if not email:
        return jsonify({'error': 'No email provided'}), 400

    results = email_reader(email)
    results2 = email_social_media(email)
    result3 = email_verification(email)
    result4 = domain_email_search(email)

    form_data = {
        'name': name,
        'query': email,
        'status': 'completed',
        "date": formatted_datetime,
        'json_data': results,
        'social_media': results2,
        'verification': result3,
        'domains': result4
    }
    db[username].insert_one(form_data)
    return jsonify(results)


@app.route('/ip6_location', methods=['POST'])
def ipv6_location1():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = request.get_json()
    url = data.get('url')
    name = data.get('name')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    is_ipv4 = ipaddress.ip_address(url).version == 4 if '.' in url else False
    is_ipv6 = ipaddress.ip_address(url).version == 6 if ':' in url else False

    if (is_ipv6):
        results = ipv6_location(url)
        results1 = ip_verification(url)
    else:
        results = ip4_geolocator(url)
        results1 = ip_verification(url)

    form_data = {
        'name': name,
        'query': url,
        'status': 'completed',
        "date": formatted_datetime,
        'json_data': results,
        'verify': results1
    }

    db[username].insert_one(form_data)
    return jsonify(results)


@app.route('/phn_location', methods=['POST'])
def phn_location1():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = request.get_json()
    url = data.get('url')
    name = data.get('name')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    results = phone_lookup(url)

    form_data = {
        'name': name,
        'query': url,
        'status': 'completed',
        "date": formatted_datetime,
        'json_data': results
    }

    db[username].insert_one(form_data)
    return jsonify(results)


@app.route('/get_data', methods=['GET'])
def get_data():
    token = request.headers.get('Authorization')
    username = verify_token(token)
    print(username)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = list(db[username].find({}, {'_id': 0}))
    return jsonify(data)


@app.route('/get_data_by_name/<name>', methods=['GET'])
def get_data_by_name(name):
    token = request.headers.get('Authorization')
    username = verify_token(token)
    if not username:
        return jsonify({'error': 'Invalid or expired token'}), 401

    data = db[username].find_one({'name': name}, {'_id': 0})
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
