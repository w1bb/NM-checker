import multiprocessing
import time

def f(num):
    # The code you want to execute goes here
    time.sleep(num)
    print(f"Function f was passed {num}")

if __name__ == '__main__':
    p = multiprocessing.Process(target=f, args=(0.6,))
    p.start()
    p.join(timeout=2)
    if p.is_alive():
        p.terminate()
        p.join()
        print("Function f took more than 2 seconds to complete")
    else:
        print("Function f completed within 2 seconds")