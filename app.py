import solution
from flask import Flask, render_template, request, jsonify , send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']

    if not uploaded_file:
        return jsonify({'error': 'No file provided'}), 400

    # Save the uploaded file to a temporary directory
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)

    # Pass the file path to the solution module
    solution.start(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200


@app.route('/submit', methods=['POST'])
def submit():
    try:
        airport_info = {
            'max_planes': int(request.form['max_planes']),
            'boarding_gates': int(request.form['boarding_gates']),
            'max_planes_boarding': int(request.form['max_planes_boarding']),
            'hovering_planes': int(request.form['hovering_planes'])
        }

        flight_info = []

        for key, value in request.form.items():
            if key.startswith('flight'):
                flight_info.append(value)

        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.txt')

        with open(input_file_path, "w") as f:
            f.write(f"{airport_info['max_planes']} {airport_info['boarding_gates']} {airport_info['max_planes_boarding']}\n")
            f.write(f"{airport_info['hovering_planes']}\n")

            for i in range(0, len(flight_info), 5):
                f.write(" ".join(flight_info[i:i+5]) + "\n")

        solution.start(input_file_path)

        return jsonify({'success': True, 'message': 'Form submitted successfully', 'file_path': input_file_path}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400



@app.route('/display-output', methods=['GET'])
def display_output():
    output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.txt')
    with open(output_file_path, 'r') as f:
        output_data = f.read()
    return output_data



if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = r'static\Upload_Folder'
    app.config['OUTPUT_FOLDER'] = r'static\Output_Folder'
    app.run(debug=True)
