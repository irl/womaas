# WOMaaS

Write-Only Memory as a Service

## Introduction

In 1972, Signetics introduced the [25120 Fully Encoded, 9046xN, Random Access
Write-Only-Memory IC][1]. This IC had many applications, including don't care
buffer stores, non-intelligent microcontrollers and first-in-never-out (FINO)
asynchronous buffers.

[1]: https://github.com/irl/womaas/raw/master/doc/signetics-25120.pdf

With WOMaaS, these capabilities can now be made available as a cloud service,
removing the need to have equipment for WOM stores on site and allowing
multiple users to share the same stores, thus reducing both hardware investment
and management and maintenance costs.

![WOMaaS Home Page](https://github.com/irl/womaas/raw/master/doc/home.png)

## Requirements

 * Python 2.7+
 * Python-Flask
 * Python-zlib

## Getting Started

    git clone https://github.com/irl/womaas.git
    cd womaas
    make db
    python main.py

By default, the application will listen on [localhost port 5000][2].

[2]: http://localhost:5000/

## Uploading Objects

Objects can be uploaded via either the web interface or from the command line.
To upload from the web interface simply use the form on the home page of the
application. You will be redirected to the object metadata page after a
successful upload or shown a cryptic error message in the event of a failure.

To upload from the command line, you will need to use an HTTP client such as
`wget` or `curl`. For `curl`:

    curl -F "upload=@/path/to/file" http://localhost:5000/s

For `wget` you are on your own.

After a successful upload from the command line, you will be returned the
object's identifier in the store as the body of an HTTP response.

## Regular Maintenance

You may wish to regularly reset your WOM storage to allow for more data to be
written. No tools are provided for removing individual objects from the
storage, but it is possible to destroy an entire store and create a new one:

    make clean
    make db

