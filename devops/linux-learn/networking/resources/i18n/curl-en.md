<!-- source_blob: 33fadc496c58ab1f990e2529b6b8e25157c36c3f -->

# Before we begin

When I was working as an Azure support engineer, I often dealt with products such as Azure Application Gateway (APG) and Azure Front Door (AFD), mainly these two. I was constantly using the `curl` command to test website connectivity and similar scenarios, so I spent some time studying `curl` and decided to record what I learned here.

# The `curl` command

The options and parameters I use most often are `-i -v`, because they let me see all the important information. For example:

```bash
curl -i -v https://www.google.com:443
```

```bash
* Trying 209.85.203.104:443...
* TCP_NODELAY set
* Connected to www.google.com (209.85.203.104) port 443 (#0)
* ALPN, offering h2
* ALPN, offering http/1.1
* successfully set certificate verify locations:
*   CAfile: /etc/ssl/certs/ca-certificates.crt
  CApath: /etc/ssl/certs
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN, server accepted to use h2
* Server certificate:
*  subject: CN=www.google.com
*  start date: Oct 21 08:38:45 2024 GMT
*  expire date: Jan 13 08:38:44 2025 GMT
*  subjectAltName: host "www.google.com" matched cert's "www.google.com"
*  issuer: C=US; O=Google Trust Services; CN=WR2
*  SSL certificate verify ok.
* Using HTTP2, server supports multi-use
* Connection state changed (HTTP/2 confirmed)
* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
* Using Stream ID: 1 (easy handle 0x564c4348b0e0)
> GET / HTTP/2
> Host: www.google.com
> user-agent: curl/7.68.0
> accept: */*
>
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
* Connection state changed (MAX_CONCURRENT_STREAMS == 100)!
< HTTP/2 200
HTTP/2 200
```

# Analysis of the output

## Initial connection

### 1. Initial connection phase
```bash
* Trying 209.85.203.104:443...
* TCP_NODELAY set
* Connected to www.google.com (209.85.203.104) port 443 (#0)
```
- First, it tries to connect to Google's IP address (`209.85.203.104`) on port `443` (the default HTTPS port).
- `TCP_NODELAY` is enabled. This is a TCP option used to disable the Nagle algorithm.
- The TCP connection is established successfully.

### 2. ALPN (Application-Layer Protocol Negotiation)
```bash
* ALPN, offering h2
* ALPN, offering http/1.1
```
- The client tells the server which protocols it supports: HTTP/2 (`h2`) and HTTP/1.1.
- ALPN is a TLS extension that allows the client and server to negotiate the application-layer protocol during the handshake.

### 3. SSL certificate configuration
```bash
* successfully set certificate verify locations:
*   CAfile: /etc/ssl/certs/ca-certificates.crt
  CApath: /etc/ssl/certs
```
- `curl` uses the system CA certificate store to verify the server certificate.
- It specifies the locations of the certificate file and certificate directory.

## TLS handshake process
```bash
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
```

### `(OUT)` and `(IN)`

- `OUT`: data sent from the client (outgoing)
- `IN`: data received from the server (incoming)

### Message Type

The numbers in parentheses are the Message Types defined in the TLS protocol. In TLS, messages are divided into different protocol types (Content Types), and each type contains its own message types. The main protocol types are:

```
TLS Protocol
├── Handshake Protocol (22)
│   ├── Client Hello (1)
│   ├── Server Hello (2)
│   ├── Certificate (11)
│   ├── Certificate Verify (15)
│   ├── Finished (20)
│   └── ...
├── Change Cipher Spec Protocol (20)
│   └── Change Cipher Spec (1)
├── Alert Protocol (21)
└── Application Data Protocol (23)
```

So in the output, the `(1)` here refers to the message type under the Handshake Protocol:

```bash
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
```

While the `(1)` below refers to the message type under the Change Cipher Spec Protocol:

```bash
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
```

This is like using the same number in different namespaces because they belong to different contexts, just like files in different folders can have the same name.

> [!note]
>
> In TLS 1.3, the Change Cipher Spec message has effectively become a legacy message. It no longer has real cryptographic significance in the new version, but it is still retained for compatibility. That is why you can still see this message during the TLS 1.3 handshake even though it is no longer technically required.

### Full handshake flow

```
Client                                         Server
   |                                                |
   |-------(OUT) Client Hello (1)------------------>|
   |                                               	|
   |<------(IN) Server Hello (2)--------------------|
   |<------(IN) Encrypted Extensions (8)------------|
   |<------(IN) Certificate (11)--------------------|
   |<------(IN) Certificate Verify (15)-------------|
   |<------(IN) Finished (20)-----------------------|
   |                                               	|
   |-------(OUT) Change Cipher Spec (1)------------>|
   |-------(OUT) Finished (20)--------------------->|

```

Details of each step:
- `Client Hello (1)`: The client starts the handshake and sends the supported TLS versions, cipher suites, random values, and more.
- `Server Hello (2)`: The server responds and selects the TLS version and cipher suite.
- `Encrypted Extensions (8)`: The server sends encrypted extension information.
- `Certificate (11)`: The server sends its digital certificate.
- `Certificate Verify (15)`: The server proves that it owns the private key corresponding to the certificate.
- `Finished (20)`: Both sides send a Finished message to confirm that the handshake is complete.
- `Change Cipher Spec (1)`: Tells the other side that subsequent communication will use the negotiated encryption parameters.

This process ensures that:
1. Both sides negotiate which encryption algorithms to use.
2. The server identity is verified.
3. Secure session keys are established.
4. Subsequent communication is protected.

> [!note]
>
> In TLS 1.3, compared with earlier versions, the handshake process has been optimized to reduce round trips and improve both performance and security. Most messages in the process are sent from the server to the client (`IN`), while the client mainly sends the initial and final messages (`OUT`).

### SSL connection information
```bash
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* ALPN, server accepted to use h2
```
- TLS 1.3 is used.
- The `TLS_AES_256_GCM_SHA384` cipher suite is used.
- The server agrees to use the HTTP/2 (`h2`) protocol.

## Server certificate
```bash
* Server certificate:
*  subject: CN=www.google.com
*  start date: Oct 21 08:38:45 2024 GMT
*  expire date: Jan 13 08:38:44 2025 GMT
*  subjectAltName: host "www.google.com" matched cert's "www.google.com"
*  issuer: C=US; O=Google Trust Services; CN=WR2
*  SSL certificate verify ok.
```

### Subject (certificate subject)

The Subject represents the identity information of the certificate owner. It uses DN (Distinguished Name) format and may include the following fields:
- `CN` (Common Name): usually the website domain name or server name
- `O` (Organization): organization name
- `OU` (Organizational Unit): organizational unit
- `L` (Locality): city or region
- `ST` (State): state or province
- `C` (Country): country code (two letters)
- `E` (Email): email address

So here, `CN=www.google.com` means that this certificate was issued for the domain name `www.google.com`.

### Subject Alternative Name
```bash
subjectAltName: host "www.google.com" matched cert's "www.google.com"
```
- `host "www.google.com"`: the hostname we are accessing
- `matched cert's "www.google.com"`: this hostname matches one of the values in the certificate's SAN list

Modern browsers mainly use SAN rather than CN to verify domain names. SAN can include:

- DNS names
- IP addresses
- Email addresses
- URIs

For example, the SAN of a certificate might include:
```
DNS:www.google.com
DNS:*.google.com
DNS:google.com
```

### Issuer
```bash
issuer: C=US; O=Google Trust Services; CN=WR2
```

The meaning of each field here is:
- `C=US`: Country = United States
- `O=Google Trust Services`: Organization = Google Trust Services
- `CN=WR2`: Common Name = WR2 (this is the internal name of the certificate issuance system)

So this indicates:
- The certificate was issued in the United States
- The organization is Google Trust Services
- The specific issuing system is WR2

This hierarchical structure helps establish the chain of trust:

```
Root CA (Root Certificate Authority)
    ↓
Intermediate CA (Intermediate Certificate Authority: Google Trust Services)
    ↓
End-entity Certificate (End certificate: www.google.com)
```

A more complete example of a certificate subject might look like this:

```
Subject: 
    CN = www.example.com
    O = Example Corporation
    OU = IT Department
    L = San Francisco
    ST = California
    C = US
    E = admin@example.com
```

This hierarchical naming structure ensures the completeness and uniqueness of certificate information, allowing a certificate to accurately identify both its owner and its issuer.

### Establishing the HTTP/2 protocol
```bash
* Using HTTP2, server supports multi-use
* Connection state changed (HTTP/2 confirmed)
* Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
* Using Stream ID: 1 (easy handle 0x564c4348b0e0)
```
- Confirms that HTTP/2 is being used
- Establishes an HTTP/2 stream
- Assigns stream ID `1`

### HTTP request headers
```bash
> GET / HTTP/2
> Host: www.google.com
> user-agent: curl/7.68.0
> accept: */*
```
- Sends a GET request
- Includes the basic HTTP header information

### Session tickets and response
```bash
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
* Connection state changed (MAX_CONCURRENT_STREAMS == 100)!
< HTTP/2 200
HTTP/2 200
```
- Receives new session tickets (used for TLS session resumption)
- Sets the maximum concurrent streams to `100`
- The server returns status code `200`, indicating the request succeeded

This output shows a complete HTTPS request process, including:
1. TCP connection establishment
2. TLS handshake
3. Certificate verification
4. HTTP/2 protocol negotiation
5. Request transmission and response reception

With the `-v` option, we can see all of these low-level details, which is especially useful when debugging HTTPS connection issues.
