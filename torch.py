import torch
print("PyTorch version:", torch.__version__)
print("CUDA version used by PyTorch:", torch.version.cuda)
print("cuDNN version used by PyTorch:", torch.backends.cudnn.version())
print("PyTorch GPU availability:", torch.cuda.is_available())
