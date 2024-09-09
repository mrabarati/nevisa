import os


for root, folder, file in os.walk("."):
	for dir in folder:
		if "__pycache__" in dir or "migrations" in dir:
			print("Root ==> ", root)

			print("dir ==> ", dir)
			
			try:
				os.system("rm -rf {}".format(root+'/'+dir))
				print(f"removed folder ==> {root+dir}")
			except Exception as e:
				print(e)
