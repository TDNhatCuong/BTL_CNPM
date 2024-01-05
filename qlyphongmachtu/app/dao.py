
import hashlib
from app import app,db
from app.models import Patient, Account, Books, Time
import cloudinary.uploader
from flask_login import current_user



def add_booking(desc, date, time):
    b = Books(desc=desc, booked_date=date, time_id=time,patient=current_user)
    print('acb')
    db.session.add(b)
    db.session.commit()
    return b


def load_time():
    return Time.query.all()

def get_user_by_id(user_id):
    return Account.query.get(user_id)


def auth_user(email, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.email.__eq__(email.strip()),
                                Account.password.__eq__(password)).first()


def add_user(name, email, password, err_msg):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Patient(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    err_msg="Bạn đã đăng ký thành công"

#
# def add_booking(desc, date, time):
#     t = Time.query.filter_by(period = time).first()
#     if t:
#         b = Books(desc=desc, booked_date=date, time_id=t.id, patient=current_user)
#         db.session.add(b)
#         db.session.commit()


def update_info(namSinh,sdt,diaChi,avatar,Patient_id, gioiTinh):
    p = Patient.query.filter_by(id=Patient_id).first()
    a = Account.query.filter_by(id=Patient_id).first()
    if p:
        p.namSinh = namSinh
        p.sdt = sdt
        p.diaChi = diaChi
        p.gioiTinh = gioiTinh
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            print(res)
            a.avatar = res['secure_url']

        db.session.commit()

