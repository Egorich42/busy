;(function() {
'use strict';

var show_menu = document.getElementById('show-menu');
var close_menu = document.getElementById('close-menu');
var menu = document.getElementById('nav-menu');

show_menu.addEventListener( "click" , function() {menu.classList.add('show'); });
close_menu.addEventListener( "click" , function() {menu.classList.remove('show')});



function toggle(button_name, block_name){
	var button = document.getElementById(button_name)
	var block = document.getElementById(block_name)

	button.addEventListener( "click" , function() {block.classList.toggle('close')});
}




window.onload = function() { 
toggle("show-tax", "tax-period")
toggle("show-hvosty", "hvosty")
toggle("show-portal", "portal")

};

})()
