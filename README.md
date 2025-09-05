# YouTube Video Downloader

A simple web application built with Flask that allows users to download YouTube videos and audio in various formats.

## Features

- Download YouTube videos in MP4 format
- Download audio-only tracks
- Web-based interface with thumbnail preview
- Docker support for easy deployment
- Temporary file cleanup after download

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- **FFmpeg** (required for merging video and audio; see below)

### FFmpeg Requirement

This application uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), which requires the [FFmpeg](https://ffmpeg.org/) executable to be installed on your system for merging video and audio streams.

**How to install FFmpeg:**

- **Windows:**  
  Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add the `bin` folder to your system PATH.
- **macOS:**  
  Install via Homebrew:  
  ```bash
  brew install ffmpeg
  ```
- **Linux:**  
  Install via apt:  
  ```bash
  sudo apt-get update && sudo apt-get install -y ffmpeg
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wabo-kabrel/youtube-video-downloader.git
   cd youtube-video-downloader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter a YouTube URL and click "Download"

4. Select the desired format and download the file

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t youtube-downloader .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 youtube-downloader
   ```

3. Access the application at `http://localhost:5000`

## Project Structure

```
youtube-video-downloader/
├── app.py                 # Main Flask application
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── test_app.py            # Unit tests
├── LICENSE                # MIT License
├── .dockerignore          # Docker ignore file
├── .gitignore             # Git ignore file
├── static/
│   └── css/
│       └── style.css      # CSS styles
└── templates/
    ├── index.html         # Home page template
    └── download.html      # Download options template
```

## Testing

Run the tests using pytest:
```bash
pytest test_app.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for educational purposes only. Please respect YouTube's terms of service and copyright laws when downloading content.
