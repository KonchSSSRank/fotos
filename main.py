from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    file = request.files['image']
    if file:
      try:
        img = Image.open(file.stream)
        text = pytesseract.image_to_string(img, lang='rus+eng')
        return jsonify({'text': text})
      except Exception as e:
        return jsonify({'error': str(e)})
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)