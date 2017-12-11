$(document).ready(function(){
    $(".hideform").click(function(){
        $(".formah").toggle();
    });
});





function toggle_elem(elem_name) {
    $(elem_name).toggleClass("show-hide-main");
}

$(document).ready(function(){

    $("#control-elem").click(function(){
        $("#nalog-form").toggleClass("show-hide-element");
    });


    $("#pp").click(function(){
        toggle_elem("#pp-list")
    });


    $("#naklad").click(function(){
        toggle_elem("#naklad-list");
    });


    $("#tn-and-acts").click(function(){
        toggle_elem("#tn-and-acts-list");
    });


    $("#my-debts").click(function(){
        toggle_elem("#my-debts-list");
    });


    $("#they-debts").click(function(){
        toggle_elem("#they-debts-list");
    });


    $("#doc-menu").click(function(){
        toggle_elem("#doc-list");
    });


    $("#ops").click(function(){
        toggle_elem("#ops-list");
    });


    $("#hvosty").click(function(){
        toggle_elem("#hvosty-list");
    });


    $("#top-menu").click(function(){
        $("#top-menu-list").toggleClass("show-top-menu");
    });
});


/*dropdown end*/

/*Yandex MAP API script*/
ymaps.ready(init);
var myMap, 
myPlacemark;

function init(){ 
myMap = new ymaps.Map("map", {
center: [53.896199, 27.599893], 
zoom: 16
}); 
            
myPlacemark = new ymaps.Placemark([53.896199, 27.599893], {
hintContent: 'Мы здесь',
balloonContent: 'Наша адрес: г.Минск, переулок Козлова, 7'
});

myMap.geoObjects.add(myPlacemark);
}

/*UP BUTTON*/
window.onload = function() { 

var scrollUp = document.getElementById('scrollup'); 
scrollUp.onclick = function() { 
window.scrollTo(0,0);
};

// show button
window.onscroll = function () { 
if ( window.pageYOffset > 0 ) {
scrollUp.style.display = 'block';
} else {
scrollUp.style.display = 'none';
  }
 };
};