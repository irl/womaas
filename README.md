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

## Getting Started

    git clone https://github.com/irl/womaas.git
    make db
    python main.py

By default, the application will listen at http://localhost:5000/.

