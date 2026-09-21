from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from config import Config
from database import db, User, ScanHistory
from scanner.url_scanner import scan_url
from scanner.qr_scanner import decode_qr
from scanner.sms_detector import predict_sms
from scanner.email_detector import predict_email

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# ---------- AUTHENTICATION ----------

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method=="POST":

        fullname=request.form["fullname"]
        email=request.form["email"]
        password=request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered.","danger")
            return redirect("/signup")

        user=User(
            fullname=fullname,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Account Created Successfully.","success")
        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect("/dashboard")

        flash("Invalid Email or Password.","danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# ---------- DASHBOARD ----------

@app.route("/dashboard")
@login_required
def dashboard():

    scans=ScanHistory.query.filter_by(user_id=current_user.id).count()
    safe=ScanHistory.query.filter_by(user_id=current_user.id,prediction="Safe").count()
    scam=ScanHistory.query.filter_by(user_id=current_user.id,prediction="Scam").count()

    history=ScanHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ScanHistory.created_at.desc()).limit(5)

    return render_template("dashboard.html",
        scans=scans,
        safe=safe,
        scam=scam,
        history=history)

# ---------- URL ----------

@app.route("/url_scan", methods=["GET","POST"])
@login_required
def url_scan():

    if request.method=="POST":

        url=request.form["url"]
        result=scan_url(url)

        save=ScanHistory(
            user_id=current_user.id,
            scan_type="URL Scan",
            input_data=url,
            prediction=result["prediction"],
            confidence=result["confidence"],
            reason=", ".join(result["reasons"])
        )

        db.session.add(save)
        db.session.commit()

        return render_template("url_result.html",url=url,result=result)

    return render_template("url_scan.html")

# ---------- QR ----------

@app.route("/qr_scan", methods=["GET","POST"])
@login_required
def qr_scan():

    if request.method=="POST":

        image=request.files["qr_image"]

        filename=secure_filename(image.filename)
        filepath=os.path.join(UPLOAD_FOLDER,filename)

        image.save(filepath)

        qr_url=decode_qr(filepath)

        if qr_url is None:
            flash("QR Code Not Detected","danger")
            return redirect("/qr_scan")

        result=scan_url(qr_url)

        save=ScanHistory(
            user_id=current_user.id,
            scan_type="QR Scan",
            input_data=qr_url,
            prediction=result["prediction"],
            confidence=result["confidence"],
            reason=", ".join(result["reasons"])
        )

        db.session.add(save)
        db.session.commit()

        return render_template("qr_result.html",
            image=filename,
            qr_url=qr_url,
            result=result)

    return render_template("qr_scan.html")

# ---------- SMS ----------

@app.route("/sms_scan", methods=["GET","POST"])
@login_required
def sms_scan():

    if request.method=="POST":

        message=request.form["sms"]

        result=predict_sms(message)

        save=ScanHistory(
            user_id=current_user.id,
            scan_type="SMS Scan",
            input_data=message,
            prediction=result["prediction"],
            confidence=result["confidence"],
            reason=", ".join(result["reasons"])
        )

        db.session.add(save)
        db.session.commit()

        return render_template("sms_result.html",
            message=message,
            result=result)

    return render_template("sms_scan.html")

# ---------- EMAIL ----------

@app.route("/email_scan", methods=["GET","POST"])
@login_required
def email_scan():

    if request.method=="POST":

        subject=request.form["subject"]
        body=request.form["body"]

        text=subject+" "+body

        result=predict_email(text)

        save=ScanHistory(
            user_id=current_user.id,
            scan_type="Email Scan",
            input_data=subject,
            prediction=result["prediction"],
            confidence=result["confidence"],
            reason=", ".join(result["reasons"])
        )

        db.session.add(save)
        db.session.commit()

        return render_template("email_result.html",
            subject=subject,
            body=body,
            result=result)

    return render_template("email_scan.html")

@app.route("/history")
@login_required
def history():

    history=ScanHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ScanHistory.created_at.desc())

    return render_template("history.html",history=history)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

if __name__=="__main__":
    app.run(debug=True)