let serverURL = ""

function clearError(){
    console.log("here")
    var errMessage = document.querySelectorAll('p[style*="color: red; font-size: 14px;"]');
    console.log(errMessage);
    if (errMessage !== null){
        errMessage.forEach((node) => {
            node.parentNode.removeChild(node);;
        });
    }
};

function showError(node, text){
    var textElement = document.createElement("p");
    textElement.innerText = text;
    textElement.style.color = "red";
    textElement.style.fontSize = "14px";
    textElement.style.marginTop = "0px";
    node.parentNode.insertBefore(textElement, node);
}

document.addEventListener('DOMContentLoaded', function () {
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    var url = document.getElementById("url");
    var submit = document.getElementById("submit");

    username.addEventListener("click", async function(){
        clearError();
    });

    password.addEventListener("click", async function(){
        clearError();
    });

    url.addEventListener("click", async function(){
        clearError();
    });

    submit.addEventListener("click", async function(){
        clearError();
        var usernameInput = username.value;
        var passwordInput = password.value;
        var urlInput = url.value;
        if (usernameInput == "" || passwordInput == "" || urlInput == ""){
            showError(submit, "All the fields should be filled out, please try again");
        }
        else {
            serverURL = urlInput.replaceAll(' ','');
            var match = 300
            // match = await postWriterText({state: "adminlogin", username: usernameInput, password: passwordInput});
            if (match == 300){
                sessionStorage.setItem('serverURL', serverURL);
                window.location.href = "barGraph.html";
            }
            else if (match == 100){
                showError(submit, "Incorrect username/password, please try again");
            }
            else if(match == 400){
                showError(submit, "Sever error encountered, please try again");
            }
        }
    });
});

async function postWriterText(activity) {
    try {
        const response = await fetch(serverURL + "/login", {
            // mode: 'no-cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(activity),
        })
        const message = await response.json();
        console.log(message);
        // 100: Wrong username/password
        // 200: User already exist
        // 300: pass
        // 400: server error
        return message.status
    }
    catch (err){
        console.log(err);
        console.log('failed to fetch');
        return 400;
    }
}