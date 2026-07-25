from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
def home_view(request):
    return render(request, "home/home.html")

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email
            send_mail(
                subject=f"New Contact Message from {contact.name}",
                message=contact.message,
                from_email=contact.email,  # or DEFAULT_FROM_EMAIL if required
                recipient_list=['smiqmoses@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')  # or use 'contact' if it's a separate page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
