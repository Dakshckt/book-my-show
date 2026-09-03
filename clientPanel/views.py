from django.shortcuts import render , redirect
from database.collections import city , movie
from django.http import JsonResponse , HttpResponse
from bson import ObjectId
from datetime import datetime , timedelta
from database.collections import shows , shows_timing , city , theater , movie , movie_type , location , screen , seats , booking
from adminPanel.support import login_required , admin_required , client_required
from django.contrib import messages
import json
# Create your views here.

@login_required
@client_required
def sendMovieFunc(req):
    if req.method == "POST":
        try :
            cityId = req.POST.get("cityId")
            req.session["user_selected_city"] = cityId
            all_shows = list(shows.find({"city_id" : ObjectId(cityId)}))


            movie_list = []
            added_moive_ids = set()

            for element in all_shows:

                movie_id = element["movie_id"]

                if movie_id in added_moive_ids:
                    continue

                added_moive_ids.add(movie_id)

                movieObj = movie.find_one({"_id" : element["movie_id"]})

                
                movie_list.append({
                    "id": str(movieObj["_id"]),
                    "name": movieObj["name"],
                    "description": movieObj["description"],
                    "poster": movieObj["poster"]
                })


            return JsonResponse({
                "status" : True,
                "movies" : movie_list
            })

        
        except Exception as err:
            
            return JsonResponse({
                "status" : False,
                "message" : "Error in Process"
            })


@login_required
@client_required
def clientHomeFunc(req):
    print("\n\nclientHomeFunc Function Called\n\n")

    cities = list(city.find())
    movies = list(movie.find())

    for element in movies:
        element["id"] = element["_id"]

    for element in cities:
        element["id"] = element["_id"]

    
    return render(req , "user/home.html" , {"movies" : movies , "cities" : cities})



@login_required
@client_required
def singleMovieFunc(req , link):
    print("\n\nsingleMovieFunc Function Called\n\n")
    raw_movie = movie.find_one({"_id" : ObjectId(link)})

    types_list = []
    for element in raw_movie["movie_types"]:
        single_movie_type = movie_type.find_one({"_id" : ObjectId(element)})
        types_list.append(single_movie_type["name"])

    select_movie = {
        "id" : str(raw_movie["_id"]),
        "name" : raw_movie["name"],
        "desc" : raw_movie["description"],
        "poster" : raw_movie["poster"],
        "duration" : raw_movie["duration"],
        "movie_types" : types_list
    }


    return render(req , "user/singleMovie.html" , {"movie" : select_movie})




@login_required
@client_required
def movieInTheater(req , link):
    print("\n\nMovieInTheater Function Called\n\n")
    try :
        movieId = link
        cityId = req.session["user_selected_city"]

        all_shows = list(shows.find({"movie_id" : ObjectId(movieId) , "city_id" : ObjectId(cityId)}))
       

        location_list = []
        for element in all_shows:
            locationObj = location.find_one({"_id" : element["location_id"]})
            locationObj["id"] = str(locationObj["_id"])
            locationObj["city_id"] = str(locationObj["city_id"])

            if any(temp_location["id"] == locationObj["id"] for temp_location in location_list):
                continue

            location_list.append(locationObj)

        collected_movies = movie.find_one({"_id" : ObjectId(movieId)})
        collected_movies["id"] = collected_movies["_id"]

        movies = {
            "id": str(collected_movies["_id"]),
            "name": collected_movies["name"],
            "description": collected_movies["description"],
            "poster": collected_movies["poster"]
        }


        return render(req , "user/movieInTheater.html" , {"location_list" : location_list , "movies" : movies})

    except Exception as Err:

        messages.error(req, "Please select a city first.")
        return redirect("/client/home/")



def sendDateFunc(req):
    print("\nsendDateFunc Function Called\n")
    if req.method == "POST":
        movieId = req.POST.get("movie_id")
        locationId = req.POST.get("location_id")
        cityId = req.session["user_selected_city"]

        major_shows = list(shows.find({"movie_id" : ObjectId(movieId) , "city_id" : ObjectId(cityId) , "location_id" : ObjectId(locationId)}))
        all_shows = []
        # print("\n\n")
        # print(major_shows)
        # print("\n\n")


        all_dates = []

        for element in major_shows:

            release_date = element["release_date"]
            release_date = release_date.date()
            to_date = element["to_date"]
            to_date = to_date.date()
            current_date = datetime.now().date()

            if release_date < current_date:
                release_date = current_date

            current_date = release_date

            while current_date <= to_date:

                if current_date not in all_dates:
                    all_dates.append(current_date)

                current_date += timedelta(days=1)

        # print(all_dates)

        return JsonResponse({
            "status" : True,
            "all_dates" : all_dates
        })



@login_required
@client_required
def sendShowsFunc(req):
    print("\nsendShowsFunc Function Called\n")
    if req.method == "POST":
        movieId = req.POST.get("movie_id")
        locationId = req.POST.get("location_id")
        date_selected = req.POST.get("selected_date")  # Wild Card Entry of this Selected Date
        selected_date = datetime.strptime(
            date_selected,
            "%Y-%m-%d"
        )
        cityId = req.session["user_selected_city"]
        

        major_shows = list(shows.find({"release_date" : {"$lte" : selected_date} , "to_date" : {"$gte" : selected_date} , "movie_id" : ObjectId(movieId) , "city_id" : ObjectId(cityId) , "location_id" : ObjectId(locationId)}))
        all_shows = []

        for element in major_shows:

            show_timming_list = list(shows_timing.find({"shows_id" : element["_id"]}))
          
            show_timming_obj_list = []
            for temp in show_timming_list:
                show_timming_obj = {
                    "show_id" : str(temp["shows_id"]),
                    "show_timming_id" : str(temp["_id"]),
                    "starting_time" : temp["start_time"],
                    "ending_time" : temp["end_time"]
                }
                show_timming_obj_list.append(show_timming_obj)

            theaterObj = theater.find_one({"_id" : element["theater_id"]})
            screenObj = screen.find_one({"_id" : element["screen_id"]})

            obj = {
                "theater_id" : str(theaterObj["_id"]),
                "theater_name" : str(theaterObj["name"]),
                "screen_id" : str(screenObj["_id"]),
                "screen_name" : str(screenObj["name"]),
                "shows_timmings" : show_timming_obj_list,
                
            }

            all_shows.append(obj)

        return JsonResponse({
            "status" : True,
            "show_timming" : all_shows
        })
    

def make_payment():
    return True

def calculate_price_func(selected_seats):
    return 0

@login_required
@client_required
def seatSelectionFunc(req , show_id , show_timing_id , date_selected):
    print("\n\nseatSelectionFunc Function Called\n\n")
    # print(date_selected , "\n\n")
    if req.method == "POST":

        booking_date = req.POST.get("date_selected")

        print("Called from seat selection")
        print(booking_date , "\n\n")

        selected_seats = json.loads(req.POST.get("selected_seats"))


        calculated_price = calculate_price_func(selected_seats)
        payment_result = make_payment()


        booking_obj = {

            "user_id" : ObjectId(req.session["user_id"]),
            "show_timing_id" : ObjectId(show_timing_id),
            "show_id" : ObjectId(show_id),
            "selected_seats" : selected_seats,
            "payment_id" : None,
            "booking_date" : datetime.strptime(booking_date, "%Y-%m-%d"),
            "total_amount" : calculated_price,
            "status" : "confirmed",       # Has only 3 values as 'confirmed' 'cancelled' 'available'  
        }
        print("\n\n")
        print(booking_obj)
        print("\n\n")
        result = booking.insert_one(booking_obj)

        if result:    

           return JsonResponse({"status" : True , "message" : "Seat Bokked"})


    # Not displayed the type of seat in the row which will also help to calculate the price of the seat 
    selected_date_obj = datetime.strptime(date_selected, "%Y-%m-%d")

    show_obj = shows.find_one({"_id" : ObjectId(show_id)})
    show_timing_obj = shows_timing.find_one({"_id" : ObjectId(show_timing_id)})
    shows_booking = list(booking.find({"show_id" : show_obj["_id"] , "show_timing_id" : show_timing_obj["_id"] , "status": "confirmed" , "booking_date" : selected_date_obj}))
    seat_booked_ids = []

    for booking_obj in shows_booking:
        seat_booked_ids.extend(booking_obj["selected_seats"])

    # print("\n\n\n")
    # print(seat_booked_ids)
    # print("\n\n\n")

    screen_obj = screen.find_one({"_id" : show_obj["screen_id"]})
    screen_seats_list = list(seats.find({"screen_id" : screen_obj["_id"]}))

    screen_seat_obj = {}

    for temp_seats in screen_seats_list:

        status = "available"
        if str(temp_seats["_id"]) in seat_booked_ids:
            status = "confirmed"

        single_obj = {
           "id" : str(temp_seats["_id"]),
           "screen_id" : str(temp_seats["screen_id"]),
           "row" : temp_seats["row"],
           "column" : temp_seats["column"],
           "name" : temp_seats["name"],
           "type" : temp_seats["type"],
           "status" : status
        }

        row = temp_seats["row"]

        if row not in screen_seat_obj:
            screen_seat_obj[row] = []


        screen_seat_obj[row].append(single_obj)


    return render(req , "user/seatSelection.html" , {"screen_seat_obj" : screen_seat_obj , "date_selected" : date_selected})





def myBookingFunc(req):

    all_booking = list(booking.find({"user_id" : ObjectId(req.session["user_id"])}))

    expired_booking = []
    upcomming_booking = []


    for booking_temp in all_booking:
        show_timming_obj = shows_timing.find_one({"_id" : ObjectId(booking_temp["show_timing_id"])})

        show_date = booking_temp["booking_date"]
        show_start_time = show_timming_obj["start_time"]
        show_end_time = show_timming_obj["end_time"]

        show_datetime = datetime.combine(
            show_date.date(),
            show_end_time.time()
        )

        current_datetime = datetime.now()

        if current_datetime >= show_datetime:
            expired_booking.append(booking_temp)
        else:
            upcomming_booking.append(booking_temp)


    return render(req , "user/myBooking.html" , {"upcomming_booking" : upcomming_booking , "expired_booking" : expired_booking})