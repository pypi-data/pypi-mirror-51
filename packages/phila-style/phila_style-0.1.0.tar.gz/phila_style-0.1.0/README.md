# phila_style

[![Build Status](https://travis-ci.org/PhiladelphiaController/phila_style.svg?branch=master)](https://travis-ci.org/PhiladelphiaController/phila_style)
[![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/download/releases/3.6.0/)
![t](https://img.shields.io/badge/status-stable-green.svg)
[![](https://img.shields.io/github/license/PhiladelphiaController/phila_style.svg)](https://github.com/PhiladelphiaController/phila_style/blob/master/LICENSE)
[![PyPi version](https://img.shields.io/pypi/v/phila_style.svg)](https://pypi.python.org/pypi/phila_style/)

A data visualization style based on the [City of Philadelphia Digital Standards](https://standards.phila.gov/guidelines/design-development/brand-elements/color-palette/). Matplotlib and Altair themes are included by default.

The theme requires the [Open Sans](https://fonts.google.com/specimen/Open+Sans) font to be installed.

## Light Mode

![Light Mode](/images/light_mode.png)

## Grey Mode

![Grey Mode](/images/grey_mode.png)

## Color palettes

The default color palette is slightly tweaked from the palette defined by the Digital Standards. The list of colors can be retrieved using:

```python
from phila_style import *

# default color palette with light/dark variations
default = get_default_palette()
light = get_light_palette()
dark = get_dark_palette()
```

Sequential color ramps can be constructed for any of the colors in the default color palettes. The color from the palette will be the midpoint of the color ramp.

```python
# get color ramp
ramp = get_color_ramp("blue", N=9)
```

All colors defined by the [Digital Standards palette](https://standards.phila.gov/guidelines/design-development/brand-elements/color-palette/) can also be loaded:

```python
standard = get_digital_standards()
```

## Matplotlib theme

'Dark', 'grey', and 'light' modes are available. Below is an example of the 'grey' theme:

```python
from matplotlib import pyplot as plt
import numpy as np
from phila_style.matplotlib import get_theme

with plt.style.context(get_theme(mode="grey")):
    for i in range(7):
        plt.plot(np.random.random(size=10))

    plt.gcf().text(
        0.005,
        0.95,
        "An Example of the City of Philadelphia 'Grey' Matplotlib Theme",
        weight="bold",
        fontsize=14,
    )
```

![Matplotlib Grey Mode](/images/grey_matplotlib_theme.png)

## Altair theme

Heavily inspired by the [LA Times Altair theme](https://github.com/datadesk/altair-latimes), but using the
recommended color palette from the City of Philadelphia's Digital Standards.

Currently, only the light theme is available.

```python
from phila_style.altair as get_theme
import altair as alt

# register and enable the theme
alt.themes.register('phila', get_theme)
alt.themes.enable('phila')
```

```python
from vega_datasets import data
source = data.cars()

alt.Chart(source).mark_circle(size=60).encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).interactive()
```

![Altair example](/images/altair_example.png)
