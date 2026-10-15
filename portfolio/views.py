from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, PortfolioItem, BookingInquiry, AboutSection, ServiceTier, LegacyStory, Testimonial
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

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
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        # 1. Save the inquiry to your database model safely
        try:
            BookingInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
        except Exception as db_error:
            print(f"Database save error: {db_error}")

        # 2. Email notification details with full safety wrapper
        subject = f"New Inquiry from {name} — ITHIHAS Photography"
        email_content = (
            f"You received a new inquiry from your website contact form:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )

        try:
            send_mail(
                subject,
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                ['ithihasbyvd@gmail.com'],
                fail_silently=True, # Set to True so it never crashes the app if email fails
            )
            messages.success(request, "Your message has been sent successfully. We will get back to you soon!")
        except Exception as e:
            print(f"Email error: {e}")
            messages.success(request, "Your booking inquiry has been saved successfully!")

        return redirect('contact')

    return render(request, 'portfolio/contact.html')