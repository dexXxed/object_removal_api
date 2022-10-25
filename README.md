# Object Removal API

## Deploy to the GPU Srerver

1. Install Python 3.8 and pip
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
sudo apt-get install python3-pip
```
2. Install drivers for GPU
```
sudo add-apt-repository ppa:graphics-drivers/ppa
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
sudo reboot
```
3. Clone this repo and download the model
```
git clone https://github.com/dexXxed/object_removal_api.git
cd object_removal_api/assets
curl -L https://huggingface.co/spaces/aryadytm/remove-photo-object/resolve/f00f2d12ada635f5f30f18ed74200ea89dd26631/assets/big-lama.pt -o big-lama.pt
cd ..
```
4. Install all packages
```
sudo pip3 install torch==1.8.0+cu111 torchvision==0.9.0+cu111 torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html
sudo pip3 install numpy Pillow opencv-python scipy python-multipart uvicorn fastapi gunicorn
```
5. Run the app
```
sudo gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --workers 2 --timeout 5000 --access-logfile ./gpu_logs.log --log-file ./gpu_logs.log --log-level info --capture-output -D main:app
```
