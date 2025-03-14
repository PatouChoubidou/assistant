import numpy as np

peter = np.arange(-32767, 32768, dtype=np.int16)

print(peter)

'''
def normalize(arr):
    for i, val in enumerate(arr):
        if(i != 65535):
            if val < 0:
                val_norm = (val-32767) / (32767 - (-32767)) * 2 + 1
            elif val > 0:
                val_norm = (val-32767) / (32767 - (-32767)) * 2 + 1
            else:
                val_norm = val
        arr[i] = val_norm
    return arr

x_norm = normalize(peter)
'''

# x_norm = (np.abs(peter)- 0) / (32767 - (0)) * 2 - 1
# print(len(x_norm))

# this just does it
x_norm = (peter / 32767)

print(f"max: {np.max(x_norm)}")
print(f"min: {np.min(x_norm)}")
# print(f"position 65535 is negative sign: {x_norm[65535]}")
print(x_norm[0])
print(x_norm[int(32767/4)])
print(x_norm[int(32767/2)])
print(x_norm[int(3*(32767/4))])
print(x_norm[32767])
print(x_norm[32767+int(32767/4)])
print(x_norm[32767+int(32767/2)])
print(x_norm[32767+3*int(32767/4)])
print(x_norm[65533])
