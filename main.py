from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)


app.config['STATIC_FOLDER'] = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.config['STATIC_FOLDER'], 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


db = SQLAlchemy(app)


pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


class OCRRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            try:

                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)


                img = Image.open(image_path)
                text = pytesseract.image_to_string(img, lang='rus+eng')


                ocr_record = OCRRecord(text=text, image_path=image_path)
                db.session.add(ocr_record)
                db.session.commit()

                return jsonify({'text': text, 'image_path': image_path})
            except Exception as e:
                return jsonify({'error': str(e)})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
