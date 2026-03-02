from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
import json

from core import models
from external_apis import dispatcher


def list_movies(request):
    # SELECT DISTINCT movie_name FROM screening
    movie_names = (
        models.Screening.objects
        .values("movie_name")
        .distinct()
        .order_by("movie_name")
    )
    return JsonResponse({"movies": [m["movie_name"] for m in movie_names]})


def list_screenings(request):
    movie_name = request.GET.get("movie")
    if not movie_name:
        return JsonResponse({"error": "movie query param required"}, status=400)

    screenings = (
        models.Screening.objects
        .filter(movie_name=movie_name)
        .select_related("theater")
        .order_by("date")
    )
    return JsonResponse({
        "screenings": [
            {
                "theater_name": s.theater.name,
                "address": s.theater.address,
                "date": s.date,
            }
            for s in screenings
        ]
    })


def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        if not data.get("email"):
            return JsonResponse({"error": "Email required"}, status=400)

        
        # For authentification, using Django's built-in User
        user = models.User.objects.create_user(
            username=data['name'],
            email=data['email'],
            password=data['password'],
        )
        user.save()
        
        # Creating our BookUser model, saving what we want to know on user
        book_user = models.BookUser(
            user=user,
            is_company=data.get("is_company", False),
        )
        book_user.save()

        return JsonResponse({
            "username": book_user.name,
            "email": book_user.email,
            "id": book_user.id,
            "is_company": book_user.is_company,
        }, status=201)


def get_user(request):
    user_id = request.GET.get('id')
    if not user_id:
        return JsonResponse({'error':'id required'}, status=400)
    try:
        user = models.BookUser.objects.get(pk=user_id)
        return JsonResponse({
            "username": user.name,
            "email": user.email,
            "id": user.id,
            "is_company": user.is_company,
        })
    except models.BookUser.DoesNotExist:
        return JsonResponse({'error':'not found'}, status=404)


def get_my_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Must be authenticated to see your profile"},
            status=403,
        )

    # For Django's built-in User to our BookUser
    user = request.user.bookuser

    return JsonResponse({
        "username": user.name,
        "email": user.email,
        "id": user.id,
        "is_company": user.is_company,
    })


def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required."}, status=400
        )

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful"})
    else:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)


def create_screening(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Must be authenticated"}, status=403)

    book_user = request.user.bookuser
    if not book_user.is_company:
        return JsonResponse({"error": "Only company users can manage screenings"}, status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        try:
            theater = models.Theater.objects.get(pk=data["theater_id"])
        except models.Theater.DoesNotExist:
            return JsonResponse({"error": "Theater not found"}, status=404)

        if theater.owner != book_user:
            return JsonResponse({"error": "You do not own this theater"}, status=403)

        screening = models.Screening(
            movie_name=data["movie_name"],
            date=data["date"],
            theater=theater,
        )
        screening.save()
        return JsonResponse({
            "id": screening.id,
            "movie_name": screening.movie_name,
            "date": screening.date,
            "theater_id": theater.id,
        }, status=201)


def cancel_screening(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "must be authenticated"}, status=403)

    book_user = request.user.bookuser
    if not book_user.is_company:
        return JsonResponse({"error": "only company users can manage screening"}, status=403)

    if request.method == "DELETE":
        data = json.loads(request.body)
        try:
            screening = models.Screening.objects.get(pk=data["screening_id"])
        except models.Screening.DoesNotExist:
            return JsonResponse({"error": "Screening not found"}, status=404)

        if screening.theater.owner != book_user:
            return JsonResponse({"error": "You do not own this theater"}, status=403)

        screening.delete()
        return JsonResponse({}, status=204)


def create_theater(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "must be authenticated"}, status=403)

    book_user = request.user.bookuser
    if not book_user.is_company:
        return JsonResponse({"error": "Only company users can create theaters"}, status=403)

    if request.method == "POST":
        data = json.loads(request.body)
        theater = models.Theater(
            name=data["name"],
            address=data["address"],
            owner=book_user,
        )
        theater.save()
        return JsonResponse({
            "id": theater.id,
            "name": theater.name,
            "address": theater.address,
        }, status=201)

def book_movie(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Must be authenticated to book a seat"},
            status=403,
        )

    if request.method == "POST":
        data = json.loads(request.body)

        try:
            theater = models.Theater.objects.get(pk=data["theater_id"])
        except models.Theater.DoesNotExist:
            return JsonResponse({"error": "Theater not found"}, status=404)

        return JsonResponse(
            dispatcher.book_seat(
                theater=theater,
                movie_name=data["movie_name"],
                date=data["date"],
            )
        )