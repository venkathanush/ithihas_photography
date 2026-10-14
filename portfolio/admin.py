from django.contrib import admin
from .models import Category, PortfolioItem, Photo, BookingInquiry, AboutSection, ServiceTier, LegacyStory, Testimonial

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    inlines = [PhotoInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'event_type', 'event_date', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent creating multiple about sections (singleton pattern)
        return not AboutSection.objects.exists()

@admin.register(ServiceTier)
class ServiceTierAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_featured', 'order')
    list_editable = ('order', 'is_featured')

@admin.register(LegacyStory)
class LegacyStoryAdmin(admin.ModelAdmin):
    list_display = ('client_names', 'location', 'chronicle_type', 'order')
    list_editable = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'location_tag', 'rating', 'order')
    list_editable = ('order',)