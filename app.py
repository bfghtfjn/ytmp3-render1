from flask import Flask, request, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube to Audio server is running!"

@app.route('/yt')
def youtube_to_audio():
    yt_url = request.args.get('url')
    if not yt_url:
        return "Error: No URL provided", 400

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'quiet': True,
        'noplaylist': True,
        'skip_download': True,
        'cookiefile': 'cookies.txt'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
            return redirect(info['url'])

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
