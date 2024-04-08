from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import os
import base64
# please set path to chrome or firefox
# PATH = r"C:/chromedriver_win32/chromedriver.exe"


def get_images_from_google(wd, delay, max_images, url):
	print("Get_Images_From_Google Called!")
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
		
		if len(thumbnails) == 0:
			break

		for img in thumbnails[len(image_urls) + skips:max_images]:
			print(img)
			try:
				print("Inside Try")
				img.click()
				time.sleep(delay)
			except:
				print("Inside Except")
				continue
			
			print("Outside Loop")
			images = wd.find_elements(By.CLASS_NAME, "sFlh5c")
			print("Images Found :")
			print(images)
			i=1
			for image in images:
				print("Inside Image For Loop")
				# print(image.get_attribute("src").split(",")[-1])
				imgdata = base64.b64decode(str(image.get_attribute("src").split(",")[-1]))
				# print(imgdata)
				print(f"writing file some_image{i}.jpeg")
				filename = f"some_image{i}.jpeg"
				with open(filename,'wb') as f:
					f.write(imgdata)
				# if image.get_attribute('src') in image_urls:
				# 	print("Found Image Source")
				# 	max_images += 1
				# 	skips += 1
				# 	break

				# if image.get_attribute('src') and 'http' in image.get_attribute('src'):
				# 	image_urls.add(image.get_attribute('src'))
				# 	print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url,file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

def download_images(urls, vegetable,folder_name):
	try:
		os.mkdir(vegetable)
	except Exception as e:
		print(e)
	try:
		os.mkdir(f"{vegetable}/{folder_name}")
	except Exception as e:
		print(e)
	for i, url in enumerate(urls):
		download_image(f"{vegetable}/{folder_name}/", url, str(i) + ".jpg")

wd = webdriver.Chrome()

with open("./input.txt") as f:
	lines = f.readlines()

lines = [x.replace("\n", "") for x in lines]
urls = get_images_from_google(wd, 1, 5, lines[1])

download_images(urls, lines[3], lines[2])

print(lines)
wd.quit()

# get_images_from_google takes google images as url and stores it in folder mentioned in download_image
# download_image does not create folder