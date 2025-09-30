# Cloud Native Video App Backend

This is the backend component of the Cloud Native Video App, built using FastAPI. It provides a RESTful API for streaming video content.

## Features

* Video streaming endpoint (`/stream/{video_id}`)
* Supports HTTP range requests for partial content retrieval

## Running the Application

1. Ensure you have Python and pip installed on your system.
2. Navigate to the project directory: `cd /Users/ajaygeor/Desktop/cloud-native-video-app/backend`
3. Install the required dependencies: `pip install -r requirements.txt` (assuming a requirements.txt file is present)
4. Run the application using Uvicorn: `uvicorn main:app --reload`

## Testing the Video Streaming Endpoint

You can test the video streaming endpoint using `curl` or a web browser:

* Using `curl`: `curl -v http://localhost:8000/stream/test -o test.mp4`
* Using a web browser: Open `http://localhost:8000/stream/test` in your browser.

## Notes

* This application uses HTTP streaming to deliver video content.
* It supports range requests, allowing clients to request specific byte ranges of the video file.
