from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    cover_image = models.ImageField(upload_to='portfolio/covers/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Photo(models.Model):
    portfolio_item = models.ForeignKey(PortfolioItem, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Photo for {self.portfolio_item.title}"

class BookingInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry: {self.name} - {self.event_type}"

class AboutSection(models.Model):
    heading = models.CharField(max_length=200, default="About ITHIHAS")
    subheading = models.CharField(max_length=200, default="Our Essence")
    paragraph_one = models.TextField(default="Derived from Sanskrit, \"Ithihas\" translates to \"So indeed it was\" — defining grand histories, epic narratives, and unforgettable legacies.")
    paragraph_two = models.TextField(default="We view photography as a sacred responsibility...")
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return "About Us Content & Image"

class ServiceTier(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=50, help_text="e.g. ₹2,80,000")
    description = models.TextField()
    features = models.TextField(help_text="Enter each feature separated by a comma or new line")
    icon_class = models.CharField(max_length=50, default="fa-solid fa-ring", help_text="FontAwesome icon class e.g. fa-solid fa-ring, fa-solid fa-video")
    is_featured = models.BooleanField(default=False, help_text="Highlight as Signature Choice")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

class LegacyStory(models.Model):
    client_names = models.CharField(max_length=150, help_text="e.g. Aarav & Meera")
    location = models.CharField(max_length=150, help_text="e.g. Royal Palace, Jaipur")
    story_quote = models.TextField(help_text="Client's testimonial quote")
    chronicle_type = models.CharField(max_length=150, help_text="e.g. 3-Day Royal Wedding Chronicle")
    image = models.ImageField(upload_to='stories/', help_text="Story cover photo")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Legacy Stories"
        ordering = ['order']

    def __str__(self):
        return f"{self.client_names} - {self.location}"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=150, help_text="e.g. Rohan & Devika")
    location_tag = models.CharField(max_length=150, help_text="e.g. New Delhi Wedding")
    quote = models.TextField(help_text="Client review text")
    rating = models.PositiveIntegerField(default=5, help_text="Star rating from 1 to 5")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.client_name} - {self.location_tag}"

class MentorshipInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    skill_level = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentorship Inquiry from {self.name} ({self.email})"