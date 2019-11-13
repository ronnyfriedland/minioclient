# minioclient
Minio / S3 graphical client written in python

## Configuration

The configuration is stored in `config.ini` which is generated after initial startup.

## Configuration example

```
[minio]
url = <host>:<port>
accesskey = .....
secretkey = .....
ssl = <True|False>
debug = <True|False>

[logging]
loglevel = <DEBUG|INFO|WARN|ERROR>
```

# Todos:

- Navigate back to parent directory
- Threading
  - upload / download
  - show current running processes
  - show status
