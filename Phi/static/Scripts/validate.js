function validateRegForm() {
	var elements = document.getElementsByTagName("input");
	for(var i = 0; i < elements.length; i++) {
 		elements[i].style.background = "#fff";
	}

    var c = checkRequired(document.forms["regForm"]["username"].value, "username", "Username");
    if(!c) 
    	return false;
    
    c = checkRequired(document.forms["regForm"]["displayed_name"].value, "displayed_name", "Name to Be Displayed");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["regForm"]["password"].value, "password", "Password");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["regForm"]["password2"].value, "password2", "Password Again");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["regForm"]["email"].value, "email", "Email");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["regForm"]["birthday"].value, "birthday", "Birthday");
	if(!c)
    	return false;
    
    c = validateEmail(document.forms["regForm"]["email"].value);
	if(!c)
    	return false;
    
    c = validatePassword(document.forms["regForm"]["password"].value, document.forms["regForm"]["password2"].value);
	if(!c)
    	return false;
    
    //var element = document.getElementById("reg-btn");
    //element.setAttribute("class", "btn btn-success btn-block");
    //element.innerHTML = "Activation mail has been sent."
    //setTimeout(dummy, 10000);
}

function checkRequired(value, inputName, inputTitle) {
	if (value === null || value == "") {
        react(inputName, "Field must be filled out.", inputTitle);
        return false;
    }
    return true;
}

function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    if (!re.test(email)) {
    	react("email", "Inavalid email address", "Email");
    	return false;
    }
    return true;
}

function validatePassword(password, secondPassword) {
	if (password.length < 6) {
		react("password", "Short password (<6)", "Password");
		return false;
	}

	if (!(password === secondPassword)) {
		react("password2", "Password confirmation failed.", "Password Again");
		return false;
	}
	return true;
}

function react(name, message, inputTitle) {
	var element = document.getElementsByName(name);
	element[0].style.background = "rgb(255, 232, 223)";
	element[0].value = element[0].defaultValue;
	element[0].setAttribute("placeholder", message);
    setTimeout(function f() {
        element[0].setAttribute("placeholder", inputTitle);
    }, 1000);
}

function validateLoginForm() {
	var r = Math.random();

	if (r < 0.5) {
		var element = document.getElementById("login-btn");
    	element.setAttribute("class", "btn btn-danger btn-block");
    	element.innerHTML = "Wrong username or password";
	}
}

function sendForgottenPassword() {
	var r = Math.random();
	var element = document.getElementById("send");

	if (r < 0.5) {
    	element.setAttribute("class", "btn btn-danger btn-block");
    	element.innerHTML = "Failed!";
	}

	else {
		element.setAttribute("class", "btn btn-success btn-block");
    	element.innerHTML = "Sent!";	
	}
}
