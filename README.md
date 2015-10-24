# WOMaaS

Write-Only Memory as a Service

## Introduction

In 1972, Signetics introduced the 25120 Fully Encoded, 9046xN, Random Access
Write-Only-Memory IC. This IC had many applications, including don't care
buffer stores, non-intelligent microcontrollers and first-in-never-out (FINO)
asynchronous buffers.

With WOMaaS, these capabilities can now be made available as a cloud service,
removing the need to have equipment for WOM stores on site and allowing
multiple users to share the same stores, thus reducing both hardware investment
and management and maintenance costs.

## Requirements

 * Python 2.7+
 * Python-Flask
 * Python-zlib

## Getting Started

    git clone https://github.com/irl/womaas.git
    cd womaas
    make db
    python main.py

By default, the application will listen on [localhost port 5000][1].

[1]: http://localhost:5000/

## Regular Maintenance

You may wish to regularly reset your WOM storage to allow for more data to be
written. No tools are provided for removing individual objects from the
storage, but it is possible to destroy an entire store and create a new one:

    make clean
    make db

