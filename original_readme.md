# Deep Equilibrium Optical Flow Estimation

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/deep-equilibrium-optical-flow-estimation/optical-flow-estimation-on-kitti-2015-train)](https://paperswithcode.com/sota/optical-flow-estimation-on-kitti-2015-train?p=deep-equilibrium-optical-flow-estimation)

(🌟Version 2.0 released!🌟)

This is the official repo for the paper [*Deep Equilibrium Optical Flow Estimation*](https://arxiv.org/abs/2204.08442) (CVPR 2022), by [Shaojie Bai](https://jerrybai1995.github.io/)\*, [Zhengyang Geng](https://gsunshine.github.io/)\*, [Yash Savani](https://yashsavani.com/) and [J. Zico Kolter](http://zicokolter.com/).

<div align=center><img src="assets/frame_0037_frame.png" width="400" height="218" /><img src="assets/frame0037_pred.png" width="400" height="218" /></div>

> A deep equilibrium (DEQ) flow estimator directly models the flow as a path-independent, “infinite-level” fixed-point solving process. We propose to use this implicit framework to replace the existing recurrent approach to optical flow estimation. The DEQ flows converge faster, require less memory, are often more accurate, and are compatible with prior model designs (e.g., RAFT and GMA).

## Demo

We provide a demo video of the DEQ flow results below.

https://user-images.githubusercontent.com/18630903/163676562-e14a433f-4c71-4994-8e3d-97b3c33d98ab.mp4

---

## Update

🌟 2022.xx.xx - Support visualization and demo on your own datasets and videos! Coming soon!

🌟 2022.08.08 - Release the **version 2.0** of DEQ-Flow! DEQ-Flow will be merged into [DEQ](https://github.com/locuslab/deq) after further upgrading and unit testing. 

- A clean and decoupled **[DEQ lib](https://github.com/locuslab/deq-flow/blob/main/code.v.2.0/core/deq)**. This is a fully featured and out-of-the-box lib. You're welcome to implement **your own DEQ** using our DEQ lib! We support the following features. (*The DEQ lib will be available on PyPI soon for easy installation via `pip`.*)
  - Automatic arg parser decorator. You can call this function to add the DEQ args to your program. See the explanation for args [here](https://github.com/locuslab/deq-flow/blob/main/code.v.2.0/core/deq/arg_utils.py)!
  
    ```Python
    add_deq_args(parser)
    ```

  - Automatic DEQ definition. Call `get_deq` to get your DEQ class! **It's highly decoupled implementation agnostic to your model design!**

    ```Python
    DEQ = get_deq(args)
    self.deq = DEQ(args)
    ```

  - Automatic normalization for DEQ. You now do not need to add normalization manually to each weight in the DEQ func!

    ```Python
    if args.wnorm:
        apply_weight_norm(self.update_block)
    ```

  - Easy DEQ forward. Even for a multi-equilibria system, you can call the DEQ function using several lines!

    ```Python
    # Assume args is a list [z1, z2, ..., zn] 
    # of to-be-solved equilibrium variables.
    def func(*args):
        # A functor defined in the Pytorch forward function.
        # Having the same input and output tensor shapes.
        return args

    deq_func = DEQWrapper(func, args)
    z_init = deq_func.list2vec(*args) # will be merged into self.deq(...)
    z_out, info = self.deq(deq_func, z_init)
    ```

  - Automatic DEQ training. Gradients (both exact and inexact grad) are tracked automatically! Fixed point correction can be customized through your arg parser. Just post-process `z_out` as you want!

- Benchmarked results and [checkpoints](https://drive.google.com/drive/folders/1a_eX_wYN1qTw2Rj1naEXhcsG4D3KKxFw?usp=sharing). Using the release code base v.2.0, we've trained DEQ-Flow-H on FlyingChairs and FlyingThings for two schedules, *120k+120k (1x)* and *120k+360k (3x)*. This implementation demonstrated a new SOTA, surpassing our previous results in performance, training speed, and memory usage.
  
  Notably, we also benchmark RAFT using the same model size. DEQ-Flow demonstrates a clear performance and efficiency margin and **much stronger scaling property** (scale up to larger models) over RAFT!

    |  Checkpoint Name | Sintel (clean) | Sintel (final) | KITTI AEPE  | KITTI F1-all |
    | :--------------: | :------------: | :------------: | :---------: | :----------: |
    | RAFT-H-1x     | 1.36 | 2.59 | 4.47 | 16.16 |
    | DEQ-Flow-H-1x | 1.27 | 2.58 | 3.76 | 12.95 |
    | DEQ-Flow-H-3x | 1.27 | 2.48 | 3.77 | 13.41 |
  
  - 1x=120k iterations on FlyingThings, 3x=360k iterations on FlyingThings, using a batch size of 6.
  - Increasing the batch size on FlyingThings can further improve these results, e.g., a batch size of 12 can reduce the F1-all of DEQ-Flow-H-1x to around 12.5 on KITTI.

  To validate our results, download the pretrained [checkpoints](https://drive.google.com/drive/folders/1a_eX_wYN1qTw2Rj1naEXhcsG4D3KKxFw?usp=sharing) into the `checkpoints` directory. Run the following command in [code.v.2.0](https://github.com/locuslab/deq-flow/blob/main/code.v.2.0/) to infer over the Sintel train set and the KITTI train set. This is a reference [log](https://github.com/locuslab/deq-flow/blob/main/code.v.2.0/log/val.txt).

    ```bash
    bash val.sh
    ```

---

## Requirements

The code in this repo has been tested on PyTorch v1.10.0. Install required environments through the following commands.

```bash
conda create --name deq python==3.6.10
conda activate deq
conda install pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=11.3 -c pytorch -c conda-forge
conda install tensorboard scipy opencv matplotlib einops termcolor -c conda-forge
```

Download the following datasets into the `datasets` directory.

- [FlyingChairs](https://lmb.informatik.uni-freiburg.de/resources/datasets/FlyingChairs.en.html#flyingchairs)
- [FlyingThings3D](https://lmb.informatik.uni-freiburg.de/resources/datasets/SceneFlowDatasets.en.html)
- [MPI Sintel](http://sintel.is.tue.mpg.de/)
- [KITTI 2015](http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=flow)
- [HD1k](http://hci-benchmark.iwr.uni-heidelberg.de/)

---
The following README doc is for version 1.0, i.e., [code.v.1.0](https://github.com/locuslab/deq-flow/blob/main/code.v.1.0/). You can follow this to reproduce all the results.

## Inference

Download the pretrained [checkpoints](https://drive.google.com/drive/folders/1PeyOr4kmSuMWrh4iwYKbVLqDU6WPX-HM?usp=sharing) into the `checkpoints` directory. Run the following command to infer over the Sintel train set and the KITTI train set.

```bash
bash val.sh
```

You may expect the following performance statistics of given checkpoints. This is a reference [log](https://github.com/locuslab/deq-flow/blob/main/code.v.1.0/ref/val.txt).

|  Checkpoint Name | Sintel (clean) | Sintel (final) | KITTI AEPE  | KITTI F1-all |
| :--------------: | :------------: | :------------: | :---------: | :----------: |
| DEQ-Flow-B   | 1.43 | 2.79 | 5.43 | 16.67 |
| DEQ-Flow-H-1 | 1.45 | 2.58 | 3.97 | 13.41 |
| DEQ-Flow-H-2 | 1.37 | 2.62 | 3.97 | 13.62 |
| DEQ-Flow-H-3 | 1.36 | 2.62 | 4.02 | 13.92 |

## Visualization

Download the pretrained [checkpoints](https://drive.google.com/drive/folders/1PeyOr4kmSuMWrh4iwYKbVLqDU6WPX-HM?usp=sharing) into the `checkpoints` directory. Run the following command to visualize the optical flow estimation over the KITTI test set.

```bash
bash viz.sh
```

## Training

Download *FlyingChairs*-pretrained [checkpoints](https://drive.google.com/drive/folders/1PeyOr4kmSuMWrh4iwYKbVLqDU6WPX-HM?usp=sharing) into the `checkpoints` directory.

For the efficiency mode, you can run 1-step gradient to train DEQ-Flow-B via the following command. Memory overhead per GPU is about 5800 MB.

You may expect best results of about 1.46 (AEPE) on Sintel (clean), 2.85 (AEPE) on Sintel (final), 5.29 (AEPE) and 16.24 (F1-all) on KITTI. This is a reference [log](https://github.com/locuslab/deq-flow/blob/main/code.v.1.0/ref/B_1_step_grad.txt).

```bash
bash train_B_demo.sh
```

For training a demo of DEQ-Flow-H, you can run this command. Memory overhead per GPU is about 6300 MB. It can be further reduced to about **4200 MB** per GPU when combined with `--mixed-precision`. You can further reduce the memory cost if you employ the CUDA implementation of cost volumn by [RAFT](https://github.com/princeton-vl/RAFT).

You may expect best results of about 1.41 (AEPE) on Sintel (clean), 2.76 (AEPE) on Sintel (final), 4.44 (AEPE) and 14.81 (F1-all) on KITTI. This is a reference [log](https://github.com/locuslab/deq-flow/blob/main/code.v.1.0/ref/H_1_step_grad.txt).

```bash
bash train_H_demo.sh
```

To train DEQ-Flow-B on Chairs and Things, use the following command.

```bash
bash train_B.sh
```

For the performance mode, you can run this command to train DEQ-Flow-H using the ``C+T`` and ``C+T+S+K+H`` schedule. You may expect the performance of <1.40 (AEPE) on Sintel (clean), around 2.60 (AEPE) on Sintel (final), around 4.00 (AEPE) and 13.6 (F1-all) on KITTI. DEQ-Flow-H-1,2,3 are checkpoints from three runs.

Currently, this training protocol could entail resources slightly more than two 11 GB GPUs. In the near future, we will upload an implementation revision (of the DEQ models) that shall further reduce this overhead to **less than two 11 GB GPUs**.

```bash
bash train_H_full.sh
```

## Code Usage

Under construction. We will provide more detailed instructions on the code usage (e.g., argparse flags, fixed-point solvers, backward IFT modes) in the coming days.

---

## A Tutorial on DEQ

If you hope to learn more about DEQ models, here is an official NeurIPS [tutorial](https://implicit-layers-tutorial.org/) on implicit deep learning. Enjoy yourself!

## Reference

If you find our work helpful to your research, please consider citing this paper. :)

```bib
@inproceedings{deq-flow,
    author = {Bai, Shaojie and Geng, Zhengyang and Savani, Yash and Kolter, J. Zico},
    title = {Deep Equilibrium Optical Flow Estimation},
    booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
    year = {2022}
}
```

## Credit

A lot of the utility code in this repo were adapted from the [RAFT](https://github.com/princeton-vl/RAFT) repo and the [DEQ](https://github.com/locuslab/deq) repo.

## Contact

Feel free to contact us if you have additional questions. Please drop an email through zhengyanggeng@gmail.com (or [Twitter](https://twitter.com/ZhengyangGeng)).