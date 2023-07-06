let serverURL;
serverURL = "http://127.0.0.1:5000/";

var content;
let projectIDs = null;
let diff_htmls = null;
let projectIndex = 0;
let slider = null;
let contentDisplay = null;

document.addEventListener('DOMContentLoaded', function() {
    slider = document.getElementById("player");
    contentDisplay = document.getElementById("displayContent");
    slider.addEventListener("input", event => {
        var idx = event.target.value;
        // contentDisplay.textContent = content[idx][2];
        contentDisplay.innerHTML = diff_htmls[projectIndex][idx]
    })
});
function addButtons(){
    var buttonsDiv = document.querySelector('.buttons');
    var numberOfButtons = projectIDs.length;
    for (var i = 0; i < numberOfButtons; i++) {
      var button = document.createElement('button');
      button.textContent = projectIDs[i].slice(0, 6)+"..."+projectIDs[i].slice(-6);
      button.value = i;
//      button.textContent = projectIDs[i];
      buttonsDiv.appendChild(button);
    }
    var buttonsWithValue  = document.querySelectorAll('button[value]');
    buttonsWithValue.forEach(button => {
        button.addEventListener('click', function() {
        projectIndex = button.value;
        console.log(projectIndex);
        resetSlider();
        slider.max = diff_htmls[projectIndex].length-1;
        contentDisplay.innerHTML = diff_htmls[projectIndex][0];
        });
    });
};

function conditionMet() {
    return projectIDs != null && diff_htmls != null;
};

function resetSlider() {
    slider.value = 0;
    document.getElementById('textInput').value = slider.value;
};

function decrementSlider() {
    if (conditionMet()){
        slider.value--;
        document.getElementById('textInput').value = slider.value;

        var idx = slider.value;
        // contentDisplay.textContent = content[idx][2];
        contentDisplay.innerHTML = diff_htmls[projectIndex][idx]
    }
};

function updateTextInput(val) {
    if (conditionMet()){
        document.getElementById('textInput').value = val;
    }
};

function incrementSlider() {
    if (conditionMet()){
        slider.value++;
        document.getElementById('textInput').value = slider.value;

        var idx = slider.value;
        // contentDisplay.textContent = content[idx][2];
        contentDisplay.innerHTML = diff_htmls[projectIndex][idx]
    }
};



async function retrieveProject() {
    var text = document.getElementById("Username").value;
    const object = {Username: text}
    try {
         const response = await fetch(serverURL + "/create", {
            // mode: 'no-cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(object),
         });
        const message = await response.json();
        console.log(message);
        if (message.status == "ok"){
            projectIDs = message.projectIDs;
            diff_htmls = message.diff_htmls;
            slider.max = diff_htmls[0].length-1;
            contentDisplay.innerHTML = diff_htmls[projectIndex][0];
            addButtons();
        }
    }
    catch (err){
        console.log(err);
        console.log('failed to fetch');
    }
};