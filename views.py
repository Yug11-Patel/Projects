from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantListAPI(APIView):

    def get(self, request):

        restaurants = Restaurant.objects.all()

        cuisine = request.GET.get("cuisine")
        rating = request.GET.get("rating")
        status = request.GET.get("status")
        home_delivery = request.GET.get("home_delivery")
        takeaway = request.GET.get("takeaway")
        parking = request.GET.get("parking")
        family_friendly = request.GET.get("family_friendly")
        kid_friendly = request.GET.get("kid_friendly")
        luxury_dining = request.GET.get("luxury_dining")

        if cuisine:
            restaurants = restaurants.filter(
                cuisines__icontains=cuisine
            )

        if rating:
            try:
                rating_value = float(rating)

                restaurants = [
                    restaurant
                    for restaurant in restaurants
                    if restaurant.rating
                    and float(restaurant.rating) >= rating_value
                ]

            except ValueError:
                pass

        if status:
            restaurants = restaurants.filter(
                status__icontains=status
            )

        if home_delivery:
            restaurants = restaurants.filter(
                home_delivery=home_delivery.lower() == "true"
            )

        if takeaway:
            restaurants = restaurants.filter(
                takeaway=takeaway.lower() == "true"
            )

        if parking:
            restaurants = restaurants.filter(
                parking=parking.lower() == "true"
            )

        if family_friendly:
            restaurants = restaurants.filter(
                family_friendly=family_friendly.lower() == "true"
            )

        if kid_friendly:
            restaurants = restaurants.filter(
                kid_friendly=kid_friendly.lower() == "true"
            )

        if luxury_dining:
            restaurants = restaurants.filter(
                luxury_dining=luxury_dining.lower() == "true"
            )

        serializer = RestaurantSerializer(
            restaurants,
            many=True
        )

        return Response(serializer.data)