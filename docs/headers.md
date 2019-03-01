# Headers

Tech information about headers

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

##### 

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
