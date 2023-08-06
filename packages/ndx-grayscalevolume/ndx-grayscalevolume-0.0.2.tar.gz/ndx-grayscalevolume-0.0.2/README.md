# ndx-grayscalevolume Extension for NWB:N

[![PyPI version]()

[Python Installation](#python-installation)

[Python Usage](#python-usage)

### Python Installation
```bash
pip install git+https://github.com/ben-dichter-consulting/ndx-grayscalevolume.git
```

### Python Usage

```python
from datetime import datetime
from pynwb import NWBFile, NWBHDF5IO, ProcessingModule
from ndx_grayscalevolume import GrayscaleVolume
import numpy as np

nwb = NWBFile('session_description', 'identifier', datetime.now().astimezone())

#Creates ophys ProcessingModule and add to file
ophys_module = ProcessingModule(name='ophys',
                                description='contains optical physiology processed data.')
nwb.add_processing_module(ophys_module)

#Creates GrayscaleVolume containers
grayscale_volume = GrayscaleVolume(name='test_grayscalevolume2',
                                    data=np.zeros((3, 4, 5)),
                                    spatial_scale=(5., .5, 3.))
ophys_module.add(grayscale_volume)

with NWBHDF5IO('test_grayscalevolume.nwb', 'w') as io:
    io.write(nwb)

with NWBHDF5IO('test_grayscalevolume.nwb', 'r', load_namespaces=True) as io:
    nwb = io.read()
    print(nwb)

```
