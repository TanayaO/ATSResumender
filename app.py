from flask import Flask,request,render_template
import pickle
import PyPDF2
import re
from PyPDF2 import PdfReader


app=Flask(__name__)

rf_classifier_categorization = pickle.load(open(r"C:\Users\tanay\Desktop\ATS\models\rf_classifier_categorization.pkl", 'rb'))
tfidf_vectorizer_categorization = pickle.load(open(r'C:\Users\tanay\Desktop\ATS\models\tfidf_vectorizer_categorization.pkl', 'rb'))
rf_classifier_job_recommendation=pickle.load(open(r'C:\Users\tanay\Desktop\ATS\rf_classifier_job_recommendation.pkl','rb'))
tfidf_vectorizor_job_recommendation=pickle.load(open(r'C:\Users\tanay\Desktop\ATS\tfidf_vectorizor_job_recommendation.pkl','rb'))
#helper functions=====================================================================================================================

def cleanResume(txt):
    cleanText=re.sub('http\S+\s',' ',txt)
    cleanText=re.sub('RT|cc','.',cleanText)
    cleanText=re.sub('#\S+\s','.',cleanText)
    cleanText=re.sub('@\S+','  ',cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', txt)
    cleanText = re.sub(r'\s+', ' ', cleanText)  # Replace multiple spaces with a single space
    return cleanText.strip()
    cleanText=re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText=re.sub('\s+', ' ', cleanText)
    return cleanText


def predict_category(resume_text):
    resume_text=cleanResume(resume_text)
    resume_tfidf=tfidf_vectorizer_categorization.transform([resume_text])
    predicted_category=rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category

def job_recommendation(resume_text):
    resume_text=cleanResume(resume_text)
    resume_tfidf=tfidf_vectorizor_job_recommendation.transform([resume_text])
    recommended_job=rf_classifier_job_recommendation.predict(resume_tfidf)[0]
    return recommended_job

def pdf_to_text(file):
    reader=PdfReader(file)
    text=''
    for page in range(len(reader.pages)):
        text +=reader.pages[page].extract_text()
    return text 

import re

def extract_contact_number_from_resume(text):
    contact_number= None
    pattern = r'\b(?:\+?(\d{1,3}))?[-.\s]?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'
    match = re.search(pattern, text)
    
    if match:
        contact_number=match.group()
    return contact_number


def extract_email_from_resume(text):
    email = None
    
    # Define a regex pattern for email addresses
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    if match:
        email = match.group()
    return email

def extract_skills_from_resume(text,skills_list):
    skills=[]
    skills_list= [
    # Information Technology
    "Python", "Java", "C++", "JavaScript", "SQL", "PHP", "Ruby", "Go", "Swift", "Kotlin", "R",
    "Django", "Flask", "React", "Angular", "Vue.js", "Spring", "Node.js", "Laravel",
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite",
    "Git", "Docker", "Kubernetes", "Jenkins", "JIRA", "Selenium",
    "AWS", "Azure", "Google Cloud Platform", "OpenStack",
    "TCP/IP", "DNS", "VPN", "Firewalls", "Load Balancers",
    "Penetration Testing", "Ethical Hacking", "SIEM", "OWASP",

    # Data Science & Machine Learning
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy",
    "Matplotlib", "Seaborn", "Tableau", "Power BI", "Hadoop", "Spark", "Hive",
    "Natural Language Processing", "Computer Vision", "Deep Learning", "Data Wrangling", "Data Visualization",
    "Big Data", "Statistics", "Predictive Modeling", "Time Series Analysis",

    # Finance & Accounting
    "Financial Analysis", "Budgeting", "Forecasting", "Tax Preparation", "Auditing",
    "Excel", "QuickBooks", "SAP", "Tally", "Financial Modeling", "Risk Management",
    "GAAP", "IFRS", "Portfolio Management", "Investment Analysis", "Accounting Software",

    # Marketing & Sales
    "SEO", "Content Marketing", "Digital Marketing", "Social Media Management",
    "Google Ads", "Facebook Ads", "CRM", "Email Marketing", "Market Research",
    "Branding", "Copywriting", "Affiliate Marketing", "Salesforce", "Lead Generation",
    "Negotiation", "Customer Relationship Management", "Analytics Tools",

    # Healthcare
    "Patient Care", "Medical Terminology", "Electronic Health Records (EHR)",
    "Diagnosis", "Clinical Procedures", "Pharmacology", "Public Health", "CPR",
    "First Aid", "ICD Coding", "HIPAA Compliance", "Anatomy", "Pathology", "Surgery Assistance",

    # Engineering
    "AutoCAD", "MATLAB", "SolidWorks", "ANSYS", "Mechanical Design", "Electrical Circuits",
    "Civil Engineering", "Structural Analysis", "Thermodynamics", "Fluid Mechanics",
    "Instrumentation", "CAD/CAM", "Robotics", "Embedded Systems",

    # Human Resources
    "Recruitment", "Employee Relations", "HR Policies", "Performance Management",
    "Training and Development", "Payroll Management", "Compensation and Benefits",
    "HRIS", "Conflict Resolution", "Compliance", "Diversity and Inclusion",

    # Education & Training
    "Curriculum Development", "Lesson Planning", "Classroom Management",
    "Online Learning Platforms", "Assessment Design", "Student Counseling"
]

    
    for skill in skills_list:
        pattern=r'\b{}\b'.format(re.escape(skill))
        match=re.search(pattern,text,re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills




def extract_education_from_resume(text):
    education=[]
    
    education_keywords=education_keywords = [
    # Common Academic Degrees
    "Bachelor of Science", "BSc", "BS", "Bachelor of Arts", "BA", "Bachelor of Engineering", "BE", 
    "Bachelor of Technology", "BTech", "Bachelor of Commerce", "BCom", "Bachelor of Business Administration", "BBA", 
    "Bachelor of Computer Applications", "BCA", "Bachelor of Education", "BEd", 
    "Master of Science", "MSc", "MS", "Master of Arts", "MA", "Master of Business Administration", "MBA", 
    "Master of Technology", "MTech", "Master of Engineering", "ME", "Master of Commerce", "MCom", 
    "Master of Computer Applications", "MCA", "Master of Education", "MEd", "Doctor of Philosophy", "PhD", 
    "Doctorate", "MD", "JD", "LLM", "LLB", "DDS", "DVM", 

    # Diplomas & Certifications
    "Diploma", "Postgraduate Diploma", "Advanced Diploma", "Certificate Program", "Certification", 
    "Professional Certification", "Vocational Training",

    # Fields of Study
    "Computer Science", "Information Technology", "Engineering", "Mechanical Engineering", 
    "Electrical Engineering", "Civil Engineering", "Electronics and Communication Engineering", 
    "Artificial Intelligence", "Data Science", "Machine Learning", "Business Administration", 
    "Finance", "Accounting", "Marketing", "Human Resources", "Economics", "Statistics", 
    "Mathematics", "Physics", "Chemistry", "Biology", "Biotechnology", "Public Health", 
    "Psychology", "Sociology", "Law", "Medicine", "Pharmacy", "Education", "History", 
    "Political Science", "Environmental Science", "Journalism", "Mass Communication", "Fine Arts",

    # Professional Certifications
    "PMP", "PRINCE2", "Six Sigma", "ITIL", "AWS Certified Solutions Architect", 
    "Google Cloud Certified", "Azure Fundamentals", "CCNA", "CCNP", "CISSP", "CISM", 
    "CPA", "CFA", "Chartered Accountant", "SHRM-CP", "SPHR", "CIPD", 

    # Technical Certifications
    "CompTIA A+", "CompTIA Network+", "CompTIA Security+", "Certified Ethical Hacker", 
    "Microsoft Certified", "Oracle Certified", "Salesforce Certified", "Adobe Certified Expert",

    # Healthcare Certifications
    "Registered Nurse", "Certified Nursing Assistant", "Medical Assistant Certification", 
    "Basic Life Support (BLS)", "Advanced Cardiovascular Life Support (ACLS)", "CPR Certification",

    # Education-related Certifications
    "Teaching Certification", "TESOL", "TEFL", "CELTA", "Child Development Certification", 
    "Special Education Certification"
]
    for keyword in education_keywords:
        pattern=r"(?i)\b{}\b".format(re.escape(keyword))
        match=re.search(pattern,text)
        if match:
            education.append(match.group())
    return education


def extract_name_from_resume(text):
    name = None
    
    # Define a regex pattern for a person's name (generic example)
    pattern = r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b"
    
    # Search for the pattern in the provided text
    match = re.search(pattern, text)
    if match:
        name = match.group()
    return name

#routes path===============================================================================================================================
@app.route('/')
def resume():
    return render_template('resume.html')

@app.route("/pred",methods=["POST"])
def pred():
    if 'resume' in request.files:
        file=request.files['resume']
        filename=file.filename

        if filename.endswith('.pdf'):
            text= pdf_to_text(file)
        elif filename.endswith('.txt'):
            text=file.read().decode('utf-8')
        else:
            return render_template('resume.html', message="invalid file format,Plese upload a PDF or TXT file.")

        predicted_category = predict_category(text)
        recommended_job=job_recommendation(text)
        phone = extract_contact_number_from_resume(text)
        email=extract_email_from_resume(text)
        skills_list= [
    # Information Technology
    "Python", "Java", "C++", "JavaScript", "SQL", "PHP", "Ruby", "Go", "Swift", "Kotlin", "R",
    "Django", "Flask", "React", "Angular", "Vue.js", "Spring", "Node.js", "Laravel",
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite",
    "Git", "Docker", "Kubernetes", "Jenkins", "JIRA", "Selenium",
    "AWS", "Azure", "Google Cloud Platform", "OpenStack",
    "TCP/IP", "DNS", "VPN", "Firewalls", "Load Balancers",
    "Penetration Testing", "Ethical Hacking", "SIEM", "OWASP",

    # Data Science & Machine Learning
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy",
    "Matplotlib", "Seaborn", "Tableau", "Power BI", "Hadoop", "Spark", "Hive",
    "Natural Language Processing", "Computer Vision", "Deep Learning", "Data Wrangling", "Data Visualization",
    "Big Data", "Statistics", "Predictive Modeling", "Time Series Analysis",

    # Finance & Accounting
    "Financial Analysis", "Budgeting", "Forecasting", "Tax Preparation", "Auditing",
    "Excel", "QuickBooks", "SAP", "Tally", "Financial Modeling", "Risk Management",
    "GAAP", "IFRS", "Portfolio Management", "Investment Analysis", "Accounting Software",

    # Marketing & Sales
    "SEO", "Content Marketing", "Digital Marketing", "Social Media Management",
    "Google Ads", "Facebook Ads", "CRM", "Email Marketing", "Market Research",
    "Branding", "Copywriting", "Affiliate Marketing", "Salesforce", "Lead Generation",
    "Negotiation", "Customer Relationship Management", "Analytics Tools",

    # Healthcare
    "Patient Care", "Medical Terminology", "Electronic Health Records (EHR)",
    "Diagnosis", "Clinical Procedures", "Pharmacology", "Public Health", "CPR",
    "First Aid", "ICD Coding", "HIPAA Compliance", "Anatomy", "Pathology", "Surgery Assistance",

    # Engineering
    "AutoCAD", "MATLAB", "SolidWorks", "ANSYS", "Mechanical Design", "Electrical Circuits",
    "Civil Engineering", "Structural Analysis", "Thermodynamics", "Fluid Mechanics",
    "Instrumentation", "CAD/CAM", "Robotics", "Embedded Systems",

    # Human Resources
    "Recruitment", "Employee Relations", "HR Policies", "Performance Management",
    "Training and Development", "Payroll Management", "Compensation and Benefits",
    "HRIS", "Conflict Resolution", "Compliance", "Diversity and Inclusion",

    # Education & Training
    "Curriculum Development", "Lesson Planning", "Classroom Management",
    "Online Learning Platforms", "Assessment Design", "Student Counseling"
]
        extracted_skills=extract_skills_from_resume(text,skills_list)
        extracted_education=extract_education_from_resume(text)
        name=extract_name_from_resume(text)
 
        return render_template('resume.html',predicted_category=predicted_category,recommended_job=recommended_job,
        phone=phone,name=name,email=email,extracted_skills=extracted_skills,extracted_education=extracted_education)        
    else:
        return render_template("resume.html",message="No resume file uploaded.")

def home():
    if request.method == 'POST':  # Ensure this block is indented properly
        # Simulate prediction logic (replace with actual logic)
        predicted_category = "Software Development"
        message = "File uploaded successfully!"
        return render_template('index.html', predicted_category=predicted_category, message=message)
    # Handle GET request
    return render_template('index.html', predicted_category=None, message=None)



    

if __name__== "__main__":
    app.run(debug=True)