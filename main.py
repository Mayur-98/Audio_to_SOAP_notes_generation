# Requires python3.10
from flask import Flask, request, jsonify, redirect, url_for
import whisper
from langchain_community.llms import Ollama
from flask import Flask, abort, request, jsonify
from tempfile import NamedTemporaryFile
import whisper

# Load Ollama model
llm = Ollama(model="llama3")

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model('base')

@app.route('/transcribe', methods=['POST'])
def handler():
    if not request.files:
        # If the user didn't submit any files, return a 400 (Bad Request) error.
        abort(400)

    # For each file, let's store the results in a list of dictionaries.
    results = []

    # Loop over every file that the user submitted.
    for filename, handle in request.files.items():
        # Create a temporary file.
        # The location of the temporary file is available in `temp.name`.
        temp = NamedTemporaryFile()
        # Write the user's uploaded file to the temporary file.
        # The file will get deleted when it drops out of scope.
        handle.save(temp)
        # Let's get the transcript of the temporary file.
        result = model.transcribe(temp.name)
        # Now we can store the result object for this file.
        results.append({
            'filename': filename,
            'transcription': result['text'],
        })

    # Return the results as a JSON response.
    return jsonify({'results': results})


@app.route('/generate_soap', methods=['POST'])
def generate_soap_notes():
    data = request.json
    if 'transcription' not in data:
        return jsonify({"error": "No transcription provided"}), 400

    audio_to_text = data['transcription']
    text_string = " ".join(audio_to_text.split("\n")) + "\n\n"

    system_prompt_1 = f"""You are an expert medical professor assisting in the creation of medically accurate SOAP summaries
from {text_string}.
It is a conversation between doctor and patient.
Assume the person who is asking questions as a doctor and the person who is answering it as patient.

Create a Medical SOAP note summary from the dialogue, following these guidelines:
S (Subjective): Summarize the patient's reported symptoms, including chief complaint and relevant history.
Rely on the patient's statements as the primary source and ensure standardized terminology.
O (Objective): Highlight critical findings such as vital signs, lab results, and imaging, emphasizing important details like the side of the body affected and specific dosages.
Include normal ranges where relevant.
A (Assessment): Offer a concise assessment combining subjective and objective data.
State the primary diagnosis and any differential diagnoses, noting potential complications and the prognostic outlook.
P (Plan): Outline the management plan, covering medication, diet, consultations, and education.
Ensure to mention necessary referrals to other specialties and address compliance challenges.
Considerations: Compile the report based solely on the transcript provided.
Maintain confidentiality and document sensitively.
Use concise medical jargon and abbreviations for effective doctor communication.
Please format the summary in a clean, simple list format without using markdown or bullet points.
Use 'S:', 'O:', 'A:', 'P:' directly followed by the text. Avoid any styling or special characters.

Notes: 1. If patient's information is not present give output as "none".
2. Please ensure that you follow the "Health Insurance Portability and Accountability Act (HIPPA) that are standard for sensitive patient data protection."

Output: Give the list in the following json format strictly.

{{"Patient Name": "[Patient's Name]",
"Date of Birth": "[Date of Birth]",
"Age": "[Age]",
"Gender": "[Gender]",
"Medical Record Number": "[MRN]",
"Soap Notes":[Soap Notes Summary]}}
"""

    soap_notes = llm.invoke(system_prompt_1)
    return jsonify({"soap_notes": soap_notes}), 200


if __name__ == '__main__':
    app.run(debug=True)

