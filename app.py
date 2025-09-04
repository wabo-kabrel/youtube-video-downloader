from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
import os

# Initialization of the Flask application
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and display download options
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    try:
        yt = YouTube(video_url)

        # Extract video details
        video_title = yt.title
        thumbnail_url = yt.thumbnail_url

        # Get all available video streams (different resolutions)
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        # Provide an audio-only stream option
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        # Pass all video details to the download.html template    
        return render_template('download.html',
                               video_title=video_title,
                               thumbnail_url=thumbnail_url,
                               audio_stream=audio_stream, 
                               video_url=video_url)        # Passes the original video URL to the template
    
    except Exception as e:
        # Handle errors (e.g., invalid URL, video unavailable)
        print(f"Error: {e}")

        # Redirect to an error page or show a message on the index page
        return redirect(url_for('index', error = "Invalid URL or video unavailable. Please try again."))
    
# Route to handle the actual download request
@app.route('/download_file', methods=['POST'])
def download_file():
    """Handling of the actual download of the selected video or audio stream.
        This demonstrates downloading the file to the server and then sending it to the user."""
    video_url = request.form['video_url']
    itag = request.form['itag']

    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_by_itag(itag)
        return redirect(stream.url)     # Redirects the user to the file's URL for download, instead of downloading to our server.
    
    except Exception as e:
        print(f"Error downloading file: {e}")
        return redirect(url_for('index', error = "Could not download the file. Please try again."))
    
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)        # Debug mode for development, which provides helpful error messages
                               # and automatically reloads the server when changes are made.