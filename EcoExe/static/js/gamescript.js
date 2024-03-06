var objects = Array.from(document.querySelectorAll('.trash'));
var deathzone = document.getElementById("deathzone");

var detectOverlap = (function () {
    function getPositions(elem) {
        var pos = elem.getBoundingClientRect();
        return [[pos.left, pos.right], [pos.top, pos.bottom]];
    }

    function comparePositions(p1, p2) {
        var r1, r2;
        if (p1[0] < p2[0]) {
          r1 = p1;
          r2 = p2;
        } else {
          r1 = p2;
          r2 = p1;
        }
        return r1[1] > r2[0] || r1[0] === r2[0];
    }

    return function (a, b) {
        var pos1 = getPositions(a),
            pos2 = getPositions(b);
        return comparePositions(pos1[0], pos2[0]) && comparePositions(pos1[1], pos2[1]);
    };
})();


function respawn(object){
    object.style.marginTop = 0 + "vh";
}

function move(object){
    if(detectOverlap(object, deathzone)){
        alert("deathzone");
        respawn(object);
    }
    else{
        let absMargin = object.style.marginTop.match(/\d+/g);   //gets just the numeric value
        object.style.marginTop = (absMargin - 1) + "vh";
    }
}