import socket
from flask import Flask, render_template, request, Response,jsonify
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
    valByte = command.to_bytes(1, 'big')
    try:
        with serial.Serial("COM3", 115200) as ser:
            ser.write(valByte)
            led_state_str = ser.read()
            led_state = int.from_bytes(led_state_str, 'big')
    except SerialException:
        print('マイコンとの通信ができていない')
        led_state = 0
    return led_state


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        led_state = light_ctr(2)    # 引数に0,1以外を入れてLEDの状態をESPから聞き出す
        msg = 'ON' if led_state else 'OFF'
        return render_template("index.html", msg=msg)
    elif request.method == 'POST':
        req = request.get_data().decode('utf-8')
        command = 1 if req == 'on' else 0
        led_state = light_ctr(command)
        msg = '点けました' if led_state else '消しました'
        # return msg
        # responseにjsonを返してみる
        return jsonify({"led": msg})


@app.route('/feed')
def feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host=host, port=PORT, threaded=True, debug=True)
