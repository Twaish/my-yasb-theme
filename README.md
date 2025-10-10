# My YASB config

This repository contains my configuration-files for [YASB](https://github.com/amnweb/yasb)

## Preview

### default

![YASB Preview](./docs/preview.png)

## Building Themes

Build your YASB config (`config.yaml`) and styles (`styles.css`) individually or together using the `main.py` script.

```bash
# `styles.css` only
py main.py -c styles.css -t sharp

# `config.yaml` only
py main.py -i theme_build/build_config.yaml -o config.yaml -t sharp

# both
py main.py -i theme_build/build_config.yaml -o config.yaml -c styles.css -t sharp
```

## Ideas

### Dev Mode

Build the config.yaml or styles.css when modifying files inside the `./themes` folder.
