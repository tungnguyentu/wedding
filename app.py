from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import hashlib
import json
import os

app = Flask(__name__)
# Enable CORS for all routes with proper configuration
CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True, "methods": ["GET", "POST", "OPTIONS"]}})

client = MongoClient(f"mongodb://localhost:27017/")
db = client["wedding"]
collection = db["rsvp"]

DATA = {
    "123ccc9e": "Chị   Thảo",
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
    "f9c9e7c7": "Tập   thể   nhóm   Tet's   Holiday",
    "aud92738": "Vợ   chồng   bạn   Tấm",
    '58c806': 'Bạn   Thơm',
    '61dc1b': 'Bạn   Nhàn',
    '349a34': 'Bạn   Thu',
    '34511c': 'Bạn   Phương',
    '66efb7': 'Bạn   Nga',
    '9a271f': 'Bạn   Quang',
    '566d7a': 'Bạn   Em   Minh',
    '065547': 'Bạn   Trần   Huyền',
    'f1b16b': 'Bạn   Phạm   Huyền',
    '997ac8': 'Bạn   Hướng',
    '3ad63a': 'Bạn   Thuỷ',
    '2cbdd2': 'Bạn   Đức',
    'aae030': 'Bạn   Hà   Huyền',
    'a5c3b5': 'Bạn   Na',
    '09d4c3': 'Bạn   Huệ',
    '104c8a': 'Bạn   Minh',
    '8e6cf9': 'Bạn   Lý'
}

DATA2 = {
    "05bf96": "anh   Huy",
    "075292": "anh   Khánh",
    "104086": "bạn   Hà",
    "1ffd70": "cô   Mai",
    "216375": "bạn   Nam",
    "25b356": "bạn   Tú",
    "26d5e7": "bạn   Thảo   Anh",
    "2a42f7": "bạn   Minh   Hoàng",
    "2a59c3": "bạn   Cường",
    "2d9a19": "anh   Duy",
    "36a8c2": "bạn   Long   và   người   thương",
    "38e3b2": "bạn   An",
    "3cb6da": "anh   Dũng",
    "4df6f4": "bạn   Kim   Long",
    "6344f3": "bạn   Quang   Hiếu",
    "64a279": "anh   Thắng",
    "6a33b4": "bạn   Thịnh   và   người   thương",
    "6e5a99": "chú   Hiếu",
    "6ed2db": "bạn   Quân",
    "8314cf": "chị   Trâm",
    "865980": "bạn   Châu",
    "873531": "bạn   Việt   Hoàng",
    "8b297c": "anh   Tùng   Anh",
    "a307c4": "bạn   Sơn   Tùng",
    "ace250": "bạn   Tất   Đạt",
    "add218": "bạn   Thuý",
    "afbeb2": "bạn   Bảo",
    "c1c6c9": "anh   Vinh",
    "cf8841": "bạn   Linh",
    "d88054": "bạn   Minh",
    "e0745f": "bạn   Minh   Hiếu",
    "e5a5df": "bạn   Huy   Hoàng",
    "eb1bb0": "bạn   Hoài   Anh",
    "eef286": "bạn   Phương   Tùng   và   người   thương",
    "f1f393": "Gia   đình   bạn   Ngọc   Quỳnh",
}


@app.route("/api/rsvp", methods=["POST", "OPTIONS"])
def rsvp():
    # Handle preflight OPTIONS requests
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    data = request.get_json()
    user_id = data.get("id")
    rsvp = data.get("rsvp")
    name = None
    
    if user_id in DATA:
        name = DATA[user_id]
    elif user_id in DATA2:
        name = DATA2[user_id]
    else:
        # Handle case when user ID is not found
        return jsonify({"error": "Invalid user ID"}), 400

    # Store in MongoDB
    if collection.find_one({"user_id": user_id}):
        collection.update_one({"user_id": user_id}, {"$set": {"rsvp": rsvp}})
    else:
        collection.insert_one({"user_id": user_id, "name": name, "rsvp": rsvp})

    return jsonify({"message": "RSVP received", "data": data}), 200


@app.route("/api/content", methods=["GET", "OPTIONS"])
def content():
    # Handle preflight OPTIONS requests
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    user_id = request.headers.get("X-User-ID")
    # Add debug logging
    app.logger.info(f"Received request for user_id: {user_id}")
    
    title = None
    location = None
    date = None
    timeline = None
    name = None
    
    if user_id in DATA:
        name = DATA[user_id]
        if name:
            title = "VÀO LÚC 17 GIỜ 00, THỨ HAI"
            location = "THÔN THƯỢNG LẠP - XÃ TÂN TIẾN - VĨNH TƯỜNG - VĨNH PHÚC"
            date = "25 . 11 . 2024"
            timeline = {
                "first": {"time": "17:00 ngày 25/11", "content": "Khai tiệc"},
                "second": {"time": "05:00 ngày 26/11", "content": "Lễ đính hôn"},
                "third": {"time": "06:00 ngày 26/11", "content": "Lễ rước dâu"},
            }
    elif user_id in DATA2:
        name = DATA2[user_id]
        # Add similar configuration for DATA2 users if needed

    response_data = {
        "name": name,
        "title": title,
        "location": location,
        "date": date,
        "timeline": timeline,
    }
    
    # Add debug logging
    app.logger.info(f"Sending response: {response_data}")
    
    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
