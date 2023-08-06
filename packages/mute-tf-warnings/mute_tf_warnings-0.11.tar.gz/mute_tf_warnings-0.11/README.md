# Mute Tensorflow Warnings
Have been frustrated with tensorflow upgrade/other warnings? then this package is for you.

It mutes tensorflow warnings and makes your code outputs clean.

## Install
```bash
$ pip install mute_tf_warnings
```
## Usage
```python
import tensorflow as tf
from mute_tf_warnings import tf_mute_warning

# run this before any other tensorflow code
tf_mute_warning()

```

## license
[MIT](https://opensource.org/licenses/MIT)
