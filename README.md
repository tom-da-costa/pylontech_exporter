# pylontech_exporter

Collect pylontech data via the console interface and Expose them in a prometheus format

## TODOs
* Make it device independant (not mentionning USB0/1/...). Search for the right device if not DEVICE_PATH given
* Make it more error resiliante. if possible, never crash the container from app level error
* Add tests
* Make command line arguments take precedence
* More logs
* parse_command_bat -> get_bats_dict_from_pwr IDEM for parse_command_pwr
* better reaction to exception
* add excection

## Test local

```bash
docker build . -t pe:test
docker run --rm -it -v $(pwd):/app -w /app pe:test bash
```