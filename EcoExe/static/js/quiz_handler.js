var opt0 = document.getElementsByClassName("0 ");
var opt1 = document.getElementsByClassName("1 ");
var opt2 = document.getElementsByClassName("2 ");
var opt3 = document.getElementsByClassName("3 ");

var answers = [
    opt0,
    opt1,
    opt2,
    opt3
]

var tableBody = document.getElementById("tblOptions"); 

var rowID = 0;

answers.forEach(function(item) { 
    var row = document.createElement("tr");
    row.id = rowID;
    rowID++;

    for(let i = 0; i < item.length; i++){
        var cell = document.createElement("td"); 
        cell.appendChild(item[i]);
    }

    tableBody.appendChild(row); 
}); 