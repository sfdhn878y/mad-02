

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









class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(20), nullable=False)  # admin / student / company
    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # one to one relationship one User has one StudentProfile
    student_profile = db.relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False
    )

    # one to one relationship one User has one CompanyProfile
    company_profile = db.relationship(
        "CompanyProfile",
        back_populates="user",
        uselist=False
    )
# StudentProfile model
class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    # foriegn key one to one each StudentProfile belongs to one User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    department = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    skills = db.Column(db.String(200))  # comma-separated
    resume = db.Column(db.String(200))
    placement_status = db.Column(
        db.String(50), default="Not Placed"
    )
    # one to one each StudentProfile belongs to one User
    user = db.relationship("User", back_populates="student_profile")
    #one to many relationship one Student can apply to many jobs
    applications = db.relationship(
        "Application",
        back_populates="student"
    )
#CompanyProfile model
class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    # foriegn key one to one each CompanyProfile belongs to one User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    website = db.Column(db.String(150))
    location = db.Column(db.String(100))
    company_size = db.Column(db.String(50))
    # one to one each CompanyProfile belongs to one User
    user = db.relationship("User", back_populates="company_profile")
    #one to many relationship one company can post many jobs
    jobs = db.relationship(
        "Job",
        back_populates="company"
    )

#job model
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    # Foreign key → many jobs belong to one company
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profiles.id"),
        nullable=False
    )

    # Basic job info
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Requirements
    skills = db.Column(db.String(200), nullable=False)   # comma-separated
    experience = db.Column(db.String(50))                # NEW
    salary = db.Column(db.String(50))
    benefits = db.Column(db.String(300))                 # NEW

    # Extra details (very useful)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50), default="Full-time")

    # Admin approval system
    is_approved = db.Column(db.Boolean, default=False)

    # Timestamp
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    company = db.relationship("CompanyProfile", back_populates="jobs")

    applications = db.relationship(
        "Application",
        back_populates="job",
        cascade="all, delete"
    )#application model

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"))

    status = db.Column(db.String(50), default="Applied")

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    remarks = db.Column(db.Text)

    # ✅ NEW FIELDS
    interview_datetime = db.Column(db.DateTime)
    interview_mode = db.Column(db.String(50))   # Online / Offline
    interview_link = db.Column(db.String(300))
    interview_location = db.Column(db.String(200))
    feedback = db.Column(db.Text)
    offer_letter = db.Column(db.String(200))
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



if __name__== "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)
