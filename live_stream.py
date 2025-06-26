# live_stream.py
# Simple MJPEG HTTP streamer for your webcam.
# Usage:
#   pip install flask opencv-python
#   python live_stream.py
# Then point your phone browser to: http://<YOUR_PC_IP>:5000/live


from flask import Flask, Response
import cv2
import threading

# flask app
app = Flask(__name__)
cap = cv2.VideoCapture(0)  # 0 = default webcam

def gen_frames():
    """Yield camera frames as multipart MJPEG."""
    while True:
        success, frame = cap.read()
        if not success:
            break
        # encode as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        data = buffer.tobytes()
        # proper multipart response
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n'
        )

@app.route('/live')
def live():
    """HTTP endpoint that serves the MJPEG stream."""
    return Response(
        gen_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

def start_stream():
    """Run Flask in a background thread."""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # start Flask
    threading.Thread(target=start_stream, daemon=True).start()
    print("MJPEG stream running at http://<YOUR_PC_IP>:5000/live")
    input("Press Enter to stop the stream...\n")
    cap.release()
