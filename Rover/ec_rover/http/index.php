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

<div class=roverview>
 <div class="webcam" class="">
  <img src="/cam/?action=stream" />
 </div>

 <canvas id="controlCanvas"></canvas>
</div>

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

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="/static/js/paper-full-min.js"></script>

<script type="text/paperscript" src="/main.paperscript.js" canvas="controlCanvas"></script>
<script type="text/javascript" src="/main.js"></script>

<script>
 ENDPOINT = "ws://<?php echo $_SERVER['HTTP_HOST'] ?>"
 main()
</script>
