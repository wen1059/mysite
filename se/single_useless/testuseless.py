import re



regx = re.compile(r'峰号.+?\.gcd', re.S)
ress = regx.findall(s1)
for res in ress:
    lines = [i.split() for i in res.splitlines()]
    print(lines)
    samplename = lines[-1][-1].replace('.gcd', '')
    area = lines[1][2]
    print(samplename, area)
