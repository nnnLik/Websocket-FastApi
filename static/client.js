var connection = new WebSocket('ws://0.0.0.0:8000/signsense/video');

connection.onopen = function () {
    console.log('Connected to WebSocket server.');
    connection.send('Hello from JavaScript!');
};

connection.onerror = function (error) {
    console.log('WebSocket Error', error);
};

connection.onmessage = function (e) {
    var data = JSON.parse(e.data);
    // Do whatever you need with data here
}