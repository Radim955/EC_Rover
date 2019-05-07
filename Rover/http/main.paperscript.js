/* FOR DEBUGGING
var canvasOutlines = new Shape.Rectangle(new Point(0,0), new Size(view.bounds.width, view.bounds.height));
canvasOutlines.fillColor = '#FFFFFF';
canvasOutlines.strokeColor = '#445566';
canvasOutlines.strokeWidth = 1;
*/

tool.fixedDistance = 10;
//var joySize = view.bounds.width*0.15;

var borderOffset = 20;
var joySize = 200;
var joySmallSize = 0.2 * (joySize / 2);

var barWidth = 200;
var barHeight = 0.2 * barWidth;
var barSmallWidth = 0.05 * barWidth;

// Point. From this position, Joystick is painted
var joyPoint = new Point((joySize / 2) + borderOffset, (joySize / 2) + borderOffset);
// Point. From this position, Bar for servo controling is painted
var barPoint = new Point(((view.size.width - barWidth) - borderOffset - 20), (joySize + borderOffset) / 2);

var path;
var operationPath;
var pathReady = false;
var time = 150;
var sendMotorCommand = false;
var sendCamCommand = false;
var mVector;
var vectorLine;
var keyCode = 0;

var lastServoPosition = 90;

// Joystick controll items
var outlineCircle = new paper.Path.Circle(joyPoint, (joySize / 2));
var centerCircle  = new paper.Path.Circle(joyPoint, (joySmallSize / 2));

// Servo controll items
var camControlOutline = new Shape.Rectangle(barPoint, new Size(barWidth, barHeight));
var camControlBar = new Shape.Rectangle(barPoint, new Size(barSmallWidth, barHeight));

centerCircle.fillColor = '#FFFFFF';
centerCircle.scaling = 2;
outlineCircle.strokeColor = '#445566';
outlineCircle.strokeWidth = 1;
outlineCircle.fillColor = '#778899';

camControlBar.fillColor = '#FFFFFF';
camControlOutline.strokeColor = '#445566';
camControlOutline.strokeWidth = 1;
camControlOutline.fillColor = '#778899';

function onMouseDown(event) {
  pathReady = false;
  if((event.point - joyPoint).length < joySize*0.1){
    sendMotorCommand=true;
    mVector = event.point - joyPoint;
    centerCircle.scaling = 1;
  } else if(camControlOutline.bounds.contains(event.point)){
    sendCamCommand=true;
    camControlBar.position.x = event.point.x;
  }
}

function onMouseDrag(event) {
  if(sendMotorCommand){
    mVector = event.point - joyPoint;
    if(mVector.length > joySize / 2) mVector.length = joySize / 2;
    drawVector(mVector);
  } else if(camControlOutline.bounds.contains(event.point)){
    camControlBar.position.x = event.point.x;
  }
}

function onMouseUp(){
  sendMotorCommand=false;
  if(vectorLine) vectorLine.remove();
  centerCircle.scaling = 2;
  /*
    if(!operationPath){
	operationPath = new Path()
	operationPath.strokeColor = '#00AAFF';
	operationPath.add(cPoint);
    }
    path.translate(operationPath.lastSegment.point - path.firstSegment.point);
    operationPath.addSegments(path.segments);
    pathReady = true;
    path.remove();
  */
}

function onFrame(event){
/*
  if(event.count % 20 == 0 && pathReady && operationPath && operationPath.length > tool.fixedDistance){
    var segment = operationPath.removeSegment(0)
    var nextSegment = operationPath.firstSegment;
    //operationPath.rotate(90-(cPoint - operationPath.getPointAt(tool.fixedDistance-1)).angle);
    operationPath.translate(cPoint-nextSegment.point);
    mVector = operationPath.getPointAt(tool.fixedDistance-1) - cPoint;
    mVector.length = joySize/2;
    drawVector(mVector);
  }
*/
  //Translate mVector values into motor powers and directions
  if(event.count % 5  == 0){
    if(sendMotorCommand){/*
        var force = (mVector.length/(joySize / 2));
        var m1Pow = 512*Math.sin(mVector.rotate(-45).angleInRadians);
        var m2Pow = 512*Math.cos(mVector.rotate(-45).angleInRadians);
	console.log("force " + force + " m1 " + m1Pow + " m2 " + m2Pow);*/


	//var m1Pow = mVector.x / joySize;
	//var m2Pow = mVector.y / joySize;
        var m1Pow = 512;
        var m2Pow = 512;
        var m1Dir = "F";
        var m2Dir = "F";
        if(m1Pow < 0){
        m1Pow = -m1Pow;
        m1Dir = "B";
        }
        if(m2Pow < 0){
        m2Pow = -m2Pow;
        m2Dir = "B";
        }

        switch(keyCode) {
            case 37:
                m1Dir = "B";
                break;
            case 38:
                break;
            case 39:
                m2Dir = "B";
                break;
            case 40:
                m1Dir = "B";
                m2Dir = "B";
                break;
        }
	//console.log(m1Pow + " " + m2Pow);
        if(m1Pow >= 512) m1Pow = 512;
        if(m2Pow >= 512) m2Pow = 512;
        window.globals.sendData("M " +  m2Dir + " " + (Math.round((512-m2Pow)*force) * 2) + " " + time + " " + m1Dir + " " + (Math.round((512-m1Pow)*force) * 2)  + " " + time);
    } else if(sendCamCommand){
        var posX = 180*((camControlBar.position.x-camControlOutline.bounds.topLeft.x)/(camControlOutline.bounds.topRight.x-camControlOutline.bounds.topLeft.x));
        if(posX == lastServoPosition)
        {
            return;
	}
	lastServoPosition = posX;
	document.getElementById("Degrees").innerHTML = "Degrees: " + (Math.round(-1 * (90 - posX)).toString());
// 	console.log(posX);
//	console.log(camControlBar.position.X);
//	console.log(camControlOutline.bounds.topLeft.x);
//	console.log(camControlOutline.bounds.topRight.x);
        window.globals.sendData("S " + (180 - Math.round(posX)) + " " + (180 - Math.round(posX)));
    }
  }
}

function drawVector(vector){
  var arrowVector = vector.normalize(20);
  var end = joyPoint + vector;
  if(vectorLine) vectorLine.remove();
  vectorLine = new Group([
	new Path([joyPoint, end]),
	new Path([
		end + arrowVector.rotate(135),
		end,
		end + arrowVector.rotate(-135)
	])
  ]);
  vectorLine.strokeWidth = 10;
  vectorLine.strokeColor = '#FFFFFF';
}

document.onkeydown = function(event) {
    if (event.key == 37 || event.key == 38 || event.key == 39 || event.key == 40){
        keyCode = event.key;
        sendMotorCommand = true;
    }
    /*switch (event.key) {
        case 37:
            Left
            break;
        case 38:
            alert('Up key pressed');
            break;
        case 39:
            alert('Right key pressed');
            break;
        case 40:
            alert('Down key pressed');
            break;
    }*/
};
