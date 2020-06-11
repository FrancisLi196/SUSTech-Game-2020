'''
Function:
	CNN simulate Game of Life.
'''
import os
import torch
import imageio
import argparse
import matplotlib.pyplot as plt
from traine import lifeGame
from myModel import myModel


'''png -> gif'''
'''
def png2gif(pngdir, savename='result.gif'):
	pngpaths = sorted(os.listdir(pngdir))
	images = []
	for pngpath in pngpaths:
		if pngpath.split('.')[-1] != 'png':
			continue
		images.append(imageio.imread(os.path.join(pngdir, pngpath)))
		#os.remove(os.path.join(pngdir, pngpath))
	imageio.mimsave(os.path.join(pngdir, savename), images)
'''
def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.1)
    return


def png2gif(pngdir):
	pngpaths = sorted(os.listdir(pngdir))
	images = []
	for pngpath in pngpaths:
		if pngpath.split('.')[-1] != 'png':
			continue
		images.append(imageio.imread(os.path.join(pngdir, pngpath)))
		#os.remove(os.path.join(pngdir, pngpath))
	#imageio.mimsave(os.path.join(pngdir, savename), images)
	maine()


def maine():
    image_list = ["//Users/saya/PycharmProjects/CNN gol step1/results/" + str(x) + ".png" for x in range(0, 149)]
    gif_name = 'created_gif.gif'
    create_gif(image_list, gif_name)





'''demo to show the results'''
def demo(weightfile, num_frames=150):
	if not os.path.exists('results'):
		os.mkdir('results')
	model = myModel()
	model.load_state_dict(torch.load(weightfile))
	game = lifeGame()
	use_cuda = torch.cuda.is_available()
	if use_cuda:
		model = model.cuda()
	model.eval()
	FloatTensor = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor
	frame = game.initGame()
	frame_cnn = frame.copy()
	shape = frame.shape
	for i in range(num_frames):
		fig = plt.figure()
		plt.title('Left: Game of life || Iteration: %s || Right: CNN prediction' % i)
		ax = fig.add_subplot(121)
		_ = ax.matshow(frame, vmin=0, vmax=1, cmap='gray')
		ax = fig.add_subplot(122)
		_ = ax.matshow(frame_cnn, vmin=0, vmax=1, cmap='gray')
		plt.savefig("results/%d.png" % (i))
		frame = game.nextFrame(frame)
		frame_cnn = model(torch.from_numpy(frame_cnn).float().reshape(1, 1, *shape).type(FloatTensor)).cpu().data.numpy().reshape(shape)
	png2gif('results')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="use cnn to simulate Game of Life.")
	parser.add_argument('-m', dest='model', help='The trained model path.')
	args = parser.parse_args()
	if args.model:
		demo(args.model)
#       python demo.py -m weights/epoch_6.pkl