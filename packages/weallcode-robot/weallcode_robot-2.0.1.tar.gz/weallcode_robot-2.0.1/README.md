# We All Code Robot Client

[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> The Python client code for the We All Code robots.

## Table of Contents

- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [Development](#development)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python >= 3

## Install

On Ubuntu-like systems:

```bash
sudo apt-get install python3-pip -y
pip3 install weallcode_robot
```

## Usage

```python
from weallcode_robot import Robot

alpha = Robot('alpha')

# (left, right) wheels 100% forward
alpha.wheels(100, 100)
alpha.sleep(1)

# (left, right) wheels 100% backward
alpha.wheels(-100, -100)
alpha.sleep(1)

# spin around
alpha.wheels(100, -100)
alpha.sleep(1)
```

## API

| Method       | Params                 | Values          | Example                   |
|--------------|------------------------|-----------------|---------------------------|
| `buzzer_off` |                        |                 | `bot.buzzer_off()`        |
| `buzzer`     | `hertz`, `period`      | `1` to `1000`   | `bot.buzzer(1000, 1000)`  |
| `led`        | `red`, `green`, `blue` | `0` to `255`    | `bot.led(0, 12, 255)`     |
| `sleep`      | `seconds`              | number >= 0     | `bot.sleep(1.5)`          |
| `stop`       |                        |                 | `bot.stop()`              |
| `wheels`     | `left`, `right`        | `-100` to `100` | `bot.wheels(-90, 80)`     |

## Development

### Requirements

- Docker

### Install

```bash
make install
```

### Run

Open the desired file in the `demo` folder and specify a robot name.

```bash
make demo       # Default demo
make demo march # Imperial Death March
make demo slow  # 50% wheel speed
make demo spin  # Spin around for 10 seconds
```

### Publish

```bash
make publish
```

## Maintainers

[@danielmconrad](https://github.com/danielmconrad)

## Contributing

PRs accepted.

Small note: If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

MIT © 2019 We All Code
