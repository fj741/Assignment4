var timer = 10

var homepage = "{{url_for(home.html)}}"

if(seconds <= 0){
    window.location = homepage
}
else{
    timer --
    document.getElementById("seconds").innerHTML(timer)
    setTimeout("redirect()", 1000)
}