import random
from concurrent.futures import ProcessPoolExecutor, as_completed


def count1():
    sum, count = 0, 0
    while True:
        sum += random.uniform(0, 1)
        count += 1
        if sum > 1:
            return count


def main(n):
    countall = 0
    for i in range(n):
        countall += count1() / n
    # print(countall)
    return countall


if __name__ == '__main__':
    with ProcessPoolExecutor() as ex:
        tasks = [ex.submit(main, 100000000) for i in range(16)]
        print(sum(i.result() for i in as_completed(tasks)) / 16)
