import scipy.io
import glob
import os
from playsound import playsound


directory = '/Users/prantikbarua/SkillLab/work/2023/ne201059/Logdata/SkillLab/'
file_pattern = '*.mat'

# ディレクトリ内の一致するファイルのリストを取得
files = glob.glob(os.path.join(directory, file_pattern))

# ファイルの作成日時を取得して、最新のファイルを選択
latest_file = max(files, key=os.path.getctime)

# 最新のファイルを読み込む
mat = scipy.io.loadmat(latest_file)
# list_of_files = glob.glob('/Users/prantikbarua/SkillLab/Logdata/SkillLab/*')
# latest_file = max(list_of_files, key=os.path.getctime)


# .matファイルの読み込み
# mat = scipy.io.loadmat('/Users/prantikbarua/SkillLab/Logdata/SkillLab/latest_file')

# データの表示
# print(mat)
# print(sorted(mat.keys()))
# print(mat['__header__'])
# print(mat['__version__'])
# print(mat['__globals__'])
print(mat['None'])
print(mat['None'][0][3])
print(latest_file)
#print(mat['__function_workspace__'][0].shape[0])
#print(mat['__function_workspace__'][0])

#teststruct = mat['__function_workspace__']
#print(teststruct.dtype)
#print(teststruct.size)
#print(teststruct.shape)

#for _data in mat['__function_workspace__']:
#    for _d in _data:
#        print(_d)

for _data in mat['None']:
     print("x : " + str(_data[0][0]), end = '\t')
     print("y : " + str(_data[0][1]), end = '\t')
     print("z : " + str(_data[0][2]))
    # print("y : " + str(_data[1]), end = '\t')
    # print("z : " + str(_data[2]))

#動画を再生する
playsound("arupakaraspi.mp3")

