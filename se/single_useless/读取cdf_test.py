from netCDF4 import Dataset

dc = Dataset(r"C:\ttmp\a85258505.CDF")
print(dc)
keys = dc.variables.keys()
print(keys)
for key in keys:
    if key!='intensity_values':
        continue
    print(key)
    v = dc.variables[key]

    # values_nc = v.ncattrs()
    # print(values_nc)

    values = list(v[:])
    print(values)
