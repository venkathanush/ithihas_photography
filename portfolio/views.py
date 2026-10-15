from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, PortfolioItem, BookingInquiry, AboutSection, ServiceTier, LegacyStory, Testimonial
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import traceback
from django.http import HttpResponse

def home(request):
    categories = Category.objects.all()
    selected_category_slug = request.GET.get('category')
    featured_items = PortfolioItem.objects.filter(is_featured=True)
    
    if selected_category_slug:
        items = PortfolioItem.objects.filter(category__slug=selected_category_slug)
    else:
        items = PortfolioItem.objects.all()

    about_data = AboutSection.objects.first()
    service_tiers = ServiceTier.objects.all()
    legacy_stories = LegacyStory.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        'categories': categories,
        'items': items,
        'featured_items': featured_items,
        'selected_category': selected_category_slug,
        'about': about_data,
        'service_tiers': service_tiers,
        'legacy_stories': legacy_stories,
        'testimonials': testimonials,
    }
    return render(request, 'portfolio/home.html', context)

def gallery(request):
    categories = Category.objects.all()
    selected_category_slug = request.GET.get('category')
    
    if selected_category_slug:
        items = PortfolioItem.objects.filter(category__slug=selected_category_slug)
    else:
        items = PortfolioItem.objects.all()

    context = {
        'categories': categories,
        'items': items,
        'selected_category': selected_category_slug,
    }
    return render(request, 'portfolio/gallery.html', context)

def portfolio_detail(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk)
    return render(request, 'portfolio/detail.html', {'item': item})

def contact(request):
    success = False
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            event_type = request.POST.get('event_type', '')
            
            # Safely handle empty date input from HTML form
            date_str = request.POST.get('event_date', '').strip()
            event_date = date_str if date_str else None
            
            message = request.POST.get('message', '')

            # 1. Save directly to the database model
            BookingInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                event_type=event_type,
                event_date=event_date,
                message=message
            )

            # 2. Send email notification via Brevo SMTP
            subject = f"New Inquiry from {name} ({event_type}) — ITHIHAS Photography"
            email_content = (
                f"You received a new booking inquiry from your website:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Event Type: {event_type}\n"
                f"Event Date: {event_date if event_date else 'Not specified'}\n\n"
                f"Message:\n{message}"
            )

            send_mail(
                subject,
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                ['ithihasbyvd@gmail.com'],
                fail_silently=False,  # Set to False so we catch any email/SMTP errors
            )

            success = True

        except Exception as e:
            # This will display the exact error traceback right on your screen!
            error_details = traceback.format_exc()
            return HttpResponse(f"<h2>Contact Form Error Debugger:</h2><pre>{error_details}</pre>", status=500)

    return render(request, 'portfolio/contact.html', {'success': success})