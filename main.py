from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Path to your Firebase Admin SDK JSON file
cred = credentials.Certificate('c.json')

# Initialize Firebase app with Firestore
firebase_admin.initialize_app(cred)

db = firestore.client()

# Route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch course units based on level
@app.route('/get_course_units', methods=['POST'])
def get_course_units():
    level = request.json.get('level')
    # Example course units based on level
    course_units = {
        '1': [
        'Financial Accounting 9',
        'Economics & Entrepreneurship 21',
        'Quantitative Techniques 30',
        'Management & Information Systems 38',
        'Business & Company Law 56',
        'Cost & Management Accounting 69'
    ],
    '2': [
        'Financial Reporting 79',
        'Financial Management 92',
        'Auditing, Ethics & Assurance 103',
        'Management Decision & Control 117',
        'Taxation 128'
    ],
    '3': [
        'Advanced Financial Reporting 137',
        'Public Financial Management 152',
        'Strategy, Governance & Leadership 170',
        'Advanced Financial Management 182',
        'Audit Practice and Assurance 191',
        'Advanced Taxation 206'
    ],
    '4': [
        'Integration of Knowledge'
    ]

    }
    return jsonify(course_units.get(level, []))

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    level = request.form['level']
    course_unit = request.form['course_unit']
    thumbnail = request.files['thumbnail']
    video_link = request.form['video_link']

    # Store thumbnail as bytes in Firestore
    thumbnail_bytes = thumbnail.read()

    # Store data in Firestore
    doc_ref = db.collection('courses').document()
    doc_ref.set({
        'level': level,
        'course_unit': course_unit,
        'thumbnail': thumbnail_bytes,
        'video_link': video_link
    })

    return 'Form submitted successfully'

if __name__ == '__main__':
    app.run(debug=True)
