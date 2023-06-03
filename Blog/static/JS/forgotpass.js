var OTP;

function sendOTP(){
    var email = document.getElementById("email").value;
    if(email.length==0){
        alert("Please Enter Your mail")
        return;
    }
    document.getElementsByClassName("forgotpass")[0].style.display = "none";
    document.getElementsByClassName("OTP")[0].style.display = "contents";
    let originalOTP = sendMailToUser(email);
}

function verifyOTP(){
    var userotp = document.getElementsByClassName("otpclass");
    var finalotp = "";

    for(let x = 0; x < userotp.length; x++) {
        finalotp += userotp[x].value.toString();
    }

    if(OTP.OTP == finalotp){
        document.getElementsByClassName("OTP")[0].style.display = "none";
        document.getElementsByClassName("updatepass")[0].style.display = "contents";
    }
    else{
        alert("OTP doesn't match");
    }
}

var button = document.getElementById('linksignup');
    button.addEventListener('click', function(event) {
    event.preventDefault();
});

function showNavigation(){
    document.getElementsByClassName("fa-bars")[0].style.display = "none";
    document.getElementsByClassName("fa-xmark")[0].style.display = "block";
    document.getElementById('nav-list').style.right = "0px";
}

function hideNavigation(){
    document.getElementsByClassName("fa-bars")[0].style.display = "block";
    document.getElementsByClassName("fa-xmark")[0].style.display = "none";
    document.getElementById('nav-list').style.right = "-60%";
}

function changesign(){
    document.getElementById('sign-in').style.left = "calc(-100% - 40px)";
    document.getElementById("signup").style.right = "0";
}

function showForm(){
    document.getElementsByClassName('signin')[0].style.display = "flex";
}

function showPostLink(){
    if(screen.width > 920){
        document.getElementById("profileul").style.display = "block";
        document.getElementById("profileul").style.top = "60px";
    }
}

function hidePostLink(){
    if(screen.width > 920){
        document.getElementById("profileul").style.display = "none";
        document.getElementById("profileul").style.top = "50px";
    }
}

function sendMailToUser(email){
    console.log("Inside mail");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "../sendmail/" + email, true); // Replace with your XML URL

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        OTP = JSON.parse(xhr.responseText);
        if(OTP.OTP == 0){
            alert("User doesn't exists");
            setTimeout(
                function (){
                    location.replace("../");
                }, 0
            );
        }
      }
    };

    xhr.send();
}

function submitNewPassword(){
    if(
        document.getElementById("newpass").value ==
        document.getElementById("confirmpass").value
    ){
        document.getElementById("user_emailupdate").value = document.getElementById('email').value;
        //console.log(document.getElementsByClassName('updatepass')[0]);
        document.getElementsByClassName('updatepass')[0].submit();
    }else{
        alert("Password Doesn't match");
    }
}

function closeSignIn(){
    document.getElementsByClassName("signin")[0].style.display = "none";
    document.getElementById('sign-in').style.left = "0";
    document.getElementById("signup").style.right = "calc(-100% - 40px)";
}