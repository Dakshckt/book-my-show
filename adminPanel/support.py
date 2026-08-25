from django.shortcuts import redirect

# /////////////////////////////////////////////////////////////////////////////////
#  Dont kniw how to make this copied from teh chatgpt
def login_required(view_func):

    def wrapper(req, *args, **kwargs):

        if "user_id" not in req.session:
            return redirect("/login")

        return view_func(req, *args, **kwargs)

    return wrapper


def admin_required(view_func):

    def wrapper(req, *args, **kwargs):

        if "user_id" not in req.session:
            return redirect("/login")

        if req.session.get("user_status") != True:
            return redirect("/client/home")

        return view_func(req, *args, **kwargs)

    return wrapper


def client_required(view_func):

    def wrapper(req, *args, **kwargs):

        if "user_id" not in req.session:
            return redirect("/login")

        if req.session.get("user_status") == True:
            return redirect("/home")

        return view_func(req, *args, **kwargs)

    return wrapper

# /////////////////////////////////////////////////////////////////////////////////

def convert_id_json_to_str(data):
    for temp_data in data:
        temp_data["id"] = temp_data["_id"]

    return data

def get_all_data(collection_name):
    data = list(collection_name.find())
    
    data = convert_id_json_to_str(data)

    return data


