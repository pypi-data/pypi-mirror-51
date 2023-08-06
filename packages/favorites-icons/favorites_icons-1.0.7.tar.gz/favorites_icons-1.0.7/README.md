# Favorites Icons
```bash
pip install git+https://github.com/avryhof/favorites_icons.git
```

A simple plugin to generate all of your touch and favorites icons, as well as the needed tags to make them work.A

## settings.py
```python
ICON_SRC = '/path/to/a/big/file.png'
SITE_NAME='My Site'  # Optional if you are using the Sites framework, and have a SITE_ID configured.
TILE_COLOR='#FFFFFF'
THEME_COLOR='#FFFFFF'
# Optional
# A list of numbers for icon sizes... they will all be generated and tagged.
ICON_SIZES = [16, 32, 57, 60, 64, 72, 76, 96, 114, 120, 144, 152, 180, 192, 256, 512]
```