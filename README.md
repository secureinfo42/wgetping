# wgetping
Do some checks on URL

## Synopsis

```
Usage: wgetping [-d|-v|-c|-r|-t|-T] <url>

  -v : return HTTP headers
  -j : return HTTP headers, JSON format
  -d : return HTTP headers with colors
  -c : return HTTP status code
  -r : return HTTP reason (Not Found (404), OK (200), ...)
  -t : return text
  -T : return title (<title>.+</title>)
```

## Output (-v)

```
$ wgetping -v 'http://trk.amplmkt.com/t/2492/21163797'

HTTP Code                          : 200
HTTP Reason                        : OK
Date                               : Fri, 24 Feb 2023 04:09:31 GMT
Content-Type                       : image/gif
Content-Length                     : 43
X-Frame-Options                    : SAMEORIGIN
X-XSS-Protection                   : 0
X-Content-Type-Options             : nosniff
X-Download-Options                 : noopen
X-Permitted-Cross-Domain-Policies  : none
Referrer-Policy                    : strict-origin-when-cross-origin
Content-Disposition                : inline
Content-Transfer-Encoding          : binary
Vary                               : Accept
ETag                               : W/"548f2d6f4d0d820c6c5ffbeffcbd7f0e"
Cache-Control                      : max-age=0, private, must-revalidate
X-Request-Id                       : 919fe8ff-bb0d-4a82-8736-45619377d30d
X-Runtime                          : 0.017917
X-Cloud-Trace-Context              : 8699855d8172a0b3363d7349adbab988/14609764207029591474
Via                                : 1.1 google
Title                              :
Mime-Type                          : GIF image data, version 89a, 1 x 1
```
