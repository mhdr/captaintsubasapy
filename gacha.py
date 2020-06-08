from random import seed
from random import random
import time

percentage = 14
multi = 10
count = 1

index_count = 1
index_multi = 1

while index_count <= count:

    print("Gacha : " + str(index_count))

    while index_multi <= multi:
        seed()
        rand = random() * 100
        boundary = 100 - percentage

        if rand >= boundary:
            print("Multi : {0} => Win".format(index_multi))
        else:
            print("Multi : {0} => Loss".format(index_multi))

        index_multi += 1

    index_multi = 1
    index_count += 1
