# AASJobAlert

AASJobAlert is a Python script for checking the AAS Job Register.

Some code borrowed from this [tutorial](https://www.codementor.io/gergelykovcs/how-and-why-i-built-a-simple-web-scrapig-script-to-notify-us-about-our-favourite-food-fcrhuhn45#the-process-of-building-the-web-scrapig-script).

## Installation

Use the package manager [pip](https://pypi.org/) to install aasalert.

```bash
pip install aasalert
```

## Usage

```bash
usage: aasalert [-h] keyword

    Search the AAS job register for post-doc positions in the last year.


positional arguments:
  keyword     Keyword to search the AAS job register for.

optional arguments:
  -h, --help  show this help message and exit
```

This is best used as a cronjob for regular checks of AAS. We can use `mailx` to generate a email alert. For example:

```bash
crontab -e

00 00 * * 1 aasalert keyword 2>&1 | mailx -E -s "AAS Job Alert" your.email@address.com
```

See [this link](https://opensource.com/article/17/11/how-use-cron-linux) for examples of how to use crontab.

## Contributing
Pull requests are welcome.


## License
[MIT](https://choosealicense.com/licenses/mit/)
