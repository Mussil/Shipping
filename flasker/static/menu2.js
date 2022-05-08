var drivers_num = JSON.parse(document.getElementById("mydiv").dataset.drivers);
console.log(drivers_num);

var parcels_num = JSON.parse(document.getElementById("mydiv").dataset.parcels);
console.log(parcels_num);

var user_choice = "random";

const user_choice_a = ['Time', 'Drivers', 'Distance'];
const user_choice_b = ["Time", "Distance", "Drivers"];
const user_choice_c = ["Distance", "Drivers", "Time"];
const user_choice_d = ["Distance", "Time", "Drivers"];
const user_choice_e = ["Drivers", "Distance", "Time"];
const user_choice_f = ["Drivers", "Time", "Distance"];

$('input[name=radio-btn]').click(function () {
    if (this.id == "user-choice") {
        $("#show-me").show('slow');
        user_choice = "user_choice";
    } else {
        $("#show-me").hide('slow');
        user_choice = "random";
    }
});

$('tbody').sortable();
function sendUserInfo() {
    
    var table = document.getElementById("tbl");
    var noOfrows=table.rows.length;
    var res = new Array(noOfrows);
    for (var i=0;i<noOfrows;i++){
        res[i]=table.rows[i].cells[0].innerHTML;
    }

    if(user_choice != "random"){
        if (res.every((value, index) => value === user_choice_a[index])) {
            user_choice = "a";
        }
        else if (res.every((value, index) => value === user_choice_b[index])) {
            user_choice = "b";
        }
        else if (res.every((value, index) => value === user_choice_c[index])) {
            user_choice = "c";
        }
        else if (res.every((value, index) => value === user_choice_d[index])) {
            user_choice = "d";
        }
        else if (res.every((value, index) => value === user_choice_e[index])) {
            user_choice = "e";
        }
        else{
            user_choice = "f";
        }
    }
    
    const request = new XMLHttpRequest();
    request.open('POST',"/map");

    request.onreadystatechange = function() {
        if(request.readyState == XMLHttpRequest.DONE && request.status == 200) {
          window.location.href = `/map?driversNum=${drivers_num}&parcelsNum=${parcels_num}&userChoice=${user_choice}`;
        }
    }

    request.send();

    showspinner();
}
//////////////////////////////////
