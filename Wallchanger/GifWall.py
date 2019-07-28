import os
import sys
import time
import random
import subprocess
from PIL import Image
import datetime


SPACE = ' '

CWD = subprocess.check_output('pwd', shell=True).decode('utf-8').strip()
user_name = subprocess.check_output('whoami', shell=True).decode('utf-8').strip()

wall_directory = f'{CWD}'

list_of_images = os.listdir(wall_directory)

current_gsettings = subprocess.check_output('which gsettings', shell=True).decode('utf-8')

"""THIS CODE WAS TAKEN FROM GIT TO HELP SAVE EACH GIF FRAME BY FRAME"""

def analyseImage(path):
	'''
	Pre-process pass over the image to determine the mode (full or additive).
	Necessary as assessing single frames isn't reliable. Need to know the mode
	before processing all frames.
	'''
	im = Image.open(path)
	results = {
		'size': im.size,
		'mode': 'full',
	}
	try:
		while True:
			if im.tile:
				tile = im.tile[0]
				update_region = tile[1]
				update_region_dimensions = update_region[2:]
				if update_region_dimensions != im.size:
					results['mode'] = 'partial'
					break
			im.seek(im.tell() + 1)
	except EOFError:
		pass
	return results

def processImage(path):
	'''
	Iterate the GIF, extracting each frame.
	'''
	mode = analyseImage(path)['mode']

	im = Image.open(path)

	i = 0
	p = im.getpalette()
	last_frame = im.convert('RGBA')

	try:
		while True:
			#print ("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

			'''
			If the GIF uses local colour tables, each frame will have its own palette.
			If not, we need to apply the global palette to the new frame.
			'''
			if not im.getpalette():
				im.putpalette(p)

			new_frame = Image.new('RGBA', im.size)

			'''
			Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
			If so, we need to construct the new frame by pasting it on top of the preceding frames.
			'''
			if mode == 'partial':
				new_frame.paste(last_frame)

			new_frame.paste(im, (0,0), im.convert('RGBA'))
			new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')

			i += 1
			last_frame = new_frame
			im.seek(im.tell() + 1)
	except EOFError:
		pass

"""Git code ends here"""

'''We need to count how long is the loop of the gif'''


def get_avg_fps(PIL_Image_object):
	""" Returns the average framerate of a PIL Image object """
	PIL_Image_object.seek(0)
	frames = duration = 0
	while True:
		try:
			frames += 1
			duration += PIL_Image_object.info['duration']
			PIL_Image_object.seek(PIL_Image_object.tell() + 1)
		except EOFError:
			return frames / duration * 1000



def set_desktop_background(new_wall_name_with_extention):
	set_to_new_wall_adress = f'gsettings set org.mate.background picture-filename ' + f'{wall_directory}/{new_wall_name_with_extention}'

	os.system(set_to_new_wall_adress)


def frames_list(gif_name):
	ordered_list =[]
	new_image_list = os.listdir(wall_directory)
	image_name = os.path.splitext(gif_name)[0]
	i = 0
	for image in new_image_list:

		if image_name in image:
			ordered_list.append(f'{image_name}-{i}')
			i += 1


	return ordered_list

def start_giffing_away():
	for gif in list_of_images:
		if gif.endswith('.gif'):
			# if f'{gif}-3.png' not in list_of_images:
			my_gif = Image.open(gif)
			fps = get_avg_fps(my_gif)
			if len(list_of_images) < 3:
				processImage(gif)
			list_of_frames = frames_list(gif)
			return (list_of_frames,fps)




if __name__ == '__main__':

	argv = sys.argv
	if len(argv) < 2:
		wait_time = None
	else:
		wait_time = float(argv[1])

	print("Hello, I am the script that makes your GIF a WALLPAPER!!!")
	print("Exciting times")
	print("Please Make sure the script is in the GIF directory")

	# if wait_time is None:
	# 	try:
	# 		wait_time = float(input("Enter Desired Time of The Cycle in seconds,if you wish to try the default press F"))
	# 	except:
	# 		wait_time = 0
	list_of_frames,fps = start_giffing_away()
	# if wait_time == 0:
	# 	wait_time = fps
	i = 0
	while True:
		for image in list_of_frames:
			i+=1
			print(f'count-{image}')
			set_desktop_background(image+'.png')
			time.sleep(1/5)
		continue