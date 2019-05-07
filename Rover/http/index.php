<!doctype html>
<!-- Always force latest IE rendering engine (even in intranet) & Chrome Frame
Remove this if you use the .htaccess -->
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

<!-- Apple iOS Safari settings -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

<meta charset=utf-8>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rover control</title>

<link href="/index.css" rel="stylesheet">
<body>

<div class="controlbtns">
 <a class="disconnect-data_websocket"><button>Disconnect</button></a>
 <a class="connect-data_websocket"><button>Connect</button></a>
 <a class="show-controls"><button>Show controls</button></a>
 <a class="hide-controls"><button>Hide controls</button></a>
</div>

<div>
 <canvas id="controlCanvas" style="border:1px solid #000000;"></canvas>
</div>

<script>
function changeServoDegree(degree) {
	window.globals.sendData("S " + degree + " " + degree);
	document.getElementById("Degrees").innerHTML = "Degrees: " + (-1 * (degree - 90)).toString();
}

function stopCommand() {
   window.globals.sendData("C STOP");
}
</script>

<table style="width:100%">
<tr>
<td><button class="button1" type="button" width="100%" onClick="stopCommand(0)">STOP</button></td> 
<td><button class="button1" type="button" onClick="changeServoDegree(180)">-90</button></td> 
<td><button class="button1" type="button" onClick="changeServoDegree(135)">-45</button></td> 
<td><button class="button1" type="button" onClick="changeServoDegree(90)">0</button></td>
<td><button class="button1" type="button" onClick="changeServoDegree(45)">45</button></td>
<td><button class="button1" type="button" onClick="changeServoDegree(0)">90</button></td>
<td width="120px"><b><span id="Degrees">Degrees: 0</span></b></td>
</tr>
</table>

<div class="logcntnr">
 <fieldset>
  <legend>Console</legend>
  <pre class=log></pre>
   <div class="readline">
    <input type="text" placeholder="Write your data-to-be-sent here and press enter.">
   </div>
  </fieldset>
</div>

<div id="control" class="row fill tab-pane active col-lg-1 col-centered" style="height: 100%;"></div>

<script src="/static/js/jquery-2.1.1.min.js"></script>
<script src="/static/js/paper-full-min.js"></script>

<script>
controlCanvas.width = window.innerWidth;
//controlCanvas.height = window.innerHeight * 0.7;
controlCanvas.height = 240;
</script>

</script>
<script type="text/paperscript" src="/main.paperscript.js" canvas="controlCanvas"></script>
<script type="text/javascript" src="/main.js"></script>

<script>
 ENDPOINT = "ws://<?php echo $_SERVER['HTTP_HOST'] ?>"
 main()
</script>
