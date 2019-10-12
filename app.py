from flask import Flask,request,render_template,redirect,send_file
import pyqrcode
import io
import os
import time
import webbrowser
import pyimgur

app = Flask(__name__)

CLIENT_ID = "xxxxxxx"
CLIENT_SECRET = "xxxxxxx"
im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)

auth_url = im.authorization_url('pin')
pin = "xxxxxxxx"

@app.route('/')
def index():
    webbrowser.open(auth_url)
    return render_template('ImgurAuth.html')

@app.route('/verification', methods=['POST'])
def authorize():
    pin = request.form['imgurverif']
    im.exchange_pin(pin)
    return render_template('index.html')

@app.route('/qrcode', methods=['POST'])
def geturl():
    userinput = request.form['userinp']
    url = userinput

    userinput = pyqrcode.create(userinput)
    userinput.png("qrcodes/output.png",scale=10)
    uploaded_image = im.upload_image('qrcodes/output.png', title=url)
    uploaded_image_link = uploaded_image.link
    dataindex = uploaded_image_link.find(".png")
    uploaded_image_data = uploaded_image_link[20:dataindex]
    uploaded_image_link = uploaded_image_link[6:dataindex]
    os.remove("qrcodes\\output.png")

    return    render_template('datahandled.html', qrdata=uploaded_image_data , qrlink=uploaded_image_link, url=url)

if(__name__ == '__main__'):

    app.debug = True
    app.run()