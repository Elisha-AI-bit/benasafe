from flask import Flask
from pyngrok import ngrok, conf

# Set custom path to your ngrok.exe
conf.get_default().ngrok_path = r"C:\Users\THE ARCHTECT\AppData\Local\Microsoft\WindowsApps\ngrok.exe"

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask via Ngrok!"

if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print(f" * Ngrok tunnel: {public_url}")
    app.run(port=5000)
