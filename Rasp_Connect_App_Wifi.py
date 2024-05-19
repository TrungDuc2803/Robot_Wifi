from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import socket

app = Flask(__name__)

# Thiết lập các chân GPIO
ENA = 4
IN_1 = 17
IN_2 = 18
IN_3 = 27
IN_4 = 22
ENB = 23
Light = 24

# Tốc độ xe (0 đến 100)
speedCar = 50
speed_low = 20

# Thiết lập các chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN_1, GPIO.OUT)
GPIO.setup(IN_2, GPIO.OUT)
GPIO.setup(IN_3, GPIO.OUT)
GPIO.setup(IN_4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(Light, GPIO.OUT)

pwmA = GPIO.PWM(ENA, 100)
pwmB = GPIO.PWM(ENB, 100)
pwmA.start(speedCar)
pwmB.start(speedCar)

@app.route('/control', methods=['GET'])
def control():
    command = request.args.get('State')
    if command == "F":
        goForward()
    elif command == "B":
        goBack()
    elif command == "L":
        goLeft()
    elif command == "R":
        goRight()
    elif command == "I":
        goForwardRight()
    elif command == "G":
        goForwardLeft()
    elif command == "J":
        goBackRight()
    elif command == "H":
        goBackLeft()
    elif command == "W":
        GPIO.output(Light, GPIO.HIGH)  # Bật đèn
    elif command == "w":
        GPIO.output(Light, GPIO.LOW)   # Tắt đèn
    elif command == "S":
        stopRobot()
    else:
        return jsonify({'status': 'invalid command'})

    return jsonify({'status': 'success'})

@app.route('/get_ip', methods=['GET'])
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Kết nối tới địa chỉ IP bất kỳ để lấy địa chỉ IP của chính mình
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        s.close()
    return jsonify({'ip': ip_address})

def goForward():
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speedCar)

    GPIO.output(IN_3, GPIO.LOW)
    GPIO.output(IN_4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speedCar)

def goBack():
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speedCar)

    GPIO.output(IN_3, GPIO.HIGH)
    GPIO.output(IN_4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speedCar)

def goLeft():
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed_low)

    GPIO.output(IN_3, GPIO.HIGH)
    GPIO.output(IN_4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speedCar)

def goRight():
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speedCar)

    GPIO.output(IN_3, GPIO.LOW)
    GPIO.output(IN_4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speed_low)

def goForwardRight():
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speedCar - speed_low)

    GPIO.output(IN_3, GPIO.LOW)
    GPIO.output(IN_4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speedCar)

def goForwardLeft():
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speedCar)

    GPIO.output(IN_3, GPIO.LOW)
    GPIO.output(IN_4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speedCar - speed_low)

def goBackRight():
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speedCar - speed_low)

    GPIO.output(IN_3, GPIO.HIGH)
    GPIO.output(IN_4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speedCar)

def goBackLeft():
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speedCar)

    GPIO.output(IN_3, GPIO.HIGH)
    GPIO.output(IN_4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speedCar - speed_low)

def stopRobot():
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.LOW)
    pwmA.ChangeDutyCycle(0)

    GPIO.output(IN_3, GPIO.LOW)
    GPIO.output(IN_4, GPIO.LOW)
    pwmB.ChangeDutyCycle(0)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
