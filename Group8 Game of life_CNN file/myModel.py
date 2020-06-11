'''
Function:
	CNN simulate Game of Life.
'''
import torch
import torch.nn as nn


'''Basic Block'''
class basicBlock(nn.Module):
	def __init__(self, in_channels, out_channels, with_shortcut=True, **kwargs):
		super(basicBlock, self).__init__()
		self.conv1 = nn.Conv2d(in_channels[0], out_channels[0], kernel_size=1, stride=1, padding=0, bias=False)
		self.bn1 = nn.BatchNorm2d(out_channels[0])
		self.conv2 = nn.Conv2d(in_channels[1], out_channels[1], kernel_size=3, stride=1, padding=1, bias=False)
		self.bn2 = nn.BatchNorm2d(out_channels[1])
		self.conv3 = nn.Conv2d(in_channels[2], out_channels[2], kernel_size=1, stride=1, padding=0, bias=False)
		self.bn3 = nn.BatchNorm2d(out_channels[2])
		if not with_shortcut:
			self.conv4 = nn.Conv2d(in_channels[0], out_channels[2], kernel_size=1, stride=1, padding=0, bias=False)
			self.bn4 = nn.BatchNorm2d(out_channels[2])
		self.relu = nn.ReLU(inplace=True)
		self.with_shortcut = with_shortcut
	def forward(self, x):
		identity = x
		x = self.conv1(x)
		x = self.bn1(x)
		x = self.relu(x)
		x = self.conv2(x)
		x = self.bn2(x)
		x = self.relu(x)
		x = self.conv3(x)
		x = self.bn3(x)
		if not self.with_shortcut:
			identity = self.conv4(identity)
			identity = self.bn4(identity)
		x += identity
		x = self.relu(x)
		return x


'''build the model'''
class myModel(nn.Module):
	def __init__(self, **kwargs):
		super(myModel, self).__init__()
		self.layer1 = nn.Sequential(nn.Conv2d(1, 8, kernel_size=1, stride=1, padding=0, bias=False),
									nn.BatchNorm2d(8),
									nn.ReLU())
		self.layer2 = basicBlock([8, 8, 8], [8, 8, 24], with_shortcut=False)
		self.layer3 = basicBlock([24, 8, 8], [8, 8, 24], with_shortcut=True)
		self.layer4 = basicBlock([24, 8, 8], [8, 8, 24], with_shortcut=True)
		self.layer5 = nn.Sequential(nn.Conv2d(24, 1, kernel_size=1, stride=1, padding=0, bias=True),
									nn.Sigmoid())
		self.layers = nn.ModuleList([self.layer1, self.layer2, self.layer3, self.layer4, self.layer5])
	def forward(self, x):
		for layer in self.layers:
			x = layer(x)
		return x
