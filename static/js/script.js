let eye = document.getElementById("eye");
let password = document.getElementById("password");

eye.onclick = function(){
    if(password.type == "password"){
        password.type = "text";
    }else{
        password.type = "password";
    }
}