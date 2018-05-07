;(function() {
'use strict';



function toggle(button_name, block_name){
	var button = document.getElementById(button_name)
	var block = document.getElementById(block_name)

	button.addEventListener( "click" , function() {block.classList.toggle('close')});
}


toggle("show-tax", "tax-period")
toggle("show-hvosty", "hvosty")
toggle("show-portal", "portal")

window.onload = function() { 
toggle("show-tax", "tax-period")
toggle("show-hvosty", "hvosty")
toggle("show-portal", "portal")

};

})()
