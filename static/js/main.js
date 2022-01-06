/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function myFunctionLogs() {
    document.getElementById("myDropdown_logs").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}




$(document).on('submit', '#insta_data', function (e) {
    e.preventDefault();
    document.getElementById("insta-login-btn").classList.add('button--loading');
    document.getElementById("insta-login-btn").disabled = true;
    var dataString = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: '/instalogin',
        data: dataString,
        success: function (response) {
            document.getElementById("insta-login-btn").classList.remove('button--loading');
            document.getElementById("insta-login-btn").disabled = false;
            if(response.status){
                data = "<p style='color: rgba(0, 168, 8, 0.747); position: relative;'>"+response.msg+"<br><span style='font-size: 4rem;'>&#10003;</span> </p>"
                document.getElementById("insta_sc_msg").innerHTML = data;
                document.getElementById("insta_form").classList.add('insta_show');
            }else{
                document.getElementById("insta_er_msg").innerHTML = response.msg;
            }
        }
    })
});



function instaForme(){
    document.getElementById("insta_content").classList.add('insta_show');
    document.getElementById("insta_form").classList.remove('insta_show');
}

function instaContent(){

    document.getElementById("insta_content").classList.remove('insta_show');
    document.getElementById("insta_form").classList.add('insta_show');
}



// tags and comments data sending
$(document).on('submit', '#data', function (e) {
    e.preventDefault();

    document.getElementById("data_btn").classList.add('button--loading');
    document.getElementById("data_btn").disabled = true;

    var dataString = $(this).serialize();

    $.ajax({
        type: 'POST',
        url: '/data',
        data: dataString,
        success: function (response) {
            document.getElementById("data_btn").classList.remove('button--loading');
            document.getElementById("data_btn").disabled = false;
            if(response.status){
                data = "<p style='color: rgb(0, 168, 8); position: relative;'>"+response.msg+"</p>"
                document.getElementById("data_sc_msg").innerHTML = data;;
            }else{
                data = "<p style='color: rgb(217, 12, 12); position: relative;'>"+response.msg+"</p>"
                document.getElementById("data_sc_msg").innerHTML = data;;
            }
            
        }
    })
});

