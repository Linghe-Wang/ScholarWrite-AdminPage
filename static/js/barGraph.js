dates = ["Aug 1", "Aug 2", "Aug 3", "Aug 4", "Aug 5", "Aug 6", "Aug 7", "Aug 8", "Aug 9", "Aug 10",
    "Aug 11", "Aug 12", "Aug 13", "Aug 14", "Aug 15", "Aug 16", "Aug 17", "Aug 18", "Aug 19", "Aug 20",
    "Aug 21", "Aug 22", "Aug 23", "Aug 24", "Aug 25", "Aug 26", "Aug 27", "Aug 28", "Aug 29", "Aug 30",
    "Aug 31", "Sep 1", "Sep 2", "Sep 3", "Sep 4", "Sep 5", "Sep 6", "Sep 7", "Sep 8", "Sep 9", "Sep 10",
    "Sep 11", "Sep 12", "Sep 13", "Sep 14", "Sep 15", "Sep 16", "Sep 17", "Sep 18", "Sep 19", "Sep 20",
    "Sep 21", "Sep 22", "Sep 23", "Sep 24", "Sep 25", "Sep 26", "Sep 27", "Sep 28", "Sep 29", "Sep 30",
    "Oct 1"];
 data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,11,2,1,5,7,10,7,2,9,10,13,12,15,7,3,7,
 4,3,2,1,11,2,1,5,7,10,7,15,13,15,11,12];
 console.log(dates.length);
 console.log(data.length);
let windowWidth;
let windowHeight;
let projectChart;
let chartHeight;
let idButton;
// Sample data for three bar graphs
const data1 = {
    labels: dates.slice(0, 15),
    datasets: [{
        label: 'Number of Edits',
        data: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        hoverBackgroundColor: 'rgb(93, 173, 226)'
    }]
};

// Chart configuration options
const options = {
    scales: {
        y: {
            beginAtZero: true
        }
    },
    maintainAspectRatio: false,
};

function prevChart(event){
    var currentPos = Number(event.target.parentNode.childNodes[0].value);
    if (currentPos >= 15){
        event.target.parentNode.childNodes[0].value = currentPos - 15;
        var canvas = event.target.parentNode.nextSibling.childNodes[0].getContext('2d');
        const chartInstance = Chart.getChart(canvas);
        chartInstance.data.labels = dates.slice(currentPos-15, currentPos);
        chartInstance.data.datasets[0].data = data.slice(currentPos-15, currentPos);
        chartInstance.update();
    }
}

function nextChart(event){
     var currentPos = Number(event.target.parentNode.childNodes[0].value);
     if (currentPos < 45){
        event.target.parentNode.childNodes[0].value = currentPos + 15;
        var canvas = event.target.parentNode.nextSibling.childNodes[0].getContext('2d');
        const chartInstance = Chart.getChart(canvas);
        chartInstance.data.labels = dates.slice(currentPos+15, currentPos+30);
        chartInstance.data.datasets[0].data = data.slice(currentPos+15, currentPos+30);
        chartInstance.update();
     }
}

function createButton(projectID){
    var buttonContainer = document.createElement('div')
    buttonContainer.className = "button-container";

    var section = (chartHeight-10)/4
    idButton = document.createElement('button');
    idButton.innerText = projectID;
    idButton.style.height = section+"px";
    idButton.value = 0;

    var prevButton = document.createElement('button');
    prevButton.innerText = "prev";
    prevButton.style.height = (3*section)+"px";
    prevButton.addEventListener('click',prevChart);

    var nextButton = document.createElement('button');
    nextButton.innerText = "next";
    nextButton.style.height = (3*section)+"px";
    nextButton.addEventListener('click', nextChart);

    buttonContainer.appendChild(idButton);
    buttonContainer.appendChild(prevButton);
    buttonContainer.appendChild(nextButton);

    projectChart.appendChild(buttonContainer);
    document.body.appendChild(projectChart);
    prevButton.style.width = ((idButton.clientWidth)/2) +"px";
    nextButton.style.width = ((idButton.clientWidth)/2) +"px";
}

function createChart(number, projectID){
    var capsule = document.createElement('div');
    var chartElement = document.createElement('canvas');
    chartElement.innerHTML=" ";
    chartElement.id = "chart"+number;
    chartElement.className = "chart-canvas";
    chartElement.style.height = chartHeight+"px";

    capsule.appendChild(chartElement);
    projectChart.appendChild(capsule);
    chartElement.style.width = (windowWidth - idButton.offsetWidth - 10)+"px";

    var canvas = document.getElementById('chart'+number).getContext('2d');
    // Create the charts
    new Chart(canvas, {
        type: 'bar',
        data: data1,
        options: options
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const serverURL = sessionStorage.getItem('serverURL');
    console.log(serverURL); // Outputs: John

    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    const head = document.getElementById('head');
    const divider = document.getElementById('divider');
    const heightOffset = head.offsetHeight + divider.offsetHeight;
    chartHeight = ((windowHeight - heightOffset)/5);

    projectChart = document.createElement('div');
    projectChart.className = "project-chart";
    createButton("6407acffd9dd10d010993a70");
    createChart(1, "6407acffd9dd10d010993a70");

    projectChart = document.createElement('div');
    projectChart.className = "project-chart";
    createButton("9s7v6g9wq2nj4040b0wn1934");
    createChart(2, "9s7v6g9wq2nj4040b0wn1934");

    projectChart = document.createElement('div');
    projectChart.className = "project-chart";
    createButton("4653adfs245g7szd9n312g10");
    createChart(3, "4653adfs245g7szd9n312g10");
});


async function retrieveProject() {
  const object = {message: "Please give me list of projects"}
  try {
       const response = await fetch(serverURL + "/list", {
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
  }
  catch (err){
      console.log(err);
      console.log('failed to fetch');
  }
};