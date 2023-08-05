# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['torchtrainer', 'torchtrainer.callbacks', 'torchtrainer.metrics']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.2,<2.0',
 'torchvision>=0.4.0,<0.5.0',
 'tqdm>=4.33,<5.0',
 'visdom>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'torchtrainer',
    'version': '0.3.4',
    'description': 'Focus on building and optimizing pytorch models not on training loops',
    'long_description': "# torchtrainer\n\n\nPyTorch model training made simpler. Focus on optimizing your model! Concepts are heavily inspired by the awesome project [torchsample](https://github.com/ncullen93/torchsample) and [Keras](https://github.com/keras-team/keras). \n\n[![Build Status](https://travis-ci.com/VictorKuenstler/torchtrainer.svg?branch=master)](https://travis-ci.com/VictorKuenstler/torchtrainer)\n[![codecov](https://codecov.io/gh/VictorKuenstler/torchtrainer/branch/master/graph/badge.svg)](https://codecov.io/gh/VictorKuenstler/torchtrainer)\n\n## Features\n\n* `Torchtrainer`\n* Logging utilities\n* Metrics\n* Visdom Visualization\n* Learning Rate Scheduler\n* Checkpointing\n* Flexible for muliple data inputs\n* Setup validation after every ... batches\n\n## Usage\n\n### Installation\n\n```bash\npip install torchtrainer\n```\n\n\n### Example\n\n```python\nfrom torch import nn\nfrom torch.optim import SGD\nfrom torchtrainer.callbacks.checkpoint import Checkpoint\nfrom torchtrainer.callbacks.csv_logger import CSVLogger\nfrom torchtrainer.callbacks.early_stopping import EarlyStoppingEpoch\nfrom torchtrainer.callbacks.progressbar import ProgressBar\nfrom torchtrainer.callbacks.reducelronplateau import ReduceLROnPlateauCallback\nfrom torchtrainer.callbacks.visdom import VisdomLinePlotter, VisdomEpoch\nfrom torchtrainer.metrics.binary_accuracy import BinaryAccuracy\nfrom torchtrainer.trainer import TorchTrainer\n\n\ndef transform_fn(batch):\n    inputs, y_true = batch\n    return inputs, y_true.float()\n\n\nmetrics = [BinaryAccuracy()]\n\ntrain_loader = ...\nval_loader = ...\n\nmodel = ...\nloss = nn.BCELoss()\noptimizer = SGD(model.parameters(), lr=0.001, momentum=0.9)\n\n# Setup Visdom Environment for your modl\nplotter = VisdomLinePlotter(env_name=f'Model {11}')\n\ncallbacks = [\n    ProgressBar(log_every=10),\n    VisdomEpoch(plotter, on_iteration_every=10),\n    VisdomEpoch(plotter, on_iteration_every=10, monitor='binary_acc'),\n    CSVLogger('test.log'),\n    Checkpoint('./model'),\n    EarlyStoppingEpoch(min_delta=0.1, monitor='val_running_loss', patience=10),\n    ReduceLROnPlateauCallback(factor=0.1, threshold=0.1, patience=2, verbose=True)\n]\n\ntrainer = TorchTrainer(model)\ntrainer.prepare(optimizer,\n                loss,\n                train_loader,\n                val_loader,\n                transform_fn=transform_fn,\n                callbacks=callbacks,\n                metrics=metrics)\n\n# train your model\ntrainer.train(epochs=10, batch_size=10)\n``` \n\n## TODO\n\n- more tests\n- metrics\n\n\n## \n\n",
    'author': 'Victor Künstler',
    'author_email': 'victor.kuenstler@outlook.com',
    'url': 'https://github.com/VictorKuenstler/torchtrainer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
