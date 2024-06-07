# https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch/layers
# CUDA driver version: 535.104.05, Python 3.10, CUDA 12.2, cuDNN > 8, PyTorch 2.1. 
FROM nvcr.io/nvidia/pytorch:23.10-py3

WORKDIR /workspace

# Install dependencies
COPY ./requirements.txt /workspace/
RUN pip install --upgrade pip
RUN pip install requirements.txt

