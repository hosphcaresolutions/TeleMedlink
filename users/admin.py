from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Patients
from .models import Users, Doctors, Patients, Specialty, Report, FAQ
from import_export.admin import ImportExportModelAdmin
from patients.models import Time, Status, Appointment, EmergencyAlert, Report, FAQ, Location
from import_export import resources, fields
from users.models import Patients
from .models import Doctors
from .models import Doctors
from .resources import DoctorResource



admin.site.register(Doctors)
admin.site.register(Patients)
admin.site.register(Specialty)
admin.site.register(Report)
admin.site.register(FAQ)

# Unregister first to avoid AlreadyRegistered error
admin.site.unregister(Patients)
admin.site.unregister(Doctors)

# for patients
class PatientResource(resources.ModelResource):
    class Meta:
        model = Patients
        # Include related user fields if needed
        fields = (
            'user__username',
            'user__first_name',
            'user__last_name',
            'user__gender',
            'user__birthday',
            'user__id_address__city',
            'user__id_address__address_line',
            'user__profile_avatar',

        )


@admin.register(Patients)
class PatientAdmin(ExportMixin, admin.ModelAdmin):

    resource_class = PatientResource
    list_display = (
        'get_username', 'get_first_name', 'get_last_name', 'get_gender', 'get_birthday',  'get_profile_pic', 
    )
    search_fields = ('user__username', 'user__fullname', 'user__gender', 'user__birthday')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_last_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_last_name.short_description = 'Full name'

    def get_first_name(self, obj):
        return f"{obj.user.first_name} {obj.user.first_name}"
    get_first_name.short_description = 'First name'


    def get_gender(self, obj):
        return obj.user.gender
    get_gender.short_description = 'Gender'

    def get_birthday(self, obj):
        return obj.user.birthday
    get_birthday.short_description = 'Birthday'


    def get_profile_pic(self, obj):
        return obj.user.profile_avatar.url if obj.user.profile_avatar else 'No Image'
    get_profile_pic.short_description = 'Profile Picture'


class PatientResource(resources.ModelResource):
    class Meta:
        model = Patients
        # Use fields or exclude if needed
        fields = ('user__username', 'get_first_name', 'get_last_name', 'user__birthday', 'user__gender',)


# for doctors
class DoctorResource(resources.ModelResource):
    full_name = fields.Field()

    class Meta:
        model = Doctors
        fields = (
            'full_name',
            'user__username',
            'user__first_name',
            'user__last_name',
            'user__email',
            'user__gender',
            'user__birthday',
            'user__profile_avatar',
            'specialty__name',
            'bio',
        )
        export_order = (
            'user__username',
            'full_name',
            'user__email',
            'user__gender',
            'user__birthday',
            'user__id_address__city',
            'user__id_address__address_line',
            'specialty__name',
            'bio',
            'user__profile_avatar',
        )

    def dehydrate_full_name(self, doctor):
        return f"{doctor.user.first_name} {doctor.user.last_name}"


class DoctorAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DoctorResource
    list_display = ('user', 'specialty', 'get_gender', 'get_email', 'bio')


    def get_gender(self, obj):
        return obj.user.gender
    get_gender.short_description = 'Gender'


    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'email'


    def get_bio(self, obj):
        return obj.user.bio
    get_bio.short_description = 'bio'

admin.site.register(Doctors, DoctorAdmin)
