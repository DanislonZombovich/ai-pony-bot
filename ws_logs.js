const WebSocket = require('ws');
const https = require('https');

function getWsCreds(callback) {
  const options = {
    hostname: 'control.heavencloud.in',
    path: '/api/client/servers/822fe758/websocket',
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ptlc_EP9hRjb7DE7HrSkyUlkyd8Yjz9zKUpa23MELHkjcOOk',
      'Accept': 'application/json'
    }
  };

  const req = https.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => { callback(JSON.parse(data).data); });
  });
  req.end();
}

getWsCreds((creds) => {
  const ws = new WebSocket(creds.socket, {
    origin: 'https://control.heavencloud.in'
  });

  ws.on('open', function open() {
    ws.send(JSON.stringify({"event":"auth","args":[creds.token]}));
    
    // Request logs ONLY (do not start)
    setTimeout(() => {
      ws.send(JSON.stringify({"event":"send logs","args":[null]}));
    }, 1000);
  });

  let logs = [];
  ws.on('message', function incoming(data) {
    const msg = JSON.parse(data);
    if (msg.event === 'console output') {
      logs.push(msg.args[0]);
    }
  });

  setTimeout(() => {
    ws.close();
    console.log(logs.slice(-100).join('\n'));
  }, 10000); 
});
