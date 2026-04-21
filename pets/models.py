from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """
    Pet categories (Dog, Cat, Birds, Fish, etc.)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            queryset = Category.objects.filter(slug__iexact=original_slug).exclude(pk=self.pk)
            count = 1
            slug = original_slug
            while queryset.exists():
                slug = f'{original_slug}-{count}'
                count += 1
                queryset = Category.objects.filter(slug__iexact=slug).exclude(pk=self.pk)
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Pet(models.Model):
    """
    Pet model with complete details
    """
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='pets')
    breed = models.CharField(max_length=100, blank=True, null=True)
    age_months = models.IntegerField(help_text='Age in months')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_vaccinated = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pets/', default='pets/default_pet.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_available']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.breed}"
    
    @property
    def age_display(self):
        """Convert months to years and months"""
        years = self.age_months // 12
        months = self.age_months % 12
        if years > 0:
            return f"{years} year{'s' if years > 1 else ''} {months} month{'s' if months > 1 else ''}"
        return f"{months} month{'s' if months > 1 else ''}"
