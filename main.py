import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from pydantic import __version__ as pydantic_version

from models import Bar, Foo


def long_running(i):
    print("long running", i)
    time.sleep(2 - (i / 10000))
    return Bar(baz=1)


def instantiate(i):
    # Create multiple instances in each thread to increase pressure
    foo = Foo(bar=[long_running(i)])
    return 1


if __name__ == "__main__":
    # https://github.com/pydantic/pydantic/issues/11849

    print(f"pydantic {pydantic_version}")
    NUM_THREADS = 1000
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [
            executor.submit(instantiate, i) for i, _ in enumerate(range(NUM_THREADS))
        ]

        # Wait for all threads to complete and collect results
        total_instances = 0
        for future in as_completed(futures):
            total_instances += future.result()

    print(f"Created {total_instances} instances across {NUM_THREADS} threads")
