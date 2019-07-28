import os
import sys
import time
import random
import subprocess

SPACE = ' '

CWD = subprocess.check_output('pwd', shell=True).decode('utf-8').strip()
user_name = subprocess.check_output('whoami', shell=True).decode('utf-8').strip()

wall_directory = f'{CWD}'

list_of_images = os.listdir(wall_directory)

current_gsettings = subprocess.check_output('which gsettings', shell=True).decode('utf-8')


def get_random_image_name():
	rand_image_name = random.choice(list_of_images)
	return rand_image_name


def set_desktop_background(new_wall_name_with_extention):
	set_to_new_wall_adress = f'gsettings set org.mate.background picture-filename ' + f'{wall_directory}/{new_wall_name_with_extention}'

	os.system(set_to_new_wall_adress)


def check_if_has_image():
	res = subprocess.check_output(f'gsettings get org.mate.background picture-filename ', shell=True).decode('utf-8')

	if res == '':
		return False


	print(f'Current Wall is {res}')
	return True

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) < 2:
		wait_time = None
	else:
		wait_time = float(argv[1])

	print("Hello, I am the script that changes wallpapers every X Seconds")
	print("Please Make sure the script is in the wallpaper collection directory")

	if wait_time is None:
		wait_time = float(input("Enter Desired Time of Cycle in seconds"))

	while True:
		print("Brace Yourself for a new one is coming")

		time.sleep(2)  # Default sleep time
		new_image = get_random_image_name()
		set_desktop_background(new_image)
		if check_if_has_image() == False:
			print("Please fill your walls file only with images,Thank you baby :* ")
			continue
		time.sleep(wait_time)
