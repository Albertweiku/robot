import pickle

def save(data):
    f = open('result.txt','w')
    data = str(data)
    f.write(data)
    f.close()

def load():
    f = open('result.txt','r')
    data = f.read()
    f.close()
    return data

save(3)
data=load()
print(data)
data = int(data)
print(type(data))