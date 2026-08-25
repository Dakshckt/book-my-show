from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from database.db import db
from database.collections import *
from adminPanel.support import login_required , admin_required

# Create your views here.
def loginFunc(req):
    if "user_id" in req.session:
        return redirect(homeFunc)
     
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")

        user = users.find_one({"email" : email , "password" : password})
        if user:
            req.session["user_id"] = str(user["_id"])
            req.session["user_name"] = user["name"]
            req.session["user_email"] = user["email"]
            req.session["user_status"] = user["status"]
            
            return JsonResponse({
                "status" : True,
                "message" : "Login Successfull",
                "user_status" : req.session["user_status"]
            })
        
        return JsonResponse({
            "status": False,
            "message": "Invalid Email or Password"
        })

    return render(req , "admin/login.html")

def signupFunc(req):
    if "user_id" in req.session:
        return redirect(homeFunc)
        
    if req.method == "POST":
        name = req.POST.get("name")
        email = req.POST.get("email")
        phone = req.POST.get("phone")
        password = req.POST.get("password")
        status = False

        customer = {"name" : name , "email" : email , "phone" : phone , "password" : password , "status" : status}
        result = users.insert_one(customer)

        if result.acknowledged:
            return JsonResponse({
                "status": True,
                "message": "User Registered Successfully"
            })

        return JsonResponse({
            "status": False,
            "message": "Unable to Register User"
        })
        

    return render(req , "admin/signup.html")

@login_required
def logoutFunc(req):
    if "user_id" not in req.session:
        return redirect(loginFunc)

    req.session.flush()
    return redirect(loginFunc)

@login_required
@admin_required
def homeFunc(req):
    if "user_id" not in req.session:
        return redirect(loginFunc)
        
    return render(req , "admin/home.html")