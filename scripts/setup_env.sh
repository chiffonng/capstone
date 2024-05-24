conda create -n venv python=3.11
conda activate venv

# Install dependencies
conda install torch==2.3.0 -c pytorch
# Enable CUDA support
# conda install cudatoolkit=12.6 -c pytorch

# Install other dependencies
pip install -r requirements.txt