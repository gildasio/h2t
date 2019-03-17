# Headers

Tech information about headers

## Clear-Site-Data

### Options

* `cache`
* `cookies`
* `storage`
* `executionContexts`
* `*`

### Configuration

#### Apache

~~~
# Apache conf
<Directory ~ "logout">
    Header always set Clear-Site-Data "*"
</Directory>
~~~

#### Nginx

~~~
# Nginx conf
location /logout/ {
    add_header Clear-Site-Data "*" always;
}
~~~

## Content-Security-Policy

### Options

There is a lot of option, it's better see [here](https://content-security-policy.com/#directive).

### Configuration

#### Apache

~~~
# Apache conf
Header always set Content-Security-Policy "default-src 'self'"
~~~

#### Nginx

~~~
# Nginx conf
add_header Content-Security-Data "default-src 'self'" always;
~~~

## Cookies

### HttpOnly

#### Configuration

##### Apache

~~~
# Apache Conf
Header edit Set-Cookie ^(.*)$ $1;HttpOnly
~~~

##### Nginx

~~~
# Nginx conf
proxy_cookie-Path / "/; HttpOnly"
~~~

##### PHP

~~~
# php.ini
session.cookie_httponly = True
~~~

[Documentation](http://php.net/session.cookie-httponly)

### Same Site

#### Options

* Strict: only send cookies in same-site requests

* Lax: send cookies to cross-site requests when it's a GET request

#### Configuration

##### Apache

~~~
# Apache conf
Header edit Set-Cookie ^(.*)$ $1;; SameSite=strict
~~~

##### Nginx

~~~
# Nginx conf
proxy_cookie-Path / "/; ; SameSite=strict"
~~~

### Secure

#### Configuration

##### Apache

~~~
# Apache Conf
Header edit Set-Cookie ^(.*)$ $1;Secure
~~~

##### Nginx

~~~
# Nginx conf: SSL or default
proxy_cookie_path / "/; Secure";
~~~

##### PHP

~~~
# php.ini
session.cookie_secure = True
~~~

[Documentation](http://php.net/session.cookie-secure)

## Except-CT

### Options

* `max-age`
* `enforce`: optional
* `report-uri`: optional

### Configuration

#### Apache

~~~
Header always set Except-CT 'max-age=86400, enforce, report-uri="http://example.com/report"';
~~~

#### Nginx

~~~
# Nginx conf
add_header Except-CT 'max-age=86400, enforce, report-uri="http://example.com/report"' always;
~~~

## Feature-Policy

### Options

#### Set feature

* `autoplay`
* `camera`
* `document-domain`
* `encrypted-data`
* `fullscreen`
* `geolocation`
* `microphone`
* `midi`
* `payment`
* `vr`

#### Set origin

* `*`
* `self`
* `src`
* `none`

### Configuration

#### Apache

~~~
# Apache conf
Header always set Feature-Policy "camera: 'none'; geolocation: 'none'"
~~~

#### Nginx

~~~
# Nginx conf
add_header Feature-Policy "camera: 'none'; geolocation: 'none'";
~~~

## HTTP-Strict-Transport-Security

### Options

* `max-age`: time in seconds to browser store this configuration
* `includeSubDomains`: instructs browser to act in same way with subdomains
* `preload`

`preload` isn't an option in the specification but is widely used. More information [here](https://hstspreload.org).

### Configuration

#### Apache

~~~
# Apache conf
Header always set Strict-Transport-Security "max-age=31536000 ; includeSubDomains; preload"
~~~

#### Nginx

~~~
# Nginx conf
add_header Strict-Transport-Security "max-age=31536000 ; includeSubDomains; preload";
~~~

## Servers

### Configuration

#### Apache

* Core Way

~~~
# Apache Conf
ServerTokens Prod

# Options
#  Full => Apache/2.4.2 (Unix) PHP/4.2.2 MyMod/1.2
#  Prod => Apache
#  Major => Apache/2
#  Minor => Apache/2.4
#  Min => Apache/2.4.2
#  OS => Apache/2.4.2 (Unix) 
~~~

* ModSecurity Way

~~~
<ifmodule mod_security2.c="">
    ServerTokens Full
    SecServerSignature "Welcome to the rabbit hole"
</ifmodule>
~~~

#### Nginx

~~~
# Nginx
server_tokens off;
~~~

## Public-Key-Pins

### Options

* `pin-sha256`: SPKI fingerprint encoded in BASE64
* `max-age`: in seconds
* `includeSubDomains`: optional
* `report-uri`: optional

### Configuration

#### Apache

~~~
# Apache conf
Header always set Public-Key-Pins 'pin-sha256="base64=="; pin-sha256="base64=="; max-age=360000; includeSubDomains; report-uri="http://examplo.com/report"'
~~~

#### Nginx

~~~
# Nginx conf
add_header Public-Key-Pins 'pin-sha256="base64=="; pin-sha256="base64=="; max-age=360000; includeSubDomains; report-uri="http://example.com/report"' always;
~~~

## Referrer-Policy

### Options

* `""`: Tells to browser use a referrer policy provided in another place (eg meta-tag), or use the default (no-referrer-when-downgrade)
* `no-referrer`: Never sends Referer
* `no-referrer-when-downgrade`: Send entire URL unless change the traffic from HTTPS to HTTP
* `origin`: Send only origin from URL in Referer
* `origin-when-cross-origin`: Send only origin from URL in Referer when the destination origin is different from source origin
* `same-origin`: Send entire URL to same origin but nothing to other origins
* `strict-origin`: Send only origin to any origin but nothin when change HTTPS to HTTP
* `strict-origin-when-cross-origin`: Send the entire URL when destination is same origin, only origin when it's another one and nothing when change HTTPS to HTTP
* `unsafe-url`: Send entire URL in Referer

### Configuration

#### Apache

~~~
# Apache Conf
Header always set Referrer-Policy strict-origin-when-cross-origin
~~~

#### Nginx

~~~
# Nginx Conf
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
~~~

## X-Content-Type-Options

### Options

* nosniff: prevents browsers from mime-sniff the content and uses the informed by server

### Configuration

#### Apache

~~~
# Apache conf
Header always set X-Content-Type-Options "nosniff"
~~~

#### Nginx

~~~
# Nginx conf
add_header X-Content-Type-Options "nosniff" always;
~~~

#### IIS

1. IIS Manager
2. Select the website
3. Double click in HTTP Response Headers
4. Click in Add
5. Add "X-Content-Type-Options" in Name and "nosniff" in Value
6. Click to save

## X-Download-Options

### Options

* noopen: prevents IE directly open a dowloaded file forcing user to save it them open in any application

### Configuration

#### Apache

~~~
# Apache conf
Header always set X-Download-Options "noopen"
~~~

#### Nginx

~~~
# Nginx conf
add_header X-Download-Options "noopen" always;
~~~

### IIS

1. IIS Manager
2. Select the website
3. Double click in HTTP Response Headers
4. Click in ADd
5. Add "X-Download-Options" in Name and "noopen" in Value
6. Click to save

## X-Frame-Options

### Options

* DENY: Deny any frame
* SAMEORIGIN: Allow frame from the same website
* ALLOW-FROM: Allow from a specific website

### Configuration

#### Apache

~~~
# Apache Conf
Header always append X-Frame-Options SAMEORIGIN

# htaccess
Header append X-FRAME-OPTIONS "SAMEORIGIN"
~~~

#### Nginx

~~~
# nginx.conf
add_header X-Frame-Options "SAMEORIGIN";
~~~

#### IIS

1. IIS Manager
2. Select the website
3. Double click in HTTP Response Headers
4. Click in Add
5. Add "X-Frame-Option" in Name and the option (eg SAMEORIGIN) in Value
6. Click to save

[Documentation](https://support.office.com/en-us/article/mitigating-framesniffing-with-the-x-frame-options-header-1911411b-b51e-49fd-9441-e8301dcdcd79)

#### ASP.Net

Use [NWebsec](https://docs.nwebsec.com/en/latest/nwebsec/Configuring-xfo.html).

## X-Permitted-Cross-Domain-Policies

### Options

* none  No policy files are allowed anywhere on the target server, including this master policy file.
master-only Only this master policy file is allowed.
by-content-type [HTTP/HTTPS only] Only policy files served with Content-Type: text/x-cross-domain-policy are allowed.
by-ftp-filename [FTP only] Only policy files whose file names are crossdomain.xml (i.e. URLs ending in /crossdomain.xml) are allowed.
all All policy files on this target domain are allowed.

### Configuration

#### Apache

~~~
# Apache Conf
Header always append X-Permitted-Cross-Domain-Policies none
~~~

#### Nginx

~~~
# Nginx conf
add_header X-Permitted-Cross-Domain-Policies "none" always;
~~~

#### IIS

1. IIS Manager
2. Select the website
3. Double click in HTTP Response Headers
4. Click in ADd
5. Add "X-Permitted-Cross-Domain-Policies" in Name and the option (eg none) in Value
6. Click to save
## X-XSS-Protection

### Options

* `0`: disable the protection
* `1`: enable the protection to sanitize the script
* `1; mode=block`: enable the protection to block the response when detect an attack
* `1; report=URI`: enable the protection to sanitize the script and report the attack to URI
* `1; mode=block; report=URI`: enable the protection to block the request and report to URI

### Configuration

#### Apache

~~~
# Apache conf
Header always append X-Xss-Protection "1; mode=block"

# htaccess
<IfModule mod_headers.c> 
  Header set X-Xss-Protection "1; mode=block" 
</IfModule>
~~~
#### Nginx

~~~
# Nginx conf
add_header X-Xss-Protection "1; mode=block" always;
~~~
#### IIS

1. IIS Manager
2. Select the website
3. Double click in HTTP Response Headers
4. Click in Add
5. Add "X-Xss-Protection" in Name and the option (eg `1; mode=block`) in Value
6. Click to sabe
