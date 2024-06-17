# pylontech_exporter

Collect pylontech data via the console interface and Expose them in a prometheus format

## TODOs
* Make it device independant (not mentionning USB0/1/...). Search for the right device if not DEVICE_PATH given
* EXTRA_DELAY -> SOFT_DELAY (dynamic delay)(include the update_metrics)
* Add tests