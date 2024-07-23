# pylontech_exporter

Collect pylontech data via the console interface and Expose them in a prometheus format

## TODOs
* Make it device independant (not mentionning USB0/1/...). Search for the right device if not DEVICE_PATH given
* Make it more error resiliante. if possible, never crash the container from app level error
* Add tests
* Make command line arguments take precedence
* More logs
* V2 with object class