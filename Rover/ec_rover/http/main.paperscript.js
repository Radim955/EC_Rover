/* FOR DEBUGGING
var canvasOutlines = new Shape.Rectangle(new Point(0,0), new Size(view.bounds.width, view.bounds.height));
canvasOutlines.fillColor = '#FFFFFF';
canvasOutlines.strokeColor = '#445566';
canvasOutlines.strokeWidth = 1;
*/

tool.fixedDistance = 5;
var joySize = view.bounds.width*0.38;

var path;
var operationPath;
var pathReady = false;
var time = 100;
var sendMotorCommand = false;
var sendCamCommand = false;
var cPoint = new Point(view.size.width*0.5, view.size.height*0.95-joySize);
var mVector;
var vectorLine;
var outlineCircle = new paper.Path.Circle(cPoint, joySize);
var centerCircle = new paper.Path.Circle(cPoint, joySize*0.1);

var camControlOutline = new Shape.Rectangle(cPoint-new Point(joySize*0.166,joySize+joySize*1.5), new Size(joySize*0.33, joySize*1.2));
var camControlBar = new Shape.Rectangle(cPoint-new Point(joySize*0.166,joySize+joySize*1.5), new Size(joySize*0.33, joySize*0.05));

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
  if((event.point - cPoint).length < joySize*0.2){
    sendMotorCommand=true;
    mVector = event.point - cPoint;
    centerCircle.scaling = 1;
  } else if(camControlOutline.bounds.contains(event.point)){
    sendCamCommand=true;
    camControlBar.position.y = event.point.y;
  }
}

function onMouseDrag(event) {
  if(sendMotorCommand){
    mVector = event.point - cPoint;
    if(mVector.length > joySize) mVector.length = joySize;
    drawVector(mVector);
  } else if(camControlOutline.bounds.contains(event.point)){
    camControlBar.position.y = event.point.y;
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
  if(event.count % 20 == 0){
    if(sendMotorCommand){
        var force = (mVector.length/joySize);
        var m1Pow = 512*Math.sin(mVector.rotate(-45).angleInRadians);
        var m2Pow = 512*Math.cos(mVector.rotate(-45).angleInRadians);
	//var m1Pow = mVector.x / joySize;
	//var m2Pow = mVector.y / joySize;
        var m1Dir = "B";
        var m2Dir = "B";
        if(m1Pow < 0){
        m1Pow = -m1Pow;
        m1Dir = "F";
        }
        if(m2Pow < 0){
        m2Pow = -m2Pow;
        m2Dir = "F";
        }
	//console.log(m1Pow + " " + m2Pow);
        if(m1Pow >= 512) m1Pow = 512;
        if(m2Pow >= 512) m2Pow = 512;
        window.globals.sendData("M " + m1Dir + " " + Math.round((512-m1Pow)*force) + " " + time + " " + m2Dir + " " + Math.round((512-m2Pow)*force) + " " + time);
    } else if(sendCamCommand){
        var posY = 180*((camControlBar.position.y-camControlOutline.bounds.topLeft.y)/(camControlOutline.bounds.bottomLeft.y-camControlOutline.bounds.topLeft.y));
        console.log(posY);
        window.globals.sendData("C " + 0 + " " + Math.round(posY) + " OFF");
    }
  }
}

function drawVector(vector){
  var arrowVector = vector.normalize(20);
  var end = cPoint + vector;
  if(vectorLine) vectorLine.remove();
  vectorLine = new Group([
	new Path([cPoint, end]),
	new Path([
		end + arrowVector.rotate(135),
		end,
		end + arrowVector.rotate(-135)
	])
  ]);
  vectorLine.strokeWidth = 10;
  vectorLine.strokeColor = '#FFFFFF';
}
