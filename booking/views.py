from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
import pytz

# View to list and create fitness classes
class FitnessClassList(APIView):
    def get(self, request):
        # Fetch all classes starting now or in future
        classes = FitnessClass.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Deserialize request data into FitnessClass model
        serializer = FitnessClassSerializer(data=request.data)

        # Validate input and save if valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to delete a fitness class by ID
class DeleteFitnessClass(APIView):
    def delete(self, request, class_id):
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

        fitness_class.delete()
        return Response({"message": "Class deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class BookClass(APIView):
    def post(self, request):
        class_id = request.data.get("class_id")
        name = request.data.get("client_name")
        email = request.data.get("client_email")

        if not all([class_id, name, email]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

        if fitness_class.available_slots < 1:
            return Response({"error": "No slots available."}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(fitness_class=fitness_class, client_name=name, client_email=email)
        fitness_class.available_slots -= 1
        fitness_class.save()

        return Response({"message": "Booking successful."}, status=status.HTTP_201_CREATED)


class BookingList(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        tz_param = request.query_params.get("tz", "Asia/Kolkata")  # Default to IST
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_tz = pytz.timezone(tz_param)
        except pytz.UnknownTimeZoneError:
            return Response({"error": "Invalid timezone."}, status=400)

        bookings = Booking.objects.filter(client_email=email).select_related("fitness_class")

        data = [{
            "class": b.fitness_class.name,
            "date": b.fitness_class.start_time.astimezone(user_tz).strftime("%Y-%m-%d %H:%M:%S"),
            "instructor": b.fitness_class.instructor,
            "booked_on": b.booking_time.astimezone(user_tz).strftime("%Y-%m-%d %H:%M:%S")
        } for b in bookings]

        return Response(data)

# class BookingList(APIView):
#     def get(self, request):
#         email = request.query_params.get("email")
#         if not email:
#             return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

#         bookings = Booking.objects.filter(client_email=email).select_related("fitness_class")
#         data = [{
#             "class": b.fitness_class.name,
#             "date": b.fitness_class.start_time,
#             "instructor": b.fitness_class.instructor,
#             "booked_on": b.booking_time
#         } for b in bookings]
#         return Response(data)
