# chrys

A collection of color palettes for mapping and visualisation.

## Demo

[netbek.github.io/chrys](https://netbek.github.io/chrys)

## Sass

### Installation

```shell
npm install chrys
```

### Usage

See the [demo](https://netbek.github.io/chrys) for a list of palette names and sizes.

```scss
@import 'node_modules/chrys/src/variables';

// Get the first color of the `colorblind` palette, size 3
$palette-name: 'colorblind';
$palette-size: 3;
$palette:      map-get(map-get($chrys-color-map, $palette-name), $palette-size);
$color:        nth($palette, 1);

div {
  background: $color;
}
```

### Development

Build distribution files:

```shell
gulp
```

## Python

### Installation

```shell
pip install chrys
```

### Usage

Generate a new palette as a subset of a given palette:

```python
>>> from chrys.palettes import VEGA_PALETTES, to_continuous_palette, to_discrete_palette
>>> to_discrete_palette(VEGA_PALETTES['viridis'], 6)
['#46327f', '#375c8d', '#27808e', '#1fa187', '#4ac26d', '#9fda3a']
>>> to_continuous_palette(VEGA_PALETTES['viridis'][256], 6)
['#440356', '#414587', '#2a788e', '#22a884', '#79d152', '#fbe724']
```

Generate a new palette as a subset of a palette from a given provider:

```python
>>> from chrys.palettes import continuous_palette, discrete_palette
>>> discrete_palette('vega_viridis', 6)
['#46327f', '#375c8d', '#27808e', '#1fa187', '#4ac26d', '#9fda3a']
>>> continuous_palette('vega_viridis', 6)
['#440356', '#414587', '#2a788e', '#22a884', '#79d152', '#fbe724']
```

Get the vendor library and palette names from a given name:

```python
>>> from chrys.palettes import parse_palette_name
>>> parse_palette_name('vega_viridis')
('vega', 'viridis')
```

### Development

Install Node and Python dependencies:

```shell
./scripts/install.sh
```

Build palette data:

```shell
npm run py-build-data
```

Build distribution package:

```shell
npm run py-build-dist
```

Publish distribution package:

```shell
npm run py-publish
```

## Credit

Palettes from:

* [Bokeh](https://bokeh.org) (BSD-3-Clause)
* [Vega](https://vega.github.io/vega) (BSD-3-Clause)

## License

Copyright (c) 2017 Hein Bekker. Licensed under the BSD 3-Clause License.
