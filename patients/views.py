from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from datetime import datetime
from django.urls import reverse
from users.models import Doctors , Specialty , Patients
from patients.models import Appointment , Time , Status, Patients
from django.http import JsonResponse
from reportlab.pdfgen import canvas
from .models import Report
from django.http import HttpResponse
from users.models import Patients, Doctors, FAQ
from .models import FAQ
from doctors.models import Doctors
from .models import Location
from xhtml2pdf import pisa  # For PDF generation
import io
from django.template.loader import render_to_string
from django.db.models.functions import ExtractMonth
from django.db.models import Q, Count
from django.template.loader import get_template


User = get_user_model()



@login_required(login_url='/login')
def patient_dashboard(request):
  user = request.user

  patient = request.user.patients
  appointments = Appointment.objects.filter(patient=patient)

  current_year = datetime.now().year

  # Monthly Data
  monthly_qs = appointments.filter(start_date__year=current_year)\
      .annotate(month=ExtractMonth('start_date'))\
      .values('month')\
      .annotate(count=Count('id'))\
      .order_by('month')

  months = [entry['month'] for entry in monthly_qs]
  month_counts = [entry['count'] for entry in monthly_qs]


  # Status Data
  status_qs = appointments.values('status__status')\
      .annotate(count=Count('id'))

  statuses = [entry['status__status'] for entry in status_qs]
  status_counts = [entry['count'] for entry in status_qs]

  # Individual status counts
  accepted_count = appointments.filter(status__status='Accepted').count()
  cancelled_count = appointments.filter(status__status='Cancelled').count()
  waited_count = appointments.filter(status__status='Waited').count()

  context = {
      'appointments': appointments,
      'months': months,
      'month_counts': month_counts,
      'statuses': statuses,
      'status_counts': status_counts,
      'total_appointments': appointments.count(),
      'accepted_count': accepted_count,
      'cancelled_count': cancelled_count,
      'waited_count': waited_count,
      'user': user,
      "profile_avatar": user.profile_avatar.url if user.profile_avatar else "assets/img/def.jpeg",
  }


  #context = {
 #       "profile_avatar": user.profile_avatar.url if user.profile_avatar else "/media/doctor/profiles/download.png",
  #  }
  return render(request,'patients/patient_dashboard.html', context)


@login_required(login_url='/login')
def my_appointments(request):
  app = Appointment.objects.filter(patient__user = request.user)
  
  filter_status = request.GET.get('filter_status')
  filter_date = request.GET.get('filter_date')
  filter_doctor_name = request.GET.get('filter_doctor_name')

  if filter_status and filter_status != 'All':
    app = app.filter(status__status=filter_status)

  if filter_date:
    app = app.filter(start_date=filter_date)

  if filter_doctor_name:
    app = app.filter(doctor__user__first_name__icontains=filter_doctor_name)

  return render(request, "patients/my_appointments.html", {
    'appointments': app,
    'filter_status': filter_status,
    'filter_date': filter_date,
    'filter_doctor_name': filter_doctor_name
  })
  



@login_required(login_url='/login')
def book_appointment(request):
  specialities = Specialty.objects.all()
  doctors = Doctors.objects.all()
  
  filter_speciality = request.GET.get('filter_speciality')
  filter_city = request.GET.get('filter_city')
  filter_doctor_name = request.GET.get('filter_doctor_name')

  if filter_speciality and filter_speciality != 'All':
    doctors = doctors.filter(specialty__name=filter_speciality)

  if filter_doctor_name:
    doctors = doctors.filter(user__first_name__icontains=filter_doctor_name)


  return render(request, "patients/book_appointment.html", {
    'doctors': doctors,
    'specialities': specialities,
    'filter_speciality': filter_speciality,
    'filter_doctor_name': filter_doctor_name,
    #'filter_city': filter_city,
  })
  
  # return render(request,'patients/book_appointment.html',{"doctors":doctors})


@login_required(login_url='/login')
def patient_confirm_book(request , doctor):
  print(doctor)
  if request.method == 'POST':
    date = request.POST.get("date")
    summary = request.POST.get("summary")
    #description = request.POST.get("description")
    time = request.POST.get("time")
    heure = Time.objects.get(time=time)
    doctor = Doctors.objects.get(user__username = doctor)
    patient = Patients.objects.get(user=request.user)
    status = Status.objects.get(status="Waited")
    
    appointment = Appointment.objects.create(
      summary=summary,
      #description=description,
      start_date=date,
      time=heure,
      doctor=doctor,
      patient=patient,
      status = status
    )
    
    # Automatic report creation
    Report.objects.create(
        user=request.user,
        doctor=doctor,
        report_type="consultation",
        content=f"Appointment with Dr. {doctor.user.first_name} on {date}. Summary: {summary}"
    )


    if appointment:
      app = Appointment.objects.filter(patient__user = request.user)
      return render(request,'patients/my_appointments.html',{"appointments":app})
    
  doc = Doctors.objects.get(user__username=doctor)
  if doc:
    times = Time.objects.all()
    return render(request,'patients/patient_confirm_book.html' ,{'times':times ,'doctor': doc })
  
  doctors = Doctors.objects.all()
  return render(request,'patients/book_appointment.html',{"doctors":doctors})

  context = {'doctor': doctor}
  return render(request, 'patients/patient_confirm_book.html', context)


# Reports
def report_view(request):
    doctors = Doctors.objects.all()  # Fetch all doctors
    patients = Patients.objects.all()  # Fetch all patients

    return render(request, 'patients/report.html', {
        'doctors': doctors,
        'patients': patients
    })


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'patients/faq.html', {'faqs': faqs})




@login_required
def location_view(request):
    locations = Location.objects.all()
    return render(request, 'patients/location.html', {'locations': locations})


# Report documents for patients
@login_required
def documents_view(request):
    appointments = Appointment.objects.filter(patient=request.user.patients)
    return render(request, 'patients/documents.html', {'appointments': appointments})

@login_required
def download_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user.patients)
    html = render_to_string('patients/appointments_pdf.html', {'appointments': appointments})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appointments.pdf"'
    
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
    return HttpResponse('PDF generation failed')

