from flask import Flask, render_template, Response
import cv2, pytesseract
from PIL import Image
from io import BytesIO

app = Flask(__name__)


active = False
frame = None
success = False
def generate_frames():
    global frame
    global success
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        ## read the camera frame

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/video',methods=['POST', 'GET'])
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/extract',methods=['POST', 'GET'])
def active():
    global active
    global success
    if active == True:
        active = False
        if success:
            image = Image.open(BytesIO(frame))
            image.save("image.jpg", format="BMP")
            text = pytesseract.image_to_string(image)
            print(text)
    else:
        active = True
    return render_template("index.html", active = active)



if __name__ == "__main__":
    app.run(debug=True, port = 5001, host='0.0.0.0')