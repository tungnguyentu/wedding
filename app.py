from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to local MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wedding']
collection = db['rsvp']

DATA = {
    "6c0378bf": "Chị   Vân   thương   mến",
    "f47e16b2": "Gia   đình   cô   Tuyết   Nhung",
    "3e4a24c8": "Em   Đức",
    "78d74adf": "Gia   đình   bạn   Liên   và   anh   Đạt",
    "6ced8d11": "Bạn   Dung   Phạm",
    "014f0bba": "Bạn   Dung   Phùng",
    "d0ec341c": "Bạn   Yên   và   người   thương",
    "63c800b3": "Gia   đình   bạn   Thêu   và   anh   Tiệp",
    "0a068806": "Gia   đình   bạn   Thiết",
    "109afdcb": "Gia   đình   bạn   Giang",
    "b2f9a61b": "Bạn   Lâm",
    "e113a470": "Vợ   chồng   bạn   Cường",
    "219f3502": "Bạn   Hiếu",
    "e86f0587": "Vợ   chồng   bạn   Bích",
    "3170ff0f": "Gia   đình   bạn   Uyên",
    "3572aee8": "Gia   đình   bạn   Hảo",
    "60488be7": "Bạn   Cường   Phạm",
    "3e6a57ae": "Bạn   Nhi",
    "2c72a75e": "Vợ   chồng   bạn   Vân   Anh",
    "9a2a8e31": "Bạn   Vũ",
    "c44dd342": "Bạn   Được",
    "740b871f": "Bạn   Duy",
    "eab4b3eb": "Bạn   Diêu   Linh",
    "5aa1972f": "Bạn   Thoa",
    "04dfd939": "Gia   đình   bạn   Như   Quỳnh",
    "c0362cb3": "Gia   đình   bạn   Trang",
    "59125371": "Bạn   Hạ   Huyền",
    "a70f7a2c": "Bạn   Khánh   Linh",
    "ddbe11d9": "Bạn   Trang",
    "0b419cef": "Bạn   Huyền",
    "71f6ee14": "Bạn   Quỳnh   Anh",
    "dc018c09": "Bạn   Đông   xa nhớ",
    "5de3c419": "Bạn   Mai   và   người   thương",
    "2664438b": "Gia   đình   chị   Yến",
    "31ce1c48": "Chị   Phương   Anh",
    "b436824f": "Bạn   Hoa",
    "37ade819": "Gia   đình   anh   Hiếu",
    "5d669011": "Gia   đình   anh   Việt",
    "c1de670e": "Anh   Như",
    "be61d217": "Chị   Ngân",
    "d8638d0a": "Bạn   Uyên",
    "3cfd376f": "Gia   đình   chị   Linh",
    "d9990478": "Gia   đình   chị   Trâm",
    "d29c7a85": "Vợ   chồng   anh   Huy",
    "2b4b8b4a": "Bạn   Phan   Ánh",
}

@app.route('/api/rsvp', methods=['POST'])
def rsvp():
    data = request.get_json()
    user_id = data.get('id')
    rsvp = data.get('rsvp')
    if user_id not in DATA:
        return jsonify({'message': 'Invalid ID'}), 400
    name = DATA[user_id]
    if collection.find_one({'user_id': user_id}):
        collection.update_one({'user_id': user_id}, {'$set': {'rsvp': rsvp}})
    else:
        collection.insert_one({'user_id': user_id, 'name': name, 'rsvp': rsvp})
    return jsonify({'message': 'RSVP received', 'data': data}), 200


@app.route('/api/content', methods=['GET'])
def content():
    user_id = request.headers.get('X-User-ID')
    if user_id not in DATA:
        return jsonify({'message': 'Invalid ID'}), 400
    name = DATA[user_id]
    title = 'VÀO LÚC 17 GIỜ 00, THỨ HAI'
    location = 'THÔN THƯỢNG LẠP - XÃ TÂN TIẾN - VĨNH TƯỜNG - VĨNH PHÚC'
    date = '25 . 11 . 2024'
    timeline = {
        'first': {
            'time': '17:00 ngày 25/11',
            'content': 'Khai tiệc'
        },
        'second': {
            'time': '05:00 ngày 26/11',
            'content': 'Lễ đính hôn'
        },
        'third':{
            'time': '06:00 ngày 26/11',
            'content': 'Lễ rước dâu'
        }
    }
    return jsonify({
        'name': name,
        'title': title,
        'location': location,
        'date': date,
        'timeline': timeline
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)