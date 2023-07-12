import subprocess

p = subprocess.run('ipconfig', stdout=subprocess.PIPE)
print(str(p.stdout, encoding='gbk'))
p = subprocess.run('pause', shell=True)
