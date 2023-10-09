import subprocess
p = subprocess.run('ipconfig', shell=True, stdout=subprocess.PIPE, encoding='gbk')
print(p.stdout)