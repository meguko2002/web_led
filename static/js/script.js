window.addEventListener("load", function(){
    document.getElementById("send_on").addEventListener("click",led_on,false);
    document.getElementById("send_off").addEventListener("click",led_off,false);
	document.getElementById('register').addEventListener("click", register,false);
	document.getElementById('angle_val').addEventListener('keypress', test_event,false);
}, false);


function register(led_req) {
    const formData = new FormData();
    formData.append('switch', led_req);
    const angle_val = document.getElementById('angle_val').value;
    formData.append('ang_val',angle_val);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/");
    xhr.send(formData);

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            jsonObj = JSON.parse(this.responseText);
            document.getElementById('led_state').textContent  = jsonObj.ledState;
            document.getElementById('angle').textContent = jsonObj.angle;
        }
    };
}

function test_event(e) {
  	if (e.keyCode === 13) {
        register() ;
	}
}

function led_on(){
    register("on");
}

function led_off(){
    register("off");
}
