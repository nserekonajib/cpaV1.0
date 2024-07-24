from flask import Flask, render_template, request, jsonify, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


# Path to your Firebase Admin SDK JSON fil
path = './static/c.json'
cred = credentials.Certificate(path)

# Initialize Firebase app with Firestore
firebase_admin.initialize_app(cred)

db = firestore.client()

# Course units and topics dictionary
course_units = {
    '1': {
        'Financial Accounting 9': [
            'Introduction to accounting',
            'The accountant',
            'Introduction to the financial reporting framework',
            'Forms of business entities',
            'Principles of double entry system of accounting',
            'Adjustments to financial statements',
            'IAS 2: Inventories',
            'Preparation of financial statements for sole traders, partnerships, and limited companies (for internal use)',
            'Correction of errors and the suspense account',
            'Preparation of financial statements from incomplete records',
            'Preparation of financial statements for non-profit making organisations'
        ],
        'Economics & Entrepreneurship 21': [
            'Microeconomics',
            'Macroeconomics',
            'Entrepreneurship',
            'Business Environment'
        ],
        'Quantitative Techniques 30': [
            'Statistics',
            'Operations Research',
            'Mathematical Techniques',
            'Business Modelling'
        ],
        'Management & Information Systems 38': [
            'Management Principles',
            'Information Systems',
            'E-commerce',
            'IT Management'
        ],
        'Business & Company Law 56': [
            'Contract Law',
            'Company Law',
            'Employment Law',
            'Business Regulations'
        ],
        'Cost & Management Accounting 69': [
            'Costing Techniques',
            'Budgeting',
            'Variance Analysis',
            'Management Reporting'
        ]
    },
    '2': {
        'Financial Reporting 79': [
            'Introduction to Financial Reporting',
            'Framework for Financial Reporting',
            'Preparation of Financial Statements',
            'Ethics and Corporate Governance'
        ],
        'Financial Management 92': [
            'Financial Planning',
            'Investment Decisions',
            'Financing Decisions',
            'Dividend Policy'
        ],
        'Auditing, Ethics & Assurance 103': [
            'Auditing Standards',
            'Ethical Issues in Auditing',
            'Internal Controls',
            'Assurance Services'
        ],
        'Management Decision & Control 117': [
            'Decision Making Techniques',
            'Budgeting and Budgetary Control',
            'Performance Measurement',
            'Risk Management'
        ],
        'Taxation 128': [
            'Principles of Taxation',
            'Tax Compliance',
            'Tax Planning',
            'International Taxation'
        ]
    },
    '3': {
        'Advanced Financial Reporting 137': [
            'Group Financial Statements',
            'Changes in Accounting Standards',
            'Advanced Consolidation',
            'Disclosure Requirements'
        ],
        'Public Financial Management 152': [
            'Government Accounting',
            'Public Sector Budgeting',
            'Financial Management in Public Sector',
            'Public Accountability'
        ],
        'Strategy, Governance & Leadership 170': [
            'Strategic Planning',
            'Corporate Governance',
            'Leadership in Organizations',
            'Business Ethics'
        ],
        'Advanced Financial Management 182': [
            'Advanced Investment Appraisal',
            'Corporate Restructuring',
            'Treasury and Risk Management',
            'International Financial Management'
        ],
        'Audit Practice and Assurance 191': [
            'Audit Planning',
            'Audit Evidence',
            'Audit Reporting',
            'Quality Control'
        ],
        'Advanced Taxation 206': [
            'Advanced Tax Planning',
            'Corporate Taxation',
            'Taxation of Trusts and Estates',
            'VAT and Other Indirect Taxes'
        ]
    },
    '4': {
        'Integration of Knowledge': [
            'Integrative Case Study',
            'Advanced Business Analysis',
            'Strategic Financial Management',
            'Corporate Governance and Leadership'
        ]
    }
}

# Route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch course units based on level
@app.route('/get_course_units', methods=['POST'])
def get_course_units():
    level = request.json.get('level')
    return jsonify(course_units.get(level, {}))

# Route to fetch topics based on course unit
@app.route('/get_topics', methods=['POST'])
def get_topics():
    level = request.json.get('level')
    course_unit = request.json.get('course_unit')
    return jsonify(course_units.get(level, {}).get(course_unit, []))

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    level = request.form['level']
    course_unit = request.form['course_unit']
    topic = request.form['topic']
    subtopic = request.form['subtopic']
    youtube_link = request.form['youtube_link']
    thumbnail = request.files['thumbnail']

   # Store thumbnail as bytes in Firestore
    thumbnail_bytes = thumbnail.read()

  # Store data in Firestore
    doc_ref = db.collection('courses').document()
    doc_ref.set({
        'level': level,
        'course_unit': course_unit,
        'topic': topic,
        'subtopic': subtopic,
        'thumbnail': thumbnail_bytes,
        'youtube_link': youtube_link
        

    })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
