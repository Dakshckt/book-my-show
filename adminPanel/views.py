from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from database.collections import city , location , theater , screen , movie_type , movie , seats , shows , shows_timing
from bson import ObjectId
from django.core.files.storage import FileSystemStorage
from datetime import datetime , timedelta
from .support import login_required , admin_required , get_all_data , convert_id_json_to_str
from .info_gather import sendLocation , sendTheater , sendScreen

fs = FileSystemStorage(location = "media/movies")



@login_required
@admin_required
def cityFunc(req):
    if req.method == "POST":

        name= req.POST.get("cityname")
        result = city.insert_one({"name" : name})

        if result.acknowledged:
            return JsonResponse({
                "status" : True,
                "message" : "City Added"
            })

        return JsonResponse({
            "status" : False,
            "message" : "Error City Adding"
        })

    cities = list(city.find())
    return render(req , "admin/city.html" , {"cities" : cities})




@login_required
@admin_required
def locationFunc(req):

    if req.method == "POST":
        locationName = req.POST.get("locationName")
        cityId = req.POST.get("citySelect")

        locationObject = {
            "name" : locationName,
            "city_id" : ObjectId(cityId)
        }

        result = location.insert_one(locationObject)

        if result.acknowledged:
            return JsonResponse({
                "status" : True,
                "message" : "Location Added"
            })

        return JsonResponse({
            "status" : True,
            "message" : "Error Location Adding"
        })

    cities = get_all_data(city)

    return render(req , "admin/location.html" , {"cities" : cities})








@login_required
@admin_required
def theaterFunc(req):

    if req.method == "POST":
        cityId = req.POST.get("citySelect")
        locationId = req.POST.get("locationSelect")
        theaterName = req.POST.get("theaterName")

        cityId = ObjectId(cityId)
        locationId = ObjectId(locationId)

        result = theater.insert_one({"name" : theaterName , "location_id" : locationId})

        if result.acknowledged:
            return JsonResponse({
                "status" : True,
                "message" : "Data Added"
            })

        return JsonResponse({
            "status" : False,
            "message" : "Error Data Adding"
        })

    cities = get_all_data(city)    

    return render(req , "admin/theater.html" , {"cities" : cities})




@login_required
@admin_required
def screenFunc(req):
    if req.method == "POST":

        theaterId = req.POST.get("theaterSelect")
        screenName = req.POST.get("screenName")

        result = screen.insert_one({"name" : screenName , "theater_id" : ObjectId(theaterId)})

        if result.acknowledged:
            return JsonResponse({
                "status" : True,
                "message" : "Screen Added"
            })

        return JsonResponse({
            "status" : False,
            "message" : "Error Screen Adding"
        })


    cities = get_all_data(city)  

    return render(req , "admin/screen.html" , {"cities" : cities})





@login_required
@admin_required
def seatsFunc(req):
    if req.method == "POST":

        screenId = req.POST.get("screenSelect")
        existing = seats.find_one({"screen_id": ObjectId(screenId)})

        if not existing:
            
            rows = int(req.POST.get("row"))
            columns = int(req.POST.get("seats_per_row"))
            rowType = req.POST.getlist("rowType")

            seat_list = []

            for i in range(0 , rows):
                row_no = chr(65 + i)
                seat_type = rowType[i]

                for j in range(1 , columns + 1):
                    column_no = int(j)

                    seat_no = row_no + str(column_no) 

                    seat_obj = {
                        "screen_id" : ObjectId(screenId),
                        "row" : row_no,
                        "column" : column_no,
                        "name" : seat_no,
                        "type" : seat_type
                    }
                    seat_list.append(seat_obj)


            result = seats.insert_many(seat_list)

            if result.acknowledged:
                return JsonResponse({
                    "status" : True,
                    "message" : "Seats Added"
                })
            
            return JsonResponse({
                "status" : False,
                "message" : "Error Occured"
            })
        
        else:
            return JsonResponse({
                "status" : False,
                "message" : "Screen Already Has seats "
            })
            

    cities = get_all_data(city)

    return render(req , "admin/seats.html" , {"cities" : cities})



@login_required
@admin_required
def movieTypeFunc(req):

    if req.method == "POST":
    
        name= req.POST.get("movieTypeName")
        result = movie_type.insert_one({"name" : name})

        if result.acknowledged:
            return JsonResponse({
                "status" : True,
                "message" : "Movie Type Added"
            })

        return JsonResponse({
            "status" : False,
            "message" : "Error Movie Type Adding"
        })


    movieTypes = list(movie_type.find())

    return render(req , "admin/movieType.html" , {"movieTypes" : movieTypes})



@login_required
@admin_required
def movieFunc(req):

    if req.method == "POST":

        name = req.POST.get("name")
        desc = req.POST.get("desc")
        poster = req.FILES.get("poster")
        movieTypeId = req.POST.getlist("movieTypeSelect")
        duration = req.POST.get("duration")

        movieTypeId = [ObjectId(element) for element in movieTypeId]
        
        try:
            filename = fs.save(poster.name , poster)

            result = movie.insert_one({
                "name" : name,
                "description" : desc,
                "poster" : "movies/" + filename,
                "movie_types" : movieTypeId,
                "duration" : int(duration) 
            })

            if result.acknowledged:
                return JsonResponse({
                    "status" : True,
                    "message" : "Movie Added"
                })

            return JsonResponse({
                "status" : False,
                "message" : "Error Movie Adding"
            })

        except Exception as err:

            return JsonResponse({
                "status" : False,
                "message" : "Error Movie Adding"
            })

    movies_type = get_all_data(movie_type)

    return render(req , "admin/movie.html" , {"movies_type" : movies_type})





@login_required
@admin_required
def movieInTheaterFunc(req):
    # Addition of the try and except is remaining 
    if req.method == "POST":
        citySelect = req.POST.get("citySelect")
        locationSelect = req.POST.get("locationSelect")
        theaterSelect = req.POST.get("theaterSelect")
        screenSelect = req.POST.get("screenSelect")
        movieSelect = req.POST.get("movieSelect")
        releaseDate = req.POST.get("releaseDate")
        toDate = req.POST.get("toDate")
        showTimmingList = req.POST.getlist("showTime")

        selected_movie = movie.find_one({"_id" : ObjectId(movieSelect)})


        releaseDate = datetime.strptime(releaseDate , "%Y-%m-%d")
        toDate = datetime.strptime(toDate , "%Y-%m-%d")

        result1 = shows.insert_one({
            "city_id" : ObjectId(citySelect),
            "location_id" : ObjectId(locationSelect),
            "theater_id" : ObjectId(theaterSelect),
            "screen_id" : ObjectId(screenSelect),
            "movie_id" : ObjectId(movieSelect),
            "release_date" : releaseDate,
            "to_date" : toDate
        })

        for times in showTimmingList:
            times = datetime.strptime(times , "%H:%M")

            shows_id = result1.inserted_id
            start_time = times
            end_time = start_time + timedelta(minutes=selected_movie["duration"])

            result2 = shows_timing.insert_one({
                "shows_id" : shows_id,
                "start_time" : start_time,
                "end_time" : end_time
            })

        if result1.acknowledged and result2.acknowledged:

            return JsonResponse({
                "status" : True,
                "message" : "Data Added"
            })
        
        return JsonResponse({
            "status" : False,
            "message" : "Error Data Adding"
        })



    cities = get_all_data(city)
    movies = get_all_data(movie)

    return render(req , 'admin/movieInTheater.html' , {"cities" : cities , "movies" : movies})




