var trashObjs = new Array(); // Array of image objects
var falseAlarmObjs = new Array(); // Array of false alarm objects (components)

var aluminumCan = new Array(); // Array of aluminumCan image sources
var numberOfImgs = 10;
for (i = 1; i <= numberOfImgs; i++) {
  aluminumCan.push("aluminumCan/can (" + i + ").png");
}

var cardboard = new Array(); // Array of cardboard image sources
numberOfImgs = 10;
for (i = 1; i <= numberOfImgs; i++) {
  cardboard.push("cardboard/cardboard (" + i + ").png");
}

var carton = new Array(); // Array of carton image sources
numberOfImgs = 10;
for (i = 1; i <= numberOfImgs; i++) {
  carton.push("carton/carton (" + i + ").png");
}

var glassBottle = new Array(); // Array of glassBottle image sources
numberOfImgs = 9;
for (i = 1; i <= numberOfImgs; i++) {
  glassBottle.push("glassBottle/glassBottle (" + i + ").png");
}

var paper = new Array(); // Array of paper image sources
numberOfImgs = 21;
for (i = 1; i <= numberOfImgs; i++) {
  paper.push("paper/paper (" + i + ").png");
}

var paperBag = new Array(); // Array of paperBag image sources
numberOfImgs = 15;
for (i = 1; i <= numberOfImgs; i++) {
  paperBag.push("paperBag/paperBag (" + i + ").png");
}

var plasticBag = new Array(); // Array of plasticBag image sources
numberOfImgs = 23;
for (i = 1; i <= numberOfImgs; i++) {
  plasticBag.push("plasticBag/plasticBag (" + i + ").png");
}

var plasticBottle = new Array(); // Array of plasticBottle image sources
numberOfImgs = 12;
for (i = 1; i <= numberOfImgs; i++) {
  plasticBottle.push("plasticBottle/plasticBottle (" + i + ").png");
}

var reject = new Array(); // Array of rejects image sources
numberOfImgs = 20;
for (i = 1; i <= numberOfImgs; i++) {
  reject.push("reject/reject (" + i + ").png");
}

var imgs = aluminumCan.concat(
  cardboard,
  carton,
  glassBottle,
  paper,
  paperBag,
  plasticBag,
  reject
);

// Audio import and looping

//Trash bin object
//var trashBin = new Component(150, 150, 525, 15, 'darkgreen')

var trashBin;
var endPiece;
var endPiece2;
var endPiece3;
var detector;

// Scoreboard object and clock object
var scoreboard;
var timer;
var time = "";
var finalInfo;
var clickToMoveOn;

var startBtn;
var convBeltImg;
var convBeltImg2;
var convBeltImgA;
var convBeltImgA2;
var convBeltImgB;
var convBeltImgB2;

// If mouse is clicked and mouse is intersecting a valid object
var dragOk = false;
var toDrag;

// Score var and time vars
var score = 100;
var gameOver = false;
var gameStart = false;
var timeLeft;
// Function that counts down the timer

var userEvents = {};
userEvents.seed = Math.seed;
var prevEvent;
var recorded;


if (!isFinite(testCase) || isNaN(testCase)) {
  sessionStorage.case = 2;//getRandomInt(0, 3); //Min (inclusive) Max (exclusive)
  testCase = sessionStorage.case;
}

if (!isFinite(roundNum) || isNaN(testCase)) {
  console.warn("Round Number Was Undefined... Resetting Round Number To Zero.");
  sessionStorage.roundNum = 0;
  roundNum = 0;
}

console.log("Test Case: " + testCase);
console.log("Current Round Num: " + roundNum);

totalObjects = -11;
totalRejects = 0;
detectedRejects = 0;
detectedFp = 0;

function startConveyers() {
  // eslint-disable-line no-unused-vars
  myConveyer.start();
  myConveyer.canvas.onmousedown = myDown;
  myConveyer.canvas.onmouseup = myUp;

  var cnv = myConveyer.canvas;

  trashBin = new ImgComponent(
    cnv.width / 2 - 75,
    15,
    "trashbin.png",
    0,
    0,
    0,
    150,
    150
  );

  //endPiece = new Component(50, 160, cnv.width - 50, 185, 'black')
  endPieceImg = new ImgComponent(
    cnv.width - 80, //x
    150, //y
    "undergroundConvBelt.png",
    0,
    0,
    0,
    100, //width
    200 //height
  );
  //endPiece2 = new Component(w = 50, h = 160, x = cnv.width - 50, y = 385, col='black')
  endPieceImg2 = new ImgComponent(
    cnv.width - 80,
    350,
    "undergroundConvBelt.png",
    0,
    0,
    0,
    100,
    200
  );
  //endPiece3 = new Component(50, 160, cnv.width - 50, 585, 'black')
  endPieceImg3 = new ImgComponent(
    cnv.width - 80,
    550,
    "undergroundConvBelt.png",
    0,
    0,
    0,
    100,
    200
  );
  detector = new Component(5, 800, cnv.width, 0, "white");

  scoreboard = new textComp("Score: 0", cnv.width - 200, 50);
  timer = new textComp(
    "Round " +
    Number(sessionStorage.roundNum) +
    " of 3\r\n Remaining Time: 5:00",
    50,
    50
  );

  sliderT = new textComp("threshold: 5", cnv.width / 3 - 200, 50);
  sliderM = new textComp("Mean: 5", cnv.width * (2 / 3), 50);

  startBtn = new ImgComponent(
    cnv.width / 2 - 175,
    300,
    "startBtn.png",
    0,
    0,
    0,
    350
  );
  convBeltImg = new ImgComponent(
    -50,
    185,
    "ConvBeltNew.png",
    0,
    0,
    0,
    cnv.width + 150,
    160
  );
  convBeltImg2 = new ImgComponent(
    -50,
    185,
    "ConvBeltNew2.png",
    0,
    0,
    0,
    cnv.width + 150,
    160
  );
  convBeltImgA = new ImgComponent(
    -50,
    385,
    "ConvBeltNew.png",
    0,
    0,
    0,
    cnv.width + 150,
    160
  );
  convBeltImgA2 = new ImgComponent(
    -50,
    385,
    "ConvBeltNew2.png",
    0,
    0,
    0,
    cnv.width + 150,
    160
  );
  convBeltImgB = new ImgComponent(
    -50,
    585,
    "ConvBeltNew.png",
    0,
    0,
    0,
    cnv.width + 150,
    160
  );
  convBeltImgB2 = new ImgComponent(
    -50,
    585,
    "ConvBeltNew2.png",
    0,
    0,
    0,
    cnv.width + 150,
    160
  );

  finalInfo = new textComp("Time's up!", cnv.width / 2, 300);

  detectorOff = new textComp(
    "The Detector has been Turned off!",
    cnv.width / 2 - 300,
    250
  );

  clickToMoveOn = new textComp(
    "Click Anywhere to move onto the next part",
    cnv.width / 2 - 375,
    400
  );
}

function ImgComponent(x, y, src, speedx = 0, speedy = 0, rot = 0, width = 100, height = 100) {
  this.img = new Image(width, height);
  if (src != undefined) {
    this.img.src = src;
    this.class = src.split("/")[0];
  } else {
    console.warn("Potential image may be missing from AWS Bucket.");
  }

  this.rot = (rot * Math.PI) / 180;
  this.height = this.img.height;
  this.width = this.img.width;
  this.detected = false;
  this.speedx = speedx;
  this.speedy = speedy;
  totalObjects++;
  this.x = x;
  this.y = y;

  if (this.class == "reject") {
    totalRejects++;
    this.rejectProbNum = Math.random();
    this.fpProb = 1;

    //Non-Recyclable
    this.confScore = getBetaDistribution(4.675, 2);
  } else {
    this.rejectProbNum = 1;
    this.fpProb = Math.random();

    //Recyclable
    this.confScore = getBetaDistribution(2, 4.675);
  }

  if (this.rejectProbNum < rejectProb && this.confScore > hitTHRESHOLD) {
    detectedRejects++;
  } else if (this.fpProb < fpProb && this.confScore > fpTHRESHOLD) {
    detectedFp++;
  }
  this.hitbox = {
    x: x + width / 2,
    y: y + height / 2,
    radius: 50,
    color: "white",
  };
  this.draggie = {
    x: 0,
    y: 0,
  };
  this.update = function () {
    var ctx = myConveyer.context;
    if (this.rot) {
      ctx.save();
      ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
      ctx.rotate(this.rot);
      ctx.drawImage(this.img, this.width / -2, this.height / -2, this.width, this.height);
      ctx.restore();
    } else {
      ctx.drawImage(this.img, this.x, this.y, this.width, this.height);
    }
  };
  this.newPos = function () {
    this.x += this.speedx;
    this.y += this.speedy;
    this.hitbox.x += this.speedx;
    this.hitbox.y += this.speedy;
  };
  this.setPos = function (x, y) {
    this.x = x;
    this.y = y;
    this.hitbox.x = x + this.width / 2;
    this.hitbox.y = y + this.height / 2;
  };
}

var myConveyer = {
  canvas: document.createElement("canvas"),
  sliderT: document.createElement("input"),
  sliderM: document.createElement("input"),
  start: function () {
    this.canvas.width = window.innerWidth;
    this.canvas.height = document.body.offsetHeight;
    this.context = this.canvas.getContext("2d");
    this.canvas.id = "myConveyerCanvas";
    this.frameNo = 0;
    this.startArea = document.getElementById("startArea");
    this.startArea.appendChild(this.canvas);

    this.interval = setInterval(updateConveyer, 10)
    window.addEventListener("mousemove", function (e) {
      var coords = myConveyer.getMousePos(
        document.getElementById("myConveyerCanvas"),
        e
      );
      myConveyer.x = coords.x;
      myConveyer.y = coords.y;
    });
  },
  everyInterval: function (n) {
    if ((myConveyer.frameNo / n) % 1 === 0) {
      return true;
    }
    return false;
  },
  getMousePos: function (canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top,
    };
  },
  getCanvasPos: function (canvas) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: rect.left,
      y: rect.top,
    };
  },
  clear: function () {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
  },
};

function Component(width, height, x, y, color) {
  this.width = width;
  this.height = height;
  this.x = x;
  this.y = y;
  this.speedx = 0;
  this.speedy = 0;
  this.color = color;
  this.update = function (rot = 0) {
    var ctx = myConveyer.context;
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
  };
  this.newPos = function () {
    this.x += this.speedx;
    this.y += this.speedy;
  };
}

function textComp(text, x, y, color) {
  this.text = text;
  this.x = x;
  this.y = y;
  this.color = color;
  this.font = "40px Arial";
  this.width = myConveyer.context.measureText(this.text).width;
  this.update = function () {
    var ctx = myConveyer.context;
    ctx.fillStyle = "black";
    ctx.font = this.font;
    ctx.fillText(this.text, this.x, this.y);
  };
  this.changeText = function (text) {
    this.text = text;
  };
}

var prev;
var do1 = true;

function falseAlarm(cx, cy, w, h, color, speedx = 0, speedy = 0) {
  this.width = w;
  this.height = h;
  this.cx = cx;
  this.cy = cy;
  this.speedx = speedx;
  this.speedy = speedy;
  this.color = color;
  this.update = function () {
    var ctx = myConveyer.context;
    if (!softHighlight) {
      ctx.beginPath();
      ctx.rect(this.cx - this.width / 2, this.cy - this.height / 2, this.width, this.height);
      ctx.lineWidth = 7;
      ctx.strokeStyle = color;
      ctx.stroke();
    } else {
      var size = sampleDistribution(Math.random(), faSizeProbDist);
      var conf = getBetaDistribution(2, 4.675);
      drawGrad(ctx, this.cx, this.cy, size, conf);
    }
  };
  this.newPos = function () {
    this.cx += this.speedx;
    this.cy += this.speedy;
  };
}

function updateConveyer() {
  myConveyer.clear();

  if (!gameStart) {
    if (noDetect) {
      detectorOff.update();
    }
    startBtn.update();
    return;
  } else if (gameOver) {
    myConveyer.frameNo++;
    finalInfo.update();
    clickToMoveOn.update();
    if (myConveyer.frameNo == prev + 50) {
      do1 = !do1;
      prev = myConveyer.frameNo;
    }
    if (do1) {
      scoreboard.update();
      timer.update();
    }
    return;
  }

  myConveyer.frameNo++;
  if (myConveyer.everyInterval(50)) {
    trashObjs.push(
      new ImgComponent(
        -100 - getRandomInt(0, 150),
        200,
        imgs[getRandomInt(0, imgs.length)],
        3,
        0,
        getRandomInt(-90, 90)
      )
    );
    trashObjs.push(
      new ImgComponent(
        -100 - getRandomInt(0, 150),
        600,
        imgs[getRandomInt(0, imgs.length)],
        4,
        0,
        getRandomInt(-90, 90)
      )
    );
    trashObjs.push(
      new ImgComponent(
        -100 - getRandomInt(0, 150),
        400,
        imgs[getRandomInt(0, imgs.length)],
        2,
        0,
        getRandomInt(-90, 90)
      )
    );
  }

  if (myConveyer.everyInterval(10) && avgFa > 0) {
    falseAlarmObjs = [];
    //Sample number of false alarms every 50 frames
    numFalseAlarmsToAdd = randn_bm() + avgFa;
    //console.log(numFalseAlarmsToAdd)
    for (i = 0; i < numFalseAlarmsToAdd; i++) {
      var c = sampleDistribution(Math.random(), facLocDist);
      var size = sampleDistribution(Math.random(), faSizeProbDist);
      var conf = getBetaDistribution(2, 4.675); // sampleDistribution(Math.random(), faConfDist)
      var speedx = 0;

      falseAlarmObjs.push(
        new falseAlarm(
          c.one,
          c.two,
          size.one,
          size.two,
          "rgba(255, 0, 0, 1)",
          speedx
        )
      );
    }
  }

  if (myConveyer.x && myConveyer.y) {
    if (dragOk && toDrag) {
      toDrag.setPos(
        myConveyer.x - toDrag.draggie.x,
        myConveyer.y - toDrag.draggie.y
      );
    }
  }

  for (i = 0; i < trashObjs.length; i++) {
    if (fullIntersection(trashObjs[i], detector)) {
      if (trashObjs[i].class == "reject") {
        score--;
        errorSound.play();
      }
    }
  }

  if (myConveyer.everyInterval(2)) {
    convBeltImg.update();
  } else {
    convBeltImg2.update();
  }
  if (myConveyer.everyInterval(2)) {
    convBeltImgA.update();
  } else {
    convBeltImgA2.update();
  }
  if (myConveyer.everyInterval(2)) {
    convBeltImgB.update();
  } else {
    convBeltImgB2.update();
  }

  trashBin.update();
  for (i = 0; i < trashObjs.length; i++) {
    trashObjs[i].newPos();
    trashObjs[i].update();
  }
  for (i = 0; i < falseAlarmObjs.length; i++) {
    falseAlarmObjs[i].newPos();
    falseAlarmObjs[i].update();
  }
  endPieceImg.update();
  endPieceImg2.update();
  endPieceImg3.update();
  scoreboard.changeText("Score: " + score);
  scoreboard.update();
  timer.changeText("Round " + Number(sessionStorage.roundNum) + " of 3\r\n Remaining Time: " + time);
  timer.update();

  //console.log(timeLeft);
  if (timeLeft < 0 || score <= 0) {
    if (timeLeft < 0) {
      timer.changeText("Round " + Number(sessionStorage.roundNum) + " of 3\r\n Remaining Time: 0:00");
      finalInfo.changeText("Time's up!");
      finalInfo.x = myConveyer.canvas.width / 2 - finalInfo.width / 2;
    } else {
      finalInfo.changeText("Your score fell to Zero!");
      finalInfo.width = myConveyer.context.measureText(finalInfo.text).width;
      finalInfo.x = myConveyer.canvas.width / 2 - finalInfo.width / 2;
    }
    gameOver = true;
    prev = myConveyer.frameNo;

    for (i = 0; i < trashObjs.length; i++) {
      if (trashObjs[i].speedx == 0) {
        score--;
      }
    }
    scoreboard.changeText("Score: " + score);

    $("#startArea").click(function () {
      //add game data to session storage
      userEvents.totalObjects = totalObjects;
      userEvents.totalRejects = totalRejects;
      userEvents.detectedRejects = detectedRejects;
      userEvents.detectedFp = detectedFp;
      sessionStorage["userEvents" + sessionStorage.roundNum] =
        JSON.stringify(userEvents);
      sessionStorage["score" + sessionStorage.roundNum] = score;
      sessionStorage["timeRemaining" + sessionStorage.roundNum] = timeLeft;
      sessionStorage["rejectProb" + sessionStorage.roundNum] = rejectProb;
      sessionStorage["fpProb" + sessionStorage.roundNum] = fpProb;
      sessionStorage.roundNum++;
      if (sessionStorage.roundNum >= MAX_ROUND_NUM) {
        location.href = "outPage.html";
      } else {
        location.href = "conveyer.html";
      }
    });
  }
}
function randn_bm() {
  var u = 0,
    v = 0;
  while (u === 0) u = Math.random(); //Converting [0,1) to (0,1)
  while (v === 0) v = Math.random();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
}

function recordEvent(type, x1, y1, w, h, detected, confScore) {
  userEvents["event" + myConveyer.frameNo] = {
    type: type,
    w: w,
    h: h,
    x1: x1,
    y1: y1,
    pickupFrameNo: myConveyer.frameNo,
    detected: detected,
    confScore: confScore
  };
  prevEvent = "event" + myConveyer.frameNo;
}

function checkIntersection(arr, x, y) {
  for (i = arr.length - 1; i >= 0; i--) {
    if (intersection(arr[i], x, y)) {
      return arr[i];
    }
  }
  return false;
}

function intersection(imgComp, x, y) {
  var dist = Math.sqrt(
    Math.pow(Math.abs(imgComp.hitbox.x - x), 2) +
    Math.pow(Math.abs(imgComp.hitbox.y - y), 2)
  );
  if (dist < imgComp.hitbox.radius) {
    return true;
  } else {
    return false;
  }
}

function fullIntersection(imgComp, comp) {
  if (imgComp.hitbox.x > comp.x && imgComp.hitbox.x < comp.x + comp.width &&
    imgComp.hitbox.y > comp.y && imgComp.hitbox.y < comp.y + comp.height) {
    return true;
  } else {
    return false;
  }
}

function myDown(e) {
  dragOk = true;
  toDrag = checkIntersection(trashObjs, myConveyer.x, myConveyer.y);
  if (!gameStart) {
    if (intersection(startBtn, myConveyer.x, myConveyer.y)) {
      gameStart = true;

      //If round 0, set timer to 1 minute
      var timerMin = 3;
      if (sessionStorage.roundNum == 0) {
        timerMin = 1;
      }

      var countDownTime = new Date(new Date().getTime() + timerMin * 60000);
      var timerX = setInterval(function () {
        var now = new Date().getTime();
        timeLeft = countDownTime - now;

        var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        if (seconds % 100 < 10) {
          seconds = "0" + seconds;
        }

        time = minutes + ":" + seconds;
      });
    }
  }
  if (toDrag) {
    if (!recorded) {
      recordEvent(
        toDrag.class,
        myConveyer.x / window.innerWidth,
        myConveyer.y,
        toDrag.width,
        toDrag.height,
        toDrag.detected,
	toDrag.confScore
      );
      recorded = true;
    }
    toDrag.draggie.x = myConveyer.x - toDrag.x;
    toDrag.draggie.y = myConveyer.y - toDrag.y;
    toDrag.speedx = 0;
  }
}

function myUp(e) {
  dragOk = false;
  if (toDrag) {
    if (recorded) {
      userEvents[prevEvent].x2 = myConveyer.x / window.innerWidth;
      userEvents[prevEvent].y2 = myConveyer.y;
      userEvents[prevEvent].dropFrameNo = myConveyer.frameNo;
      recorded = false;
    }
    var center_y = toDrag.y + toDrag.height / 2;
    if (center_y > 200 && center_y < 300) {
      toDrag.speedx = 3;
    } else if (center_y > 400 && center_y < 500) {
      toDrag.speedx = 2;
    } else if (center_y > 600 && center_y < 700) {
      toDrag.speedx = 4;
    } else if (fullIntersection(toDrag, trashBin)) {
      if (toDrag.class != "reject") {
        score--;
        errorSound.play();
      } else {
        correctSound.play();
      }
      trashObjs.splice(trashObjs.indexOf(toDrag), 1);
      //myAudio.pause()

    }
  }
  toDrag = false;
}

// rnd is a number between 0 and 1
// dist is a distribution in a JSON format ordered from smallest probability to largest
// returns object with the lower (one) and upper (two) bounds if sampling confidence, x (one) y (two) if sampling center, dcx (one) dcy (two) if sampling center offset, w (one) h (two) if sampling size
function sampleDistribution(rnd, dist) {
  var ret = {};
  var prevProb = 0;
  $.each(dist, function (k, val) {
    prevProb += Number(k);
    if (rnd < prevProb) {
      (ret["one"] = Number(val.slice(0, val.indexOf(",")))),
        (ret["two"] = Number(val.slice(val.indexOf(",") + 1)));
      return false;
    }
  });
  return ret;
}

var redRect = new Image(100, 100);
redRect.src = "RedRect.png";

function drawGrad(ctx, x, y, size, conf) {
  // outerCircleRadius = 40;
  // innerCirlceRadius = 8;

  //var grd = ctx.createRadialGradient(xGradPos, yGradPos, outerCircleRadius, xGradPos, yGradPos, innerCirlceRadius);
  //grd.addColorStop(0, "rgba(255, 0, 0, 0)");
  //grd.addColorStop(1, color);

  if (isNaN(x) || isNaN(y) || isNaN(size.one) || isNaN(size.two)) {
    return;
  }


  ctx.beginPath();
  ctx.rect(x, y, size.one, size.two);
  ctx.lineWidth = 7;
  ctx.strokeStyle = "rgba(255, 0, 0, " + conf + ")";
  ctx.stroke();


  //ctx.fillStyle = "rgba(255, 0, 0, " + conf + ")";
  //ctx.fillRect(x, y, size.one, size.two);
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

function getBetaDistribution(alpha, beta) {
  return d3.randomBeta(alpha, beta)();
}
