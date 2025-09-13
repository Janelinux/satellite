FROM continuumio/miniconda3:latest

WORKDIR /app

# 复制项目文件
COPY . /app

# 安装系统依赖（包括编译工具）
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# 创建conda环境
RUN conda create -n xda python=3.7 numpy scipy scikit-learn colorama -y

# 设置环境变量
ENV PATH /opt/conda/envs/xda/bin:$PATH

# 安装PyTorch
RUN /bin/bash -c "source activate xda && \
    conda install pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch -y"

# 先安装一些可能需要的依赖
RUN /bin/bash -c "source activate xda && \
    pip install cython setuptools wheel"

# 安装项目依赖（使用editable模式）
RUN /bin/bash -c "source activate xda && \
    cd ./satellite/XDA && \
    pip install --editable ."

RUN /bin/bash -c "source activate xda && \
    pip install -r  requirments.txt"