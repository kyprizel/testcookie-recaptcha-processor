Description
===========

**testcookie-recaptcha-processor** is a simple web server proxying recaptcha responses to Google.
Server should be used with [testcookie-nginx-module](http://github.com/kyprizel/testcookie-nginx-module) for setting cookies after solving recaptchas.

Note
====

This project is Proof-of-Contept for those people, who ask me to add "Captcha functionality" to testcookie-nginx-module.

Installation
============

Grab and install libraries:
    *) pip install -r requirements.txt
    *) start.sh

Build nginx with testcookie-nginx-module, use example configuration.
Run testcookie-recaptcha-processor, run nginx.


Example configuration
=====================

    server {
        listen 80;
        server_name domain.com;

        testcookie off;
        testcookie_name BPC;
        testcookie_secret keepmescret;
        testcookie_session $remote_addr;
        testcookie_arg attempt;
        testcookie_max_attempts 3;
        testcookie_fallback /cookies.html?backurl=http://$host$request_uri;
        testcookie_get_only on;
        testcookie_redirect_via_refresh on;
        testcookie_refresh_template "<html><body><script type=\"text/javascript\">var olC=function(){grecaptcha.render('captcha',{'sitekey':'recaptcha_public_key','callback':setcookie});};var setcookie=function(resp){document.getElementById('cpt').submit();};</script><script src=\"https://www.google.com/recaptcha/api.js?onload=olC&render=explicit\" async defer></script><form method=post action=\"/captcha\" id=\"cpt\"><div id=\"captcha\"></div></form></body></html>";

        location = /captcha {
            testcookie var;
            proxy_set_header Testcookie-Value $testcookie_set;
            proxy_set_header Testcookie-Nexturl $testcookie_nexturl;
            proxy_set_header Testcookie-Name "BPC";
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://127.0.0.1:10101/;
        }

        location / {
            testcookie on;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://127.0.0.1:8080;
        }

        location = /cookies.html {
            root /var/www/public_html;
        }

    }


Sources
=======

Available on github at [kyprizel/testcookie-recaptcha-processor]
(<http://github.com/kyprizel/testcookie-recaptcha-processor>).

Bugs
====

Feel free to report bugs and send patches to kyprizel@gmail.com
or use github's issue tracker(<http://github.com/kyprizel/testcookie-recaptcha-processor/issues>).

Copyright & License
===================

    Copyright (C) 2012 Eldar Zaitov (kyprizel@gmail.com).

    All rights reserved.

    This module is licenced under the terms of BSD license.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    *   Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.

    *   Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.

    *   Neither the name of the authors nor the names of its contributors
        may be used to endorse or promote products derived from this
        software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
