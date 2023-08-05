"use strict";

var oReq = new XMLHttpRequest();

function padZeros(number, pad) {
  return ("0".repeat(pad) + number).toString().substr(-pad, pad)
}

function formatTime(total_seconds) {

  let total_minutes = Math.floor(total_seconds / 60);
  let seconds = total_seconds % 60;
  let hours = Math.floor(total_minutes / 60);
  let minutes = total_minutes % 60;

  let time_start = padZeros(hours, 2) + ":" +
                   padZeros(minutes, 2) + ":" +
                   padZeros(seconds, 2);

  return time_start;
}

function createFrameData(jsonObj) {
  var container = document.getElementById("container");
  var frame_info = document.getElementById("frame-default");
  var fps = jsonObj['meta'][0]['fps'];

  for(var i = 0; i < jsonObj.cut.length; i++) {
    let cln = frame_info.cloneNode(true);
    cln.style = "";

    let frame_num = jsonObj.cut[i]['mpoint'];
    let time_start = Math.floor(jsonObj.cut[i]['frame_start'] / fps);
    let time_end = Math.floor(jsonObj.cut[i]['frame_end'] / fps);
    let lobj = jsonObj['length'][i];

    cln.children[0].children[0].src =
      'img-display/frame-' + padZeros(frame_num, 6) + ".png";
    cln.children[0].children[1].src =
      'img-flow/frame-' + padZeros(frame_num, 6) + ".png";
    cln.children[0].children[0].id = 'img' + (frame_num).toString();

    let ulist = cln.children[1].children[0].children;
    ulist[0].children[1].textContent = formatTime(time_start);
    ulist[1].children[1].textContent = formatTime(time_end);
    ulist[2].children[1].textContent = lobj['num_faces'].toString();
    ulist[3].children[1].textContent = lobj['num_people'].toString();
    ulist[4].children[1].textContent = lobj['objects'].toString();
    ulist[5].children[1].textContent = lobj['shot_length'].toString();
    ulist[6].children[1].textContent = lobj['people'].toString();

    container.appendChild(cln);
  }
}

oReq.onreadystatechange = function () {
  var DONE = this.DONE || 4;
  if (this.readyState === DONE){
    createFrameData(JSON.parse(this.responseText));
    document.getElementById("help").style = "display: none;";

  }
};

oReq.open("GET", "data.json");
oReq.send(null);
