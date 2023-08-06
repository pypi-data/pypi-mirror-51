## matiz

Python's 3.7 dataclasses got maried with pyyaml.

## Installation:
```sh
pip install matiz
```

## Usage example:

```py
import dataclasses
import matiz
from matiz import fields

@dataclasses.dataclass
class Some(matiz.ObsoleteAble):
    id: int = fields.Integer()
    mac: str = fields.MacAddress()
    ip: str = fields.IPv4()
    version: int = fields.Integer(default=411)

```
Now the `Some` object can be created as a pure python object (thanks to `dataclass`)
it is equipped with `__init__`, `__repr__`, `__eq__` and some other methods. 

```py
>>> obj = Some(123, 'aa:bb:cc:11:22:33', '192.168.11.6')
>>> obj
Some(id=123, mac='aa:bb:cc:11:22:33', ip='192.168.11.6', version=411)

>>> print(obj)
!iz/Some
id: 123
ip: 192.168.11.6
mac: aa:bb:cc:11:22:33
version: 411
```

It's attributes are regular python attributes:
```py
>>> obj.id
123

>>> obj.mac
'aa:bb:cc:11:22:33'

>>> obj.ip
'192.168.11.6'

>>> obj.version = 0  # can be assigned
>>> print(repr(obj))
Ints(id=123, mac='aa:bb:cc:11:22:33', ip='192.168.11.6', version=0)
```

It can be also deserialized from yaml directly to the custom object:

```py
>>> yaml_string = """
!iz/Some
id: 22001
ip: 12.13.14.15
mac: aa:bb:cc:11:22:33
version: 0
"""

>>> import yaml
>>> obj2 = yaml.load(yaml_string, Loader=yaml.Loader)
>>> repr(obj2)
Some(id=22001, mac='aa:bb:cc:11:22:33', ip='12.13.14.15', version=0)

```

*To be further documented...*
 