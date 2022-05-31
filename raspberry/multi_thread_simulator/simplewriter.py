file_object = open('sample.txt', 'a')
for i in range(12):
    file_object.write(str('\nhello'+str(i)))
