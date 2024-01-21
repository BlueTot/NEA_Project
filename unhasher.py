hash = input().split(";")
for idx, v in enumerate(hash):
    if idx % 9 == 0 and idx != 0:
        print()
    print(v[:-1], end=' ')
    
