from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from products.models import Product
from pets.models import Pet

class Review(models.Model):
    """
    Review model for products and pets
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['pet']),
        ]
    
    def __str__(self):
        item_name = self.product.name if self.product else self.pet.name if self.pet else 'Unknown'
        return f"{self.user.username} - {item_name} - {self.rating}★"
    
    @property
    def stars_range(self):
        """Return range for rendering stars"""
        return range(self.rating)
    
    @property
    def empty_stars_range(self):
        """Return range for rendering empty stars"""
        return range(5 - self.rating)
