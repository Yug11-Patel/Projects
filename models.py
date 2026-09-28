from django.db import models


class Restaurant(models.Model):

    url = models.TextField()
    name = models.TextField()
    rating = models.TextField()
    review_count = models.TextField()
    dining_rating = models.TextField()
    delivery_rating = models.TextField()
    cuisines = models.TextField()
    address = models.TextField()
    status = models.TextField()
    opening_time = models.TextField()
    cost_for_two = models.TextField()
    phone = models.TextField()

    menu_url = models.TextField()
    booking_url = models.TextField()
    direction_url = models.TextField()

    offers = models.TextField()

    digital_payments = models.BooleanField()
    home_delivery = models.BooleanField()
    takeaway = models.BooleanField()
    parking = models.BooleanField()
    stags_allowed = models.BooleanField()
    luxury_dining = models.BooleanField()
    indoor_seating = models.BooleanField()
    family_friendly = models.BooleanField()
    kid_friendly = models.BooleanField()
    work_friendly = models.BooleanField()
    free_parking = models.BooleanField()

    class Meta:
        db_table = "restaurants"
        managed = False

    def __str__(self):
        return self.name