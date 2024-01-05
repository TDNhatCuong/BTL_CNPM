from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from app.models import Time, Medicine, Books, Patient, MedicalForm, Doctor, Prescription
# from wtforms.fields import DateField
# from wtforms.widgets import Input


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")


class TimeView(ModelView):
    can_export = True

class MedicineView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True


# class DateWithoutTimeField(DateField):
#     widget = Input()

class BooksView(ModelView):                     #DS khám bệnh
    can_export = True
    column_list = ['id', 'patient', 'booked_date', 'time']
    column_filters = ['booked_date']

    # form_overrides = {
    #     'booked_date': DateWithoutTimeField
    # }

class PatientView(ModelView):
    can_export = True
    column_list = ['name', 'gioiTinh', 'namSinh', 'diaChi']
    column_filters = ['name', 'gioiTinh', 'namSinh']

class DoctorView(ModelView):
    column_list = ['name', 'ngayVaoLam']
    column_filters = ['name']
    can_export = True


class MedicalFormView(ModelView):
    column_list = ['patient', 'description', 'disease', 'date', 'doctor']
    #column_filters = ['patient']

    # form_overrides = {
    #     'date': DateWithoutTimeField
    # }

class PrescriptionView(ModelView):
    column_list = ['medicalForm', 'medicalForm.date', 'medicine', 'quantity', 'guide']
    #column_filters = ['medicalForm', 'medicalForm.date']
    # can_export = True




class MyStatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')




admin.add_view(TimeView(Time, db.session))
admin.add_view(MedicineView(Medicine, db.session))

admin.add_view(BooksView(Books, db.session))
admin.add_view(PatientView(Patient, db.session))
admin.add_view(DoctorView(Doctor, db.session))

admin.add_view(MedicalFormView(MedicalForm, db.session))
admin.add_view(PrescriptionView(Prescription, db.session))

admin.add_view(MyStatsView(name='Thống kê báo cáo'))
