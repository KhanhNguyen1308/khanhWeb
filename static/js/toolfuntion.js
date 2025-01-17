function openTool(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

function openGame(evt, GameName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(GameName).style.display = "block";
    evt.currentTarget.className += " active";
  }


function RGBtoHEX() {
    var rValue = parseInt(document.getElementById("rValue").value);
    var gValue = parseInt(document.getElementById("gValue").value);
    var bValue = parseInt(document.getElementById("bValue").value);
    if(Number.isInteger(rValue) && Number.isInteger(bValue) && Number.isInteger(gValue)){
        var value = componentToHex(rValue) + componentToHex(gValue) + componentToHex(bValue);
        document.getElementById("resultHexCode").setAttribute('value',value);
    }
    else{
        var value = "Value must be an interger number in range 0 to 255"
        document.getElementById("rgbToHexMess").innerHTML = value;
    }
    
}
function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function HEXtoRGB(){
    const hexCode = document.getElementById("HEXCODE").value;
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexCode);
    const check = hexCode.split('')[0];
    console.log(check);
    if(check != "#"){
        document.getElementById("HexToRGBMess").innerHTML = "Hex code must start with #"
    }
    else{
        if(hexCode.length < 7){
            document.getElementById("HexToRGBMess").innerHTML = "Wrong code"
        }
        else{
            document.getElementById("resultR").value = parseInt(result[1], 16);
            document.getElementById("resultG").value = parseInt(result[2], 16);
            document.getElementById("resultB").value = parseInt(result[3], 16);
        }
    }
}

function ageCal(){
    var ages = parseInt(document.getElementById("Age").value);
    var result;
    if(Number.isInteger(ages)){
        result = "Your age is " + ages.toString();
    }
    else{
        result = "Plese enter an positive integer number"
    }
    document.getElementById("age_calculate").innerHTML = result;
}