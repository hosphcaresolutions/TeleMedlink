from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources, fields
from users.models import Patients, Doctors
from .models import Status, Time
from .models import Appointment, Status, Time
# for pdf export
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string

#for charts
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Count
import json


admin.site.register(Appointment)
admin.site.register(Status)
admin.site.register(Time)

admin.site.unregister(Appointment)

class AppointmentResource(resources.ModelResource):
    patient_name = fields.Field()
    doctor_name = fields.Field()
    status_label = fields.Field()
    time_slot = fields.Field()

    class Meta:
        model = Appointment
        fields = (
            'id',
            'patient_name',
            'doctor_name',
            'start_date',
            'time_slot',
            'status_label',
            'summary',
            'comments',
        )
        export_order = (
            'id',
            'patient_name',
            'doctor_name',
            'start_date',
            'time_slot',
            'status_label',
            'summary',
            'comments',
        )

    def dehydrate_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"

    def dehydrate_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"

    def dehydrate_status_label(self, obj):
        return obj.status.status

    def dehydrate_time_slot(self, obj):
        return obj.time.time if obj.time else ''


# for pdf export
def export_appointments_pdf(modeladmin, request, queryset):
    html = render_to_string('patients/appointmentadmin_pdf.html', {'appointments': queryset})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appointments.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with PDF generation <pre>' + html + '</pre>')
    return response

export_appointments_pdf.short_description = "Export selected appointments as PDF"


class AppointmentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AppointmentResource
    actions = [export_appointments_pdf]
    list_display = ['id', 'patient', 'doctor', 'start_date', 'time', 'status', 'comment']
    list_filter = ['start_date', 'status']
    search_fields = ['patient__user__first_name', 'doctor__user__first_name']

admin.site.register(Appointment, AppointmentAdmin)


# charts


class AppointmentAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart/', self.admin_site.admin_view(self.chart_view), name="appointmentChart"),
        ]
        return custom_urls + urls

    def chart_view(self, request):
        # Sample: Count appointments by status
        data = (
            Appointment.objects
            .values('status')
            .annotate(count=Count('id'))
        )
        labels = [item['status'] for item in data]
        values = [item['count'] for item in data]

        context = dict(
            self.admin_site.each_context(request),
            title="Appointment Chart",
            labels=json.dumps(labels),
            values=json.dumps(values),
        )
        return TemplateResponse(request, "patients/chart_dashboard.html", context)
