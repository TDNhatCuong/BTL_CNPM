from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from app.models import Time, Medicine, Books, Patient
from wtforms.fields import DateField
from wtforms.widgets import Input


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")


class TimeView(ModelView):
    can_export = True

class MedicinelView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True


class DateWithoutTimeField(DateField):
    widget = Input()

class BooksView(ModelView):                     #DS khám bệnh
    can_export = True
    column_list = ['id', 'patient', 'booked_date', 'time']
    column_filters = ['booked_date']

    column_filters = ['booked_date']

    form_overrides = {
        'booked_date': DateWithoutTimeField
    }

class PatientView(ModelView):                   #Ho so benh an
    column_list = ['name', 'books']



class MyStatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')



admin.add_view(TimeView(Time, db.session))
admin.add_view(MedicinelView(Medicine, db.session))

admin.add_view(BooksView(Books, db.session))
admin.add_view(PatientView(Patient, db.session))


admin.add_view(MyStatsView(name='Thống kê báo cáo'))
