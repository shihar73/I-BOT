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
    console.log('hello');
    e.preventDefault();
    document.getElementById("insta-login-btn").classList.add('button--loading');
    document.getElementById("insta-login-btn").disabled = true;
    var dataString = $(this).serialize();
    console.log('data', dataString);
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
            console.log(response.msg);
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

// var citynames = new Bloodhound({
//     datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
//     queryTokenizer: Bloodhound.tokenizers.whitespace,
//     prefetch: {
//       url: 'assets/citynames.json',
//       filter: function(list) {
//         return $.map(list, function(cityname) {
//           return { name: cityname }; });
//       }
//     }
//   });
//   citynames.initialize();
  
//   $('input').tagsinput({
//     typeaheadjs: {
//       name: 'citynames',
//       displayKey: 'name',
//       valueKey: 'name',
//       source: citynames.ttAdapter()
//     }
//   });

$(document).on('submit', '#data', function (e) {
    console.log('hello');
    e.preventDefault();

    var dataString = $(this).serialize();

    console.log('data', dataString);

    $.ajax({
        type: 'POST',
        url: '/data',
        data: dataString,
        success: function (response) {
            console.log(response.msg);
        }
    })
});


// $("#data").validate({
    
//     rules:{
//         name:"required",
//         email:{required: true},
//         mobile:{required : true,minlength:10},
    
//     },
    
//     messages: {
//         name:"Please fill name",
//         email:{email:"Enter Valid Email!",
//             required:"Enter Email!"
//             },
//         mobile:{minlength:"Please enter Valid Mobile No.",
//             required:"Please enter Mobile No."
//             },
//     },
    
//     submitHandler: function(form){
//         console.log('hello');
//     $.ajax({
//         url: form.action,
//         type: form.method,
//         data: $(form).serialize(),
//         success: function(response) {
//             $('#answers').html(response);
//         }            
//           });		
//     }
//     });