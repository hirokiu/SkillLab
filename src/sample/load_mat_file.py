import scipy.io
#mat = scipy.io.loadmat('/Users/hiroki_u/MATLAB-Drive/MobileSensorData/sensorlog_20210905_221919.mat')
#mat = scipy.io.loadmat('/Users/hiroki_u/MATLAB-Drive/MobileSensorData/sensorlog_20210905_233837.mat')
mat = scipy.io.loadmat('/Users/hiroki_u/MATLAB-Drive/test.mat')

print(mat)
print(sorted(mat.keys()))
print(mat['__header__'])
print(mat['__version__'])
print(mat['__globals__'])
#print(mat['None'])
#print(mat['None'][0][3])
#print(mat['__function_workspace__'][0].shape[0])
#print(mat['__function_workspace__'][0])

#teststruct = mat['__function_workspace__']
#print(teststruct.dtype)
#print(teststruct.size)
#print(teststruct.shape)

#for _data in mat['__function_workspace__']:
#    for _d in _data:
#        print(_d)

print(mat['matVar1'])

for _data in mat['matVar1']:
    print("x : " + str(_data[0]), end = '\t')
    print("y : " + str(_data[1]), end = '\t')
    print("z : " + str(_data[2]))

