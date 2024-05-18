from flask import Flask, jsonify
import socket
import fcntl
import struct

app = Flask(__name__)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])

@app.route('/get_ip')
def get_ip():
    try:
        ip_address = get_ip_address('wlan0')  # Thay 'wlan0' bằng 'eth0' nếu sử dụng Ethernet
        return jsonify({'ip': ip_address})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
