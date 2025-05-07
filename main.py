import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from pydantic import __version__ as pydantic_version

from models import Bar, Foo

NUM_THREADS = 1000


def long_running(i):
    sleep_time = 2 - (i / (NUM_THREADS * 10))
    print("long running", i, sleep_time)
    time.sleep(sleep_time)
    return Bar(baz=i)


def instantiate(i):
    return Foo(bar=[long_running(i)])


if __name__ == "__main__":
    print(f"pydantic {pydantic_version}")

    instances = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(instantiate, i) for i in range(NUM_THREADS)]

        # Wait for all threads to complete and collect results
        for future in as_completed(futures):
            instances.append(future.result())

    print(f"Created {len(instances)} instances across {NUM_THREADS} threads")
