# Audio to SOAP Note Generation

## Overview

This project provides an API for converting audio recordings of doctor-patient conversations into structured SOAP (Subjective, Objective, Assessment, Plan) notes. It leverages the Whisper model for speech-to-text transcription and the Ollama model to generate SOAP notes from the transcriptions.

## Features

- **Transcription**: Converts audio files into text using the Whisper model.
- **SOAP Note Generation**: Converts the transcribed text into structured SOAP notes using the Ollama model.

## Prerequisites

- Python 3.10
- Flask
- whisper
- langchain_community
- Ollama llama3 #install it locally on your system

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/audio-to-soapnote-generation.git
    cd audio-to-soapnote-generation
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3.10 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies:**

    ```sh
    pip install flask whisper langchain_community
    ```

## Usage

1. **Run the Flask application:**

    ```sh
    python app.py
    ```

2. **API Endpoints:**

    - `/transcribe`: Accepts audio files and returns their transcriptions.
    - `/generate_soap`: Accepts transcriptions and returns structured SOAP notes.

## API Endpoints

### POST `/transcribe`

- **Description**: Accepts audio files and returns their transcriptions.
- **Request**: Multipart/form-data with audio files.
- **Response**: JSON object with filenames and their transcriptions.

### POST `/generate_soap`

- **Description**: Accepts transcriptions and returns structured SOAP notes.
- **Request**: JSON object with the transcription.
- **Response**: JSON object with structured SOAP notes.

## Example Usage

### Transcribe Audio

To transcribe an audio file, send a POST request to the `/transcribe` endpoint with the audio file.

### Generate SOAP Notes

To generate SOAP notes, send a POST request to the `/generate_soap` endpoint with the transcription.

## Notes

- The application ensures confidentiality and adheres to the Health Insurance Portability and Accountability Act (HIPAA) standards for sensitive patient data protection.
- The SOAP notes are generated in a structured JSON format for easy integration with other systems.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.


