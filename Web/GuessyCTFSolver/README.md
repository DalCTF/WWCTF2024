# Guessy CTF Solver

## Analysis

In this problem we receive the code for an Express.JS API with a single endpoint: /hack.
This endpoint received a URL along with paths that will be loaded using the `happy-dom` library and will be searched for flags following the format `PREFIX{...}` (by default `wwf{...}`).

The API restricts its use to the domain `https://fake-easy-chall.wwctf.com`, meaning that we would be restricted to investigating paths on this domain. This website also only returns fake flags, whichever the path may be.

Finally, the problem statement gives us the hint that the flag we are looking for is in "/flag.txt". This, we quickly find out, does not refer to a URL path. Leaving us to believe that this is a file on disk.

## Solution

The first thing we notice is that the URL to be analyzed is built using the `new URL(...)` constructor, which takes a `path` and a `base` and combines the two. However, if the `path` is itself a full URL, then the base is ignored. This means that we can send the `url` parameter of the request as `https://fake-easy-chall.wwctf.com`, to bypass the system's restriction, but send a full URL as part of our `path` to make the system investigate whatever URL we want.

Despite being able to investigate any URL, there is no clear location that we should explore. By digging around a bit we can find that the `happy-dom` extension, used for loading the webpage, recently had an issue created about a [RCE vulnerability](https://security.snyk.io/vuln/SNYK-JS-HAPPYDOM-8350065). We could guess that the server is running a vulnerable version of this library, meaning that we could use this exploit to read the file on disk.

To serve the exploit we can start an HTTP server using Python (`python3 -m http.server 8000`) and use a tool like `ngrok` to create a publicly available endpoint to serve the [exploit file](Attack/RCE.html). The file attempts to make a request to the same server that we are using to serve the exploit file, but appending the result of the RCE to the URL. That means we can exfiltrate content by reading the requests being made to our server.

A last hurdle to overcome is that if we try to execute a command like `cat /flag.txt`, that will get escaped into `cat%20/flag.txt` due to URL encoding. If this is executed, we get a `Command not found` error. To overcome that, we can make use of an environment variable whose value is, by default, a single space: `$IFS`. Therefore, the command we pass to the RCE is `cat$IFS/flag.txt`. By reading the log of requests made to the server, we get the flag.
