
from PIL import Image
import torch
import torchvision.transforms as transforms
import model




device = torch.device(
    "cuda:0" if torch.cuda.is_available() else "cpu")
transform = transforms.Compose([transforms.ToTensor()])
inputs=transform(Image.open("1_center_000001.jpg"))
inputs=inputs.unsqueeze(0).to(device)


parameter= torch.load('./checkpoint_07.pth.tar')
net = model.BasicResNet()
net.load_state_dict(parameter['state_dict']).to(device)
net.eval()



with torch.set_grad_enabled(False):
    outputs = net(inputs)
    _, predicted = torch.max(outputs, 1)
print(predicted)
