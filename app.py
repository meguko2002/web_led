import socket
from flask import Flask, render_template, request, Response, jsonify
from serial import SerialException

from camera import Camera
import serial.tools.list_ports

HOST = None
PORT = 5000

if HOST is not None:
    host = HOST
else:
    host = socket.gethostname()

app = Flask(__name__, static_url_path='/static')


def light_ctr(command):  # 引数:{0: OFF，1: ON, その他:制御せず}, 戻り値: LEDの状態
    reply_msg = ['turned off', 'turned on', 'no connection']
    valByte = command.to_bytes(1, 'big')
    try:
        with serial.Serial("COM4", 115200) as ser:
            ser.write(valByte)
            led_state_str = ser.read()
            led_state = int.from_bytes(led_state_str, 'big')
    except SerialException:
        led_state = 2
    return reply_msg[led_state]

# todo servoに角度値を送って回動させる
def servo_ctr(ang):
    pass
    # valByte = command.to_bytes(1, 'big')
    # try:
    #     with serial.Serial("COM4", 115200) as ser:
    #         ser.write(valByte)
    #         led_state_str = ser.read()
    #         led_state = int.from_bytes(led_state_str, 'big')
    # except SerialException:
    #     led_state = 2
    # return reply_msg[led_state]

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

angle = 0
@app.route("/", methods=['GET', 'POST'])
def index():
    global angle
    if request.method == 'GET':
        command = 2
        msg = light_ctr(command)  # LEDをコントロールせずにLEDの状態を見に行く
        return render_template("index.html", msg=msg)
    if request.method == 'POST':
        led_req = request.form['switch']
        angle_str = request.form['ang_val']
        if is_num(angle_str):
            angle=int(angle_str)
            if angle<0:angle=0
            elif angle>180:angle=180
            # todo servoを制御
            servo_ctr(angle)
            
        if led_req == 'on':
            command = 1
        elif led_req == 'off':
            command = 0
        else:
             command =2
        msg = light_ctr(command)
        return jsonify({"ledState": msg, "angle":angle})


@app.route('/feed')
def feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host=host, port=PORT, debug=True)
