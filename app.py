from flask import Flask, request, send_file
import yt_dlp
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/yt')
def get_mp3():
    yt_url = request.args.get("url")
    if not yt_url:
        return "No URL provided", 400

    temp_id = str(uuid.uuid4())
    input_file = f"/tmp/{temp_id}.m4a"
    output_file = f"/tmp/{temp_id}.mp3"

    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': input_file,
            'cookiefile': 'cookies.txt'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])

        subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '128k', output_file])

        return send_file(output_file, mimetype="audio/mpeg")

    except Exception as e:
        return f"Error: {str(e)}", 500

    finally:
        if os.path.exists(input_file):
            os.remove(input_file)
            if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
