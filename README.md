# Inky Impression Demo

This is a little python script to display images on a Pimoroni Inky Impression. It will display all images in the correct aspect ratio and you can choose if you want them to fit or fill the screen. And there is support for rotation if you want to display your images with the display being oriented in portrait or upside down.

Images are displayed one by one. 

Tested with the *7.3" Inky Impression (2025 Edition)* in combination with a *Raspberry Pi 5*.

## Requirements

- Python 3.10 or newer
- PIL / [Pillow](https://pillow.readthedocs.io/en/stable/?badge=latest)
- [inky library](https://github.com/pimoroni/inky)

## Parameter

| Argument   | Short | Description                                                  | Default |
| ---------- | ----- | ------------------------------------------------------------ | ------- |
| --file     | -f    | One or more paths to images that should be displayed.        |         |
| --dir      | -d    | A path to a directory that contains the images that should be displayed.<br />Will be ignored if `--file` was used. |         |
| --rotation | -r    | Define a rotation of the images if you placed your display in a different orientation.<br />Valid values are `0`, `90`, `180`, `270` and `-90`. | `0`     |
| --scale    | -s    | Define a scaling variant for the images.<br />Valid values are `fit` and `fill`.<br />`fit` will always display the whole image but can leave unused space on the display.<br />`fill` will scale the image up to fill the whole screen. | `fit`   |

## Examples

```shell
python main.py --file myimage.png anotherimage.jpg
```

```shell
python main.py -d ~/Pictures/Latest_Holiday -r -90 -s fill
```

## Buttons

| Button |                                            |
| ------ | ------------------------------------------ |
| A      | Next image                                 |
| B      | Random image                               |
| C      | Toggle scale mode between `fit` and `fill` |
| D      | Previous image                             |