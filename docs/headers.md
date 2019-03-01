# Headers

Tech information about headers

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
