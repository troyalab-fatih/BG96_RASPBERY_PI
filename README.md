
# Installation ![Static Badge](https://img.shields.io/badge/https%3A%2F%2Fgithub.com%2Ftroyalab-fatih%2FBG96_RASPBERY_PI) 

The easiest way to install troyalab is to download it from [`PyPI`](https://pypi.org/project/troyalab/). It's going to install the library itself and its prerequisites as well.

```shell
$ pip install troyalab
```

Secondly, you can install troyalab from its source code.

```shell
$ git clone https://github.com/troyalab-fatih/BG96_RASPBERY_PI
$ cd troyalab
$ pip install -e .
```

----

 Import 
----

Then you will be able to import the library and use its functionalities.

```python
import troyalab.RPi_Shield
```

You can connect to the card by typing which port your Troyalab RPi Shield is connected to.

```python
troyalab = troyalab.RPi_Shield.BG96("/dev/ttyS0")
```

Then you need to adjust the GPIO settings to get your card up.
And you are ready.
```python
troyalab.setupGPIO()
troyalab.powerUp()
troyalab.getHardwareInfo()
```

---



---

### Verison Descriptions

| Version | 0.1.3        |
| ------- |--------------|
| Author  | Fatih Furkan |
| Date    | 13.08.2023   |
| Raspi   | 4 - Model B  |
| Python  | 3.9.2        |
#### Verison Descriptions
- Git and PyPI pulled to the same version. 