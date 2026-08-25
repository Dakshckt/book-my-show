

$(document).ready(function(){

    console.log("Admin Panel JS Script Page")

    $("#citySelect").change(function(event){

        event.preventDefault()

        $.ajax({
            url : "/send-location/",
            type : "POST",
            data :
            {
                citySelect : $(this).val(),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            } ,
            success : function(res)
            {
                let locations = res.locations

                $("#locationSelect").empty()
                
                $("#locationSelect").append(`<option value="null">Select theater</option>`)
                locations.forEach(location => {
                    $("#locationSelect").append(`<option value='${location.id}'>${location.name}</option>`)
                });

            }
        })

    })






    $("#locationSelect").change(function(event){

        event.preventDefault()

        $.ajax({
            url : "/send-theater/",
            type : "POST",
            data : {
                locationId : $(this).val(),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            success : function(res)
            {
                theaters = res.theaters

                $("#theaterSelect").empty()
                if(res.status)
                {
                    $("#theaterSelect").append(`<option value="null">Select theater</option>`)   
                    theaters.forEach(theater => {
                        $("#theaterSelect").append(`<option value='${theater.id}'>${theater.name}</option>`)   
                    });
                }
            }
        })

    })





    
    $("#theaterSelect").change(function(event){

        event.preventDefault()

        $.ajax({
            url : "/send-screen/",
            type : "POST",
            data : {
                theaterId : $(this).val(),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            success : function(res)
            {
                screens = res.screens
                $("#screenSelect").empty()
                if(res.status)
                {
                    $("#screenSelect").append(`<option value="null">Select screen</option>`)   
                    screens.forEach(screen => {
                        $("#screenSelect").append(`<option value='${screen.id}'>${screen.name}</option>`)   
                    });
                }
            }

        })

    })

    


})
