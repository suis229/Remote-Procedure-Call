const net = require('net');
const SOCKET_PATH = '/tmp/rpc_socket';

function sendRequest(method, params, paramTypes, id) {
    const client = new net.Socket();
    const request = {
        method: method,
        params: params,
        param_types: paramTypes,
        id: id
    };

    client.connect(SOCKET_PATH, () => {
        client.write(JSON.stringify(request));
    });

    client.on('data', (data) => {
        const response = JSON.parse(data);
        console.log('Response:', response);
        client.destroy();
    });

    client.on('close', () => {
        console.log('Connection closed');
    });
}

// 例
sendRequest('floor', [3.14], ['float'], 1);
sendRequest('reverse', ['hello'], ['string'], 2);
