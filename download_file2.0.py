import requests
import sys
import tqdm
import multitasking
# import threading
from colorama import init,Fore
from urllib import parse as up
import signal
import os

init(autoreset=True)
sss = ["/","|","\\"]
signal.signal(signal.SIGINT, multitasking.killall) # Ctrl-C 关闭所有进程
class Download():
	def __init__(self, url, file, num):
		self.url = url
		self.file = file
		self.file_obj = open(file, "wb")
		self.num = num
		self.headers = {"Connection":"keep-alive", "Host":up.urlsplit(url).netloc, "Content-type":"text/plain", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42"}

		
	def split(self, start: int, end: int, step: int) -> list[tuple[int, int]]:
    # 分多块
		parts = [(start, min(start+step, end))for start in range(0, end, step)]
		return parts

	def download(self):
		print(Fore.BLUE + '''
   _____               _____                               
  / ____|             |  __ \                              
 | |  __ _   _  ___   | |__) |   _  ___  _   _  __ _  ___  
 | | |_ | | | |/ _ \  |  _  / | | |/ _ \| | | |/ _` |/ _ \ 
 | |__| | |_| | (_) | | | \ \ |_| | (_) | |_| | (_| | (_) |
  \_____|\__,_|\___/  |_|  \_\__,_|\___/ \__, |\__,_|\___/ 
                                          __/ |            
                                         |___/                      
			''')
		try:
			self.html = requests.get(self.url, headers=self.headers, stream=True)
			print(Fore.GREEN + "OK,访问成功")
		except Exception:
			print(Fore.RED + "访问失败")
			self.file_obj.close()
			return 1
		try:
			str_num = int(self.html.headers["Content-Length"])
		except Exception:
			str_num = -1

		self.str_num = str_num
		print(Fore.BLUE + "数据长度：" + str(str_num))
		print(Fore.BLUE + """
   _____ _______       _____ _______ 
  / ____|__   __|/\   |  __ \__   __|
 | (___    | |  /  \  | |__) | | |   
  \___ \   | | / /\ \ |  _  /  | |   
  ____) |  | |/ ____ \| | \ \  | |   
 |_____/   |_/_/    \_\_|  \_\ |_|   
                                     
                                     
		""")

		self.progress = tqdm.tqdm(total=self.str_num, desc="下载进度")
		self.write_num = 0
		splits = self.split(0, self.str_num, self.num)

		# self.running_threads = []
		sdl = 0
		for a in self.html.iter_content(chunk_size=self.num):
			# self.write_file()
			# thread = threading.Thread(target = self.write_file, args=(a, self.write_num, sss[sdl%len(sss)]))
			# processing.append(thread)
			self.write_file(a, splits[sdl], sss[sdl%len(sss)])
			# self.running_threads.append("Thread")
			sdl += 1


		multitasking.wait_for_tasks()
		self.progress.close()
		self.file_obj.close()
		print(Fore.BLUE + """
  ______ _   _ _____  
 |  ____| \ | |  __ \ 
 | |__  |  \| | |  | |
 |  __| | . ` | |  | |
 | |____| |\  | |__| |
 |______|_| \_|_____/ 
                      
                      
			""")

		# return 0
		# self.file_obj.close()
		return 0
	@multitasking.task
	def write_file(self, string, step, echo):
		# print("正在读取")
		h = string
		# print("读取完毕")
		# print("正在写入")
		self.file_obj.seek(step[0])
		self.file_obj.write(h)
		# print("写入完成")
		self.write_num += len(h)
		# print(Fore.BLUE + f"写入：{self.write_num}个字符，一共：{self.str_num}个字符，还剩：{self.str_num-self.write_num}，进度：{self.str_num/self.write_num*100}%，{echo}")
		self.progress.update(len(h))
		# self.running_threads.remove("Thread")
		# print("Remove Thread")


#########
def main():
	url = sys.argv[1]
	try:
		speed = sys.argv[2]
		speed = int(speed)
	except Exception:
		speed = 8192
	try:
		filename = sys.argv[3]
	except Exception:
		if up.unquote(up.urlsplit(url).path.split("/")[-1]) != "":
			filename = up.unquote(up.urlsplit(url).path.split("/")[-1])
		else:
			filename = up.urlsplit(url).hostname+".html"

	# print("ok")
	o = Download(url, filename, speed)
	# print("1111")
	o.download()

if __name__ == '__main__':
	main()