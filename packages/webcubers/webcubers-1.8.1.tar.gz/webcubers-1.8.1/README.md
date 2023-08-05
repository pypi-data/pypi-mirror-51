# WebCubers Package & CLI Tool

this is interface package for WebCubers portal.

# Usage
```bash
 __    __     _       ___      _
/ / /\ \ \___| |__   / __\   _| |__   ___ _ __ ___
\ \/  \/ / _ \ '_ \ / / | | | | '_ \ / _ \ '__/ __|
 \  /\  /  __/ |_) / /__| |_| | |_) |  __/ |  \__ \
  \/  \/ \___|_.__/\____/\__,_|_.__/ \___|_|  |___/
             < WebCubers-CLI v1.8.1 >

usage: cubers [-h] {login,snippets,logout,profile} ...

WebCubers CLI Connector.

positional arguments:
  {login,snippets,logout,profile}

optional arguments:
  -h, --help            show this help message and exit
```

## Login
```bash
Cubers login MyUsername MyApiKey
```
## Profile
```bash
Cubers profile
```
## Leaders
```bash
Cubers snippets
```
## OTP
```bash
Cubers otp
```
## Connection
```bash
Cubers connection
```
## Snippets
```bash
Cubers snippets
```
## Repository
```bash
Cubers repo
Cubers repo --download serverfile.py
Cubers repo --upload localfile.py --force
```
## Logout
```bash
Cubers logout
```