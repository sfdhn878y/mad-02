

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import (
    JWTManager,
    create_access_token
)
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] = "placesdcsdxcsdcsdcsdcdsfscdssadszsaadsaacdsaddasdasdsadsadsadsadment-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
jwt = JWTManager(app)
db = SQLAlchemy(app)





# ---------------- USER ----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # store hashed password
    role = db.Column(db.String(20), nullable=False)  # admin / student / company

    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # one user → one student profile
    student_profile = db.relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

    # one user → one company profile
    company_profile = db.relationship(
        "CompanyProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )


# ---------------- STUDENT PROFILE ----------------
class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)

    # one-to-one → must be unique
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    department = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)

    skills = db.Column(db.String(200))  # simple for now (comma separated)
    resume = db.Column(db.String(200))

    placement_status = db.Column(db.String(50), default="Not Placed")

    # relation back to user
    user = db.relationship("User", back_populates="student_profile")

    # one student → many applications
    applications = db.relationship(
        "Application",
        back_populates="student",
        cascade="all, delete"
    )


# ---------------- COMPANY PROFILE ----------------
class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)

    # one-to-one → must be unique
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    website = db.Column(db.String(150))
    location = db.Column(db.String(100))
    company_size = db.Column(db.String(50))

    # relation back to user
    user = db.relationship("User", back_populates="company_profile")

    # one company → many jobs
    jobs = db.relationship(
        "Job",
        back_populates="company",
        cascade="all, delete"
    )


# ---------------- JOB ----------------
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profiles.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    skills = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.String(50))
    salary = db.Column(db.String(50))
    benefits = db.Column(db.String(300))

    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50), default="Full-time")

    is_approved = db.Column(db.Boolean, default=False)
    is_closed = db.Column(db.Boolean, default=False)

    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relation
    company = db.relationship("CompanyProfile", back_populates="jobs")

    # one job → many applications
    applications = db.relationship(
        "Application",
        back_populates="job",
        cascade="all, delete"
    )


# ---------------- APPLICATION ----------------
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student_profiles.id"),
        nullable=False
    )

    status = db.Column(db.String(50), default="Applied")

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    remarks = db.Column(db.Text)

    # interview details
    interview_datetime = db.Column(db.DateTime)
    interview_mode = db.Column(db.String(50))  # Online / Offline
    interview_link = db.Column(db.String(300))
    interview_location = db.Column(db.String(200))

    feedback = db.Column(db.Text)
    offer_letter = db.Column(db.String(200))

    # relations
    job = db.relationship("Job", back_populates="applications")
    student = db.relationship("StudentProfile", back_populates="applications")

#Routing
#registeration
@app.route("/register", methods=["POST"])
def register():
    data = request.json                  #stores in dictionary format
    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data["role"]                  # admin / student / company
    phone = data.get("phone")            # optional
    # check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already registered"})
    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role=role,
        phone=phone,
        is_active=True,
        is_approved=False if role == "company" else True
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    })




@app.route("/login", methods=["POST"])
def login_user():

    data = request.get_json()

    if not data:
        return jsonify({"msg": "No data provided"}), 400

    # find user
    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

   

    # check password (because we stored hashed password)
    if not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Password is wrong"}), 401

    if user.role == 'company' and user.is_approved ==False:
        return jsonify({"msg":"you are not approved till yet wati fro approval"}),401


    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
            "email": user.email
        }
    )


    # if company not approved
    return jsonify({
            "msg": "Login successful",
            "token": access_token,
            "role": user.role
        }), 200




@app.route('/company/create_profile', methods=['POST'])
@jwt_required()
def create_company_profile():
    try:
        data = request.get_json()

        # just getting user id from token
        user_id = get_jwt_identity()

        # basic check (not too strict)
        if not data.get('company_name'):
            return jsonify({"message": "company name is required"}), 400

        # create new company object
        new_company = CompanyProfile(
            user_id=user_id,
            company_name=data.get('company_name'),
            industry=data.get('industry'),
            website=data.get('website'),
            location=data.get('location'),
            company_size=data.get('company_size')
        )

        # save to db
        db.session.add(new_company)
        db.session.commit()

        return jsonify({"message": "company profile created"}), 201

    except Exception as e:
        print("error:", str(e))  # simple debug
        return jsonify({"message": "something went wrong"}), 500

@app.route('/edit_company_profile',methods=['POST'])
@jwt_required()
def edit_company_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    company_profile_tr = CompanyProfile.query.filter_by(user_id= user_id).first()
    print(data.get('company_name'))
    company_profile_tr.company_name = data.get('company_name')
    db.session.commit()
    return jsonify({"meg": "compnay profile reg sucusffuly"})

@app.route('/get_company_profie')
@jwt_required()
def get_company_profie():
    #
    print('this si company profileroute')
    jwt_vala_user_id = get_jwt_identity()
    company_profile = CompanyProfile.query.filter_by(user_id = jwt_vala_user_id).first()

    
    return jsonify({
        "company_name": company_profile.company_name,
        "industry": company_profile.industry,
        "website": company_profile.website,
        "location": company_profile.location,
        "company_size": company_profile.company_size
    }), 200






# job post route 
@app.route("/company/post_job", methods=["POST"])
@jwt_required()
def post_job():
    print('post jobs hit ')
    user_id = get_jwt_identity()

    # get company profile of logged in user
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company profile not found"}), 404

    data = request.get_json()

    new_job = Job(
        company_id=company.id,
        title=data.get("title"),
        description=data.get("description"),
        skills=data.get("skills"),
        experience=data.get("experience"),
        salary=data.get("salary"),
        benefits=data.get("benefits"),
        location=data.get("location"),
        job_type=data.get("job_type"),
    )

    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job posted successfully"})

@app.route("/company/my_jobs", methods=["GET"])
@jwt_required()
def get_my_jobs():
    user_id = get_jwt_identity() #2
    print(user_id)
    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    jobs = Job.query.filter_by(company_id=company.id).all()

    job_list = []
    print(job_list)

    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "skills": job.skills,
            "salary": job.salary,
            "location": job.location,
            "job_type": job.job_type,
            "posted_at": job.posted_at,
            "is_close": job.is_closed
        })

    return jsonify(job_list)

@app.route("/company/open_job/<int:job_id>", methods=["POST"])
@jwt_required()
def open_job(job_id):
    current_user = get_jwt_identity()

    company = CompanyProfile.query.filter_by(user_id=current_user).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    job = Job.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({"message": "Job not found"}), 404

    # already open
    if job.is_close == False:
        return jsonify({"message": "Job already open"}), 400

    job.is_close = False   # ✅ FIX HERE
    db.session.commit()

    return jsonify({"message": "Job reopened successfully"})

@app.route("/company/close_job/<int:job_id>", methods=["POST"])
@jwt_required()
def close_job(job_id):
    current_user = get_jwt_identity()

    company = CompanyProfile.query.filter_by(user_id=current_user).first()

    if not company:
        print('company not found')
        return jsonify({"message": "Company not found"}), 404

    job = Job.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        print("job not found")
        return jsonify({"message": "Job not found"}), 404

    # already closed
    if job.is_close == True:
        return jsonify({"message": "Job already closed"}), 400

    job.is_close = True
    db.session.commit()

    return jsonify({"message": "Job closed successfully"})






#############




# ─── Student Routes ────────────────────────────────────────────────────────────
# paste these routes directly into your app.py (above the if __name__ == "__main__" block)


@app.route("/student/get_profile", methods=["GET"])
@jwt_required()
def get_student_profile():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    return jsonify({
        "id": profile.id,
        "user_name": user.name,
        "department": profile.department,
        "year": profile.year,
        "cgpa": profile.cgpa,
        "skills": profile.skills,
        "resume": profile.resume,
        "placement_status": profile.placement_status
    }), 200


@app.route("/student/create_profile", methods=["POST"])
@jwt_required()
def create_student_profile():
    print("create student profile hit")
    user_id = get_jwt_identity()

    existing = StudentProfile.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({"message": "Profile already exists"}), 400

    data = request.get_json()

    profile = StudentProfile(
        user_id=user_id,
        department=data.get("department"),
        year=data.get("year"),
        cgpa=data.get("cgpa"),
        skills=data.get("skills")
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profile created successfully"}), 201


@app.route("/student/edit_profile", methods=["POST"])
@jwt_required()
def edit_student_profile():
    print("edit student profile hit")
    user_id = get_jwt_identity()

    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    data = request.get_json()

    profile.department = data.get("department", profile.department)
    profile.year = data.get("year", profile.year)
    profile.cgpa = data.get("cgpa", profile.cgpa)
    profile.skills = data.get("skills", profile.skills)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200


@app.route("/student/companies", methods=["GET"])
@jwt_required()
def get_all_companies():
    print("get all companies hit")

    companies = CompanyProfile.query.all()

    company_list = []

    for c in companies:
        company_list.append({
            "id": c.id,
            "company_name": c.company_name,
            "industry": c.industry,
            "website": c.website,
            "location": c.location,
            "company_size": c.company_size
        })

    return jsonify(company_list)


@app.route("/student/available_jobs", methods=["GET"])
@jwt_required()
def get_available_jobs():
    print("available jobs hit")

    jobs = Job.query.filter_by(is_approved=True, is_close=False).all()

    job_list = []

    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "skills": job.skills,
            "experience": job.experience,
            "salary": job.salary,
            "location": job.location,
            "job_type": job.job_type,
            "company_name": job.company.company_name,
            "posted_at": job.posted_at
        })

    return jsonify(job_list)


@app.route("/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_for_job(job_id):
    print("apply job hit")
    user_id = get_jwt_identity()

    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"message": "Create your profile before applying"}), 400

    job = Job.query.filter_by(id=job_id).first()

    if not job:
        return jsonify({"message": "Job not found"}), 404

    if job.is_closed:
        return jsonify({"message": "This job is closed"}), 400

    if not job.is_approved:
        return jsonify({"message": "Job is not approved yet"}), 400

    already_applied = Application.query.filter_by(job_id=job_id, student_id=profile.id).first()

    if already_applied:
        return jsonify({"message": "Already applied for this job"}), 400

    application = Application(
        job_id=job_id,
        student_id=profile.id,
        status="Applied",
        applied_at=datetime.utcnow()
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Applied successfully"}), 201


@app.route("/student/my_applications", methods=["GET"])
@jwt_required()
def get_my_applications():
    print("my applications hit")
    user_id = get_jwt_identity()

    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify([])

    applications = Application.query.filter_by(student_id=profile.id).all()

    app_list = []

    for a in applications:
        app_list.append({
            "id": a.id,
            "job_id": a.job_id,
            "job_title": a.job.title,
            "company_name": a.job.company.company_name,
            "status": a.status,
            "applied_at": a.applied_at,
            "remarks": a.remarks,
            "interview_datetime": a.interview_datetime,
            "interview_mode": a.interview_mode,
            "interview_link": a.interview_link,
            "interview_location": a.interview_location,
            "feedback": a.feedback,
            "offer_letter": a.offer_letter
        })

    return jsonify(app_list)






# paste this route into your app.py (with the other student routes)
 
@app.route("/student/company_details/<int:company_id>", methods=["GET"])
@jwt_required()
def get_company_details(company_id):
    print("company details hit")
 
    company = CompanyProfile.query.filter_by(id=company_id).first()
 
    if not company:
        return jsonify({"message": "Company not found"}), 404
 
    # only show approved and open jobs of this company
    jobs = Job.query.filter_by(company_id=company_id, is_approved=True).all()
 
    job_list = []
 
    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "skills": job.skills,
            "experience": job.experience,
            "salary": job.salary,
            "location": job.location,
            "job_type": job.job_type,
            "is_close": job.is_closed,
            "posted_at": job.posted_at
        })
 
    return jsonify({
        "company": {
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "website": company.website,
            "location": company.location,
            "company_size": company.company_size
        },
        "jobs": job_list
    })
 


















def init_db():
    db.create_all()

    # -----------------------
    # 1️Admin
    # -----------------------
    
    if not User.query.filter_by(role="admin").first():
        admin = User(
            name="Admin",
            email="admin@college.com",  
            password=generate_password_hash("admin123"),
            role="admin",
            is_approved=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")






@app.route("/company/job/<int:job_id>/applicants", methods=["GET"])
@jwt_required()
def get_applicants(job_id):
    current_user = get_jwt_identity()

    # get company
    company = CompanyProfile.query.filter_by(user_id=current_user).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    # check job belongs to this company
    job = Job.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({"message": "Job not found"}), 404

    applicants = []

    for app in job.applications:
        student = app.student
        user = student.user

        applicants.append({
            "application_id": app.id,
            "status": app.status,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "skills": student.skills,
            "cgpa": student.cgpa,
            "resume": student.resume
        })

    return jsonify(applicants), 200












if __name__== "__main__":
    with app.app_context():
        
        init_db()

    app.run(debug=True)
