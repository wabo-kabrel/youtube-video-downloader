from flask import Flask, render_template, request, redirect, url_for, send_file, after_this_request
import yt_dlp
import os
import uuid

# Initialization of the Flask application
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and display download options
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        # Get video info
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'bestvideo+bestaudio/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
        
        video_title = info.get('title')
        thumbnail_url = info.get('thumbnail')
        formats = info.get('formats', [])

        # Filter for video and audio formats
        video_streams = [f for f in formats if f.get('vcodec') != 'none' and f.get('ext') == 'mp4']
        audio_streams = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']

        audio_stream = audio_streams[0] if audio_streams else None

        return render_template('download.html',
                               video_title=video_title,
                               thumbnail_url=thumbnail_url,
                               audio_stream=audio_stream,
                               video_streams=video_streams,
                               video_url=video_url)
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('index', error=f"Error: {e}"))
    
# Route to handle the actual download request
@app.route('/download_file', methods=['POST'])
def download_file():
    video_url = request.form['video_url']
    format_id = request.form['format_id']
    temp_filename = f"temp_{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',
        'outtmpl': temp_filename,
        'quiet': True,
        'merge_output_format': 'mp4',  # Ensures ffmpeg merges video+audio
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = temp_filename
        @after_this_request
        def remove_file(response):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Error deleting temp file: {e}")
            return response
        return send_file(filename, as_attachment=True)
    except Exception as e:
        print(f"Error downloading file: {e}")
        return redirect(url_for('index', error="Could not download the file. Please try again."))
# Run the Flask application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)