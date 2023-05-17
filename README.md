# DEQ Optical Flow experiment

The original readme can still be read [here](original_readme.md).

## Requirements
In order to run this code you need a Python installation with version at least 3.9.
You can then install the requirements using the following command:

```
pip install .
```

## Reproducing Fig. 2 of the paper
In order to reproduce the optical flow part of Fig 2. of the paper you will need to download the [data](http://sintel.is.tue.mpg.de/) and the [model weights](https://drive.google.com/drive/folders/1a_eX_wYN1qTw2Rj1naEXhcsG4D3KKxFw?usp=sharing).
These weights come from the original paper that introduced DEQ-Flow.

You can then run the following command to reproduce the results with `f_thres` the test-time number of iterations:

```
python deq_flow/main.py --eval --name deq-flow-H-all-grad --stage things \
    --validation sintel --restore_ckpt checkpoints/deq-flow-H-things-test-3x.pth --gpus 0 \
    --wnorm --eval_f_thres $f_thres --f_eps 0.00001 --f_solver naive_solver  \
    --huge --results_name optical_flow_results.csv
```

The rest of the instructions are in the `deq` folder.
