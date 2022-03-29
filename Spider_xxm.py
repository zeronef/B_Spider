from multiprocessing import Process
from B_Spider import B_Spider

l=B_Spider()
l2=B_Spider()
p1=Process(target=l.run_2_2('37754047'))

p1.start()

p2=Process(target=l2.run_3_2('37754047'))

p2.start()