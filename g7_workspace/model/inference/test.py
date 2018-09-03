
from PIL import Image
import torch
import torchvision.transforms as transforms
import model








class Monitor:
    def __init__(self, parameter_path):
        self.device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([transforms.ToTensor()])
    
        self.parameter=torch.load(parameter_path)
        self.net= model.BasicResNet()
        self.net.load_state_dict(self.parameter['state_dict']).to(self.device)
    def inference(self,frame):
        self.net.eval()
        inputs=self.transform(frame)
        inputs=inputs.unsqueeze(0).to(self.device)
        with torch.set_grad_enabled(False):
            outputs = self.net(inputs)
            _, predicted = torch.max(outputs, 1)
        return predicted+976

   


Monitor('../checkpoint_07.pth.tar')
image=Image.open("1_center_000001.jpg")
print(Monitor.inference(image))

