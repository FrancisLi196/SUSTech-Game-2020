'''
Function:
	CNN simulate Game of Life.
'''
import os
import time
import torch
import random
import numpy as np
import torch.nn as nn
from myModel import myModel
from torch.utils.data import DataLoader
import results


'''hyperparameter'''
batch_size = 64
num_workers = 4
max_epoch = 6
logfile = 'train.log'
save_interval = 2
backupdir = 'weights'


'''Game of Life'''
class lifeGame():
	def __init__(self):
		self.info = 'Game of Life'
	'''get the data of Game of Life for train'''
	def getGameData(self, max_iter=10, num_games=5000, size=20, init_life=100, is_save=True):
		X, y = np.zeros([max_iter*num_games, 1, size, size]).astype(np.float32), np.zeros([max_iter*num_games, 1, size, size]).astype(np.float32)
		for each_game in range(num_games):
			frame = self.initGame(size=size, init_life=init_life)
			for i in range(max_iter):
				X[i+each_game*max_iter, 0, :, :] = frame
				frame = self.nextFrame(frame)
				y[i+each_game*max_iter, 0, :, :] = frame
		if is_save:
			X_savename = 'Xtrain_%s.npy' % str(max_iter*num_games)
			y_savename = 'ytrain_%s.npy' % str(max_iter*num_games)
			np.save(X_savename, X)
			np.save(y_savename, y)
		return X, y
	'''get the first frame of Game of Life'''
	def initGame(self, size=60):
		frame = np.zeros([size, size]).astype(np.float32)
		for i in range(size):
			for j in range(size):
				frame[i,j]=0
		frame[9:11,2:4]=np.transpose([[1,1],[1,1]])
		frame[7:14,12:20]=[[0,0,1,1,0,0,0,0],[0,1,0,0,0,1,0,0],[1,0,0,0,0,0,1,0],[1,0,0,0,1,0,1,1],[1,0,0,0,0,0,1,0],
							[0,1,0,0,0,1,0,0],[0,0,1,1,0,0,0,0]]
		frame[5:12, 22:27] = [[0, 0, 0, 0, 1], [0, 0, 1, 0, 1], [1, 1, 0, 0, 0],
							   [1, 1, 0, 0, 0], [1, 1, 0, 0, 0],
							   [0, 0, 1, 0, 1],[0, 0, 0, 0, 1]]
		frame[7:9, 36:38] = np.transpose([[1, 1], [1, 1]])
		#print(frame[14:23,:])
		return frame
	'''get the next frame according to the current frame'''
	def nextFrame(self, frame):
		next_frame = frame.copy()
		for i in range(0, frame.shape[0]):
			for j in range(0, frame.shape[1]):
				n = frame[max(0, i-1): min(frame.shape[0]-1, i+2), max(0, j-1): min(frame.shape[1]-1, j+2)].sum() - frame[i, j]
				if n == 3:
					next_frame[i, j] = 1
				elif n == 2:
					next_frame[i, j] = frame[i, j]
				else:
					next_frame[i, j] = 0
		return next_frame


'''
Function:
	provide data for training
Input:
	path(Nore/list): [Xtrain_path, ytrain_path]
'''
class Dataset():
	def __init__(self, path=None, is_shuffle=True):
		if path is None:
			self.X, self.y = lifeGame().getGameData(max_iter=10, num_games=5000, size=20, init_life=100, is_save=True)
		else:
			self.X, self.y = np.load(path[0]), np.load(path[1])
		assert self.X.shape == self.y.shape
		if is_shuffle:
			idxs = np.arange(self.X.shape[0])
			random.shuffle(idxs)
			self.X, self.y = self.X[idxs], self.y[idxs]
	def __getitem__(self, index):
		X = self.X[index % self.X.shape[0]]
		y = self.y[index % self.y.shape[0]]
		X = torch.from_numpy(X).float()
		y = torch.from_numpy(y).float()
		return X, y
	def __len__(self):
		return self.X.shape[0]


'''print info'''
def Logging(message, savefile=None):
	content = '%s %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)
	if savefile:
		f = open(savefile, 'a')
		f.write(content + '\n')
		f.close()
	print(content)


'''train the model'''
def train():
	if not os.path.exists(backupdir):
		os.mkdir(backupdir)
	model = myModel()
	path = None
	if os.path.isfile('Xtrain_50000.npy') and os.path.isfile('ytrain_50000.npy'):
		path = ['Xtrain_50000.npy', 'ytrain_50000.npy']
	dataloader = torch.utils.data.DataLoader(Dataset(path=path),
											 batch_size=batch_size,
											 shuffle=False,
											 num_workers=num_workers)
	use_cuda = torch.cuda.is_available()
	if use_cuda:
		model = model.cuda()
	model.train()
	FloatTensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor
	optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.005)
	criterion = nn.MSELoss()
	for epoch in range(1, max_epoch+1):
		Logging('[INFO]: epoch now is %d...' % epoch, logfile)
		for batch_i, (X, y) in enumerate(dataloader):
			X, y = X.type(FloatTensor), y.type(FloatTensor)
			optimizer.zero_grad()
			preds = model(X)
			loss = criterion(preds, y)
			Logging('[INFO]: batch%d of epoch%d, loss is %.5f...' % (batch_i, epoch, loss.item()), logfile)
			loss.backward()
			optimizer.step()
		if (epoch % save_interval == 0) and (epoch > 0):
			pklpath = os.path.join(backupdir, 'epoch_%s.pkl' % str(epoch))
			torch.save(model.state_dict(), pklpath)


if __name__ == '__main__':
	train()