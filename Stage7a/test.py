from time import perf_counter
from generator import BoardGenerator

stime = perf_counter()

N = 100
for _ in range(N):
    print(_)
    b = BoardGenerator.new_board("Normal", "Expert", 9)
print((perf_counter() - stime)/N)

'''

normal easy 9 BEFORE: 0.2892594089987688
normal easy 9 AFTER: 0.3042047120002098
normal easy 9 AFTER 2: 0.28636600699974224
normal easy 9 AFTER 3: 0.31669396399986 | 0.3180331710004248
normal easy 9 AFTER 4: 0.27848525600042195
normal easy 9 FINAL: 0.29271789100021123

normal medium 9 BEFORE: 0.3684400199982338
normal medium 9 AFTER: 0.38074551899917425
normal medium 9 AFTER 2: 0.3763577209995128
normal medium 9 AFTER 3: 0.41698133800178766
normal medium 9 AFTER 4: 0.3854595820000395
normal medium 9 FINAL: 0.3706391689996235

normal hard 9 BEFORE: 0.49917770800180733
normal hard 9 AFTER: 0.4975478500011377
normal hard 9 AFTER 2: 0.5070535530010238
normal hard 9 AFTER 3: 0.6819632630003616
normal hard 9 AFTER 4: 0.48216772499959915
normal hard 9 FINAL: 0.4729874809994362

normal expert 9 BEFORE: 0.8996159069985151
normal expert 9 AFTER: 0.7395814849995077 | 0.7495513599994592
normal expert 9 AFTER 2: 1.0101816460001283 | 0.9442915490013547
normal expert 9 AFTER 3: None
normal expert 9 AFTER 4: 0.7337386769987643
normal expert 9 FINAL: 0.6248314180015586

'''
