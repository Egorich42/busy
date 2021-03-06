
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