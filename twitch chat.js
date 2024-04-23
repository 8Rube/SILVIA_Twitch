const http = require('http');
const url = require('url');

let ultimoMensaje = ''; // Variable

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);

    if (parsedUrl.pathname === '/obtener_ultimo_mensaje') {
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end(ultimoMensaje);
    } else {
        res.writeHead(404, {'Content-Type': 'text/plain'});
        res.end('Endpoint no encontrado');
    }
});

server.listen(3000, '127.0.0.1', () => {
    console.log('Servidor Node.js escuchando en http://127.0.0.1:3000/');
});

const tmi = require('tmi.js');

const client = new tmi.Client({
    channels: [ '', '' ] //Aqui puedes poner cuantos nombres quieras de canales de twitch para conectar con el chat
});

client.connect();

client.on('message', (channel, tags, message, self) => {
    // "Alca: Hello, World!"
    console.log(`${tags['display-name']}: ${message}`);
    ultimoMensaje = `${tags['display-name']}: ${message}`;

});