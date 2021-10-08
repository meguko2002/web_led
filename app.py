import socket
from flask import Flask, render_template, request, Response, jsonify
from serial import SerialException

from camera import Camera
import serial.tools.list_ports

# HOST = '172.18.17.111'
HOST = None
PORT = 5000

if HOST is not None:
    host = HOST
else:
    host = socket.gethostname()

app = Flask(__name__, static_url_path='/static')


def light_ctr(command):
    reply_msg = ['消しました', '点けました', 'マイコンなし']
    valByte = command.to_bytes(1, 'big')
    try:
        with serial.Serial("COM3", 115200) as ser:
            ser.write(valByte)
            led_state_str = ser.read()
            led_state = int.from_bytes(led_state_str, 'big')
    except SerialException:
        print('マイコンとの通信ができていない')
        led_state = 2
    return reply_msg[led_state]


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        msg = light_ctr(0)  # 引数に0,1以外を入れてLEDの状態を変えずにESPからLEDの状態を聞き出す
        return render_template("index.html", msg=msg)
    elif request.method == 'POST':
        req = request.get_data().decode('utf-8')
        command = 1 if req == 'on' else 0
        msg = light_ctr(command)
        return jsonify({"led": msg})


@app.route('/feed')
def feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host=host, port=PORT, threaded=True, debug=True)
