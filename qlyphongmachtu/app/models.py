from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime
from flask_login import UserMixin
import hashlib


class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    avatar = Column(String(255),default="https://cdn-icons-png.flaticon.com/512/3177/3177440.png")

    type = Column(String(50), default="user")
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __str__(self):
        return self.id

class Doctor(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    ngayVaoLam = Column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

class Admin(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    ngayTao = Column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Patient(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    diaChi = Column(String(50))
    namSinh = Column(String(50))
    sdt = Column(String(50), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    #active = Column(Boolean, default=False)
    books = relationship('Books', cascade="all,delete", backref='patient', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }

class Nurse(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    phuTrachKhoa = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'nurse'
    }

class Cashier(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    chucVu = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'cashier'
    }

class Time(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    khungGio = Column(String(20), nullable=False)
    books_times = relationship('Books', backref='time', lazy=True)

    def __str__(self):
        return self.khungGio

class Books(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booked_date = Column(DateTime, default=datetime.now())
    patient_id = Column(Integer, ForeignKey(Patient.id,  onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    time_id = Column(Integer, ForeignKey(Time.id), nullable=False)

    def __str__(self):
        return self.id



if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()

        # a = Admin(name='Pham Ngoc Son', email='truongson@gmail.com',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), type="admin", ngayTao="07/10/2022")
        #
        # d = Doctor(name='Truong Dinh Cuong', email='nhatcuong@gmail.com',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), type="doctor", ngayVaoLam="14/11/2022")
        #
        # db.session.add(a)
        # db.session.add(d)
        # db.session.commit()






