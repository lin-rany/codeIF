# CodeIF

## Introduction
This repository contains the code for the CodeIF project.

New Bench for Code Instruction Fellow


<p align="left">
    <a href="https://lin-rany.github.io/codeif.github.io/">🏠 Home Page </a> •
    <a href="https://huggingface.co/datasets/linrany/CodeIF">📊 Benchmark Data </a> •
    <a href="https://lin-rany.github.io/codeif.github.io/leaderboard.html">🏆 Leaderboard </a> 
</p>

## Setting Up
1. **Python Version**
    - Ensure that Python 3.11 is installed on your machine.

2. **Install Dependencies**
    - Install all dependencies that are required for the project by running:
      ```bash
      pip install -r requirements.txt
      ```

3. **Configure the Script**
    - Provide the necessary configuration for the script in `script/if_pipeline.sh`:
      ```bash
      model=""
      api_base=""
      api_key=""
      ```

## Usage
After setting up the environment, the scripts can be run with the provided model, API base, and API key configurations.
Execution
```bash
bash scripts/if_pipeline.sh
```
- Note
  - Replace placeholder values with your actual API credentials
  - Ensure execution permissions for scripts: `chmod +x scripts/*.sh`

<!-- ## Table of contents
- [CodeIF](#Introduction)
  - [📌 Introduction](#introduction)
  - [🏆 Leaderboard](#leaderboard)
  - [📋 Task](#task)
  - [📚 Data](#data)
  - [💻 Usage](#usage)
  - [📖 Citation](#citation) -->


## Citation

Feel free to cite us.

```bibtex
@misc{yan2025codeifbenchmarkinginstructionfollowingcapabilities,
      title={CodeIF: Benchmarking the Instruction-Following Capabilities of Large Language Models for Code Generation}, 
      author={Kaiwen Yan and Hongcheng Guo and Xuanqing Shi and Jingyi Xu and Yaonan Gu and Zhoujun Li},
      year={2025},
      eprint={2502.19166},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2502.19166}, 
}
```

## Contact
Feel free to contact us if you have any question or cooperation!
Email: lin_rany@foxmail.com
