from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, PortfolioItem, BookingInquiry, AboutSection, ServiceTier, LegacyStory, Testimonial
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import traceback
from django.http import JsonResponse, HttpResponse

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
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            event_type = request.POST.get('event_type', '')
            
            date_str = request.POST.get('event_date', '').strip()
            event_date = date_str if date_str else None
            
            message = request.POST.get('message', '')

            # 1. Save directly to the database model (Guaranteed save)
            BookingInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                event_type=event_type,
                event_date=event_date,
                message=message
            )

            # 2. Try sending email notification via Brevo SMTP (fail silently)
            try:
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
                    fail_silently=True,
                )
            except Exception as mail_err:
                print(f"Email error (non-blocking): {mail_err}")

            # Return a simple success response that never crashes
            return HttpResponse(
                "<div style='background:#111116; color:#00BFFF; padding:40px; text-align:center; font-family:sans-serif; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;'>"
                "<h1>Inquiry Received Successfully!</h1>"
                "<p style='color:#ccc; margin-top:10px;'>Thank you for reaching out to ITHIHAS. We will get back to you shortly.</p>"
                "<a href='/' style='margin-top:20px; background:#00BFFF; color:#000; padding:10px 20px; border-radius:9999px; text-decoration:none; font-weight:bold;'>Return Home</a>"
                "</div>"
            )

        except Exception as e:
            print(f"Contact form critical error: {e}")
            return HttpResponse("An error occurred while saving your inquiry. Please try again.", status=500)

    success = request.GET.get('submitted') == 'true'
    return render(request, 'portfolio/contact.html', {'success': success})