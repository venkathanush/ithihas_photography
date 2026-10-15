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
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        event_type = request.POST.get('event_type', '')
        event_date = request.POST.get('event_date') or None  # Handles empty date strings safely
        message = request.POST.get('message', '')

        # 1. Save the inquiry to your database model safely (including event details if your model has them)
        try:
            # If your BookingInquiry model has event_type / event_date fields, include them:
            BookingInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                event_type=event_type,
                event_date=event_date,
                message=message
            )
        except Exception as db_error:
            print(f"Database save error: {db_error}")
            # If your model doesn't have event_type/event_date columns yet, fallback to basic creation:
            try:
                BookingInquiry.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    message=message
                )
            except Exception as e2:
                print(f"Fallback DB error: {e2}")

        # 2. Email notification details
        subject = f"New Inquiry from {name} ({event_type}) — ITHIHAS Photography"
        email_content = (
            f"You received a new inquiry from your website contact form:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Event Type: {event_type}\n"
            f"Event Date: {event_date}\n\n"
            f"Message:\n{message}"
        )

        try:
            send_mail(
                subject,
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                ['ithihasbyvd@gmail.com'],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Email error: {e}")

        success = True

    return render(request, 'portfolio/contact.html', {'success': success})