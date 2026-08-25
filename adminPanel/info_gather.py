from django.http import JsonResponse
from bson import ObjectId
from database.collections import location , theater , screen


def sendLocation(req):
    if req.method == "POST":
        try:
            cityId = req.POST.get("citySelect")
            location_list = []
            
            locations = list(location.find({"city_id" : ObjectId(cityId)}))

            for element in locations:
                location_list.append({"id" : str(element["_id"]) , "name" : element["name"]})
            
            return JsonResponse({
                "status" : True,
                "locations" : location_list
            })
        
        except Exception as err:
            return JsonResponse({
                "status" : False,
                "message" : "Error Occured"
            })




def sendTheater(req):
    if req.method == "POST":
        locationId = req.POST.get("locationId")


        theaters = list(theater.find({"location_id" : ObjectId(locationId)}))

        theater_list = []

        for element in theaters:
            theater_list.append({
                "id" : str(element["_id"]),
                "name" : element["name"]
            })


        print(theater_list)

        return JsonResponse({
            "status" : True,
            "theaters" : theater_list
        })




def sendScreen(req):
    if req.method == "POST":

        theaterId = req.POST.get("theaterId")

        screens = list(screen.find({"theater_id" : ObjectId(theaterId)}))

        screen_list = []

        for element in screens:
            screen_list.append({
                "id" : str(element["_id"]),
                "name" : element["name"]
            })

        # print(screen_list)
            
        return JsonResponse({
            "status" : True,
            "screens" : screen_list
        })

