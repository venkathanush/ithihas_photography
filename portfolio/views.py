from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, PortfolioItem, BookingInquiry, AboutSection, ServiceTier, LegacyStory, Testimonial
from django.core.mail import send_mail
from django.conf import settings

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
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        message = request.POST.get('message')
        
        # Save to Database
        BookingInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            event_type=event_type,
            event_date=event_date if event_date else None,
            message=message
        )
        
        # Send Brevo Email Notification to Studio Admin
        subject = f"New Booking Inquiry: {name} ({event_type})"
        email_body = f"""
        You have received a new legacy booking inquiry on ITHIHAS:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Event Type: {event_type}
        Event Date: {event_date}
        
        Message:
        {message}
        """
        try:
            send_mail(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL], # Send to your studio inbox
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")

        return render(request, 'portfolio/contact.html', {'success': True})
        
    return render(request, 'portfolio/contact.html')