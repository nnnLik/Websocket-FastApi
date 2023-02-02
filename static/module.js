
const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');

// document.getElementById('button').addEventListener('click', ()=>socket.close())
// let socket = new WebSocket('ws://localhost:8050/signsense/video');
let socket = new WebSocket('ws://5scontrol.pl/signsense/video');

socket.onopen = function () {
    console.log('Connected to WebSocket server.');
}

socket.onclose = function(event) {
  if (event.wasClean) {
    console.log('Соединение закрыто чисто');
  } else {
    console.log('Обрыв соединения'); // например, "убит" процесс сервера
  }
  console.log('Код: ' + event.code + ' причина: ' + event.reason);
};
socket.onerror = function (error) {
    console.log('WebSocket Error', error);
};

socket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    console.log(data)
    // Do whatever you need with data here
}

// window.onbeforeunload = function() {
//   websocket.onclose = function () {}; // disable onclose handler first
//   websocket.close();
// };

function onResults(results) {
  socket.send(JSON.stringify(
            {
              poseLandmarks:results.poseLandmarks ? results.poseLandmarks : NaN, 
              leftHandLandmarks:results.leftHandLandmarks ? results.leftHandLandmarks : NaN, 
              rightHandLandmarks:results.rightHandLandmarks ? results.rightHandLandmarks : NaN
            }));
  let allVisibleLandmarks = results.poseLandmarks?.map((el)=>el.visibility>0.0001?{...el, visibility:1}:el)
      .map((e,index)=>(index>10 && index<17) || (index>22)?e:{...e, visibility:0})
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

  // Only overwrite existing pixels.
  canvasCtx.globalCompositeOperation = 'source-in';
  canvasCtx.fillStyle = '#00FF00';
  canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

  // Only overwrite missing pixels.
  canvasCtx.globalCompositeOperation = 'destination-atop';
  canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);

  canvasCtx.globalCompositeOperation = 'source-over';
  drawConnectors(canvasCtx, allVisibleLandmarks, POSE_CONNECTIONS,
                 {color: 'white', lineWidth: 4});
  drawLandmarks(canvasCtx, allVisibleLandmarks,
                {color: 'orange', lineWidth: 2});
  drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS,
                 {color: 'white', lineWidth: 2});
  drawLandmarks(canvasCtx, results.leftHandLandmarks,
                {color: 'orange', radius: 3});
  drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS,
                 {color: 'white', lineWidth: 2});
  drawLandmarks(canvasCtx, results.rightHandLandmarks,
                {color: 'orange', radius: 3});
  canvasCtx.restore();
  
}

const holistic = new Holistic({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
}});
holistic.setOptions({
  selfiMode:true,
  modelComplexity: 1,
  smoothLandmarks: true,
  enableSegmentation: false,
  smoothSegmentation: true,
  refineFaceLandmarks: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});
holistic.onResults(onResults);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await holistic.send({image: videoElement});
  },
  width: 1280,
  height: 720
});
camera.start();