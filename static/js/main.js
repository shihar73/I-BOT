/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function myFunctionLogs() {
    document.getElementById("myDropdown_logs").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
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


// loading btn
function loadingBtn() {
    console.log('sdfdgdghdhdhdfhdhdhddh');
    document.getElementById("insta-login-btn").classList.add('button--loading');
    document.getElementById("insta-login-btn").disabled = true;
    
}