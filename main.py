import pprint
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import pydantic

from models import Bar, Foo

NUM_THREADS = 1000


def instantiate_bar_slowly(i):
    sleep_time = 2 - (i / (NUM_THREADS * 10))
    time.sleep(sleep_time)
    return Bar(baz=str(i))


def instantiate_foo(i):
    return Foo(bar=instantiate_bar_slowly(i))


if __name__ == "__main__":
    print(f"pydantic {pydantic.__version__}")
    instances = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        try:
            futures = [executor.submit(instantiate_foo, i) for i in range(NUM_THREADS)]
            for future in as_completed(futures):
                instances.append(str(future.result()))
        except pydantic.errors.PydanticUserError as e:
            # Log exception to file.
            with open("errors.log", "a", newline="\n") as log_file:
                log_file.write(f"\n------------------------ {time.time()}\n")
                log_file.write(str(e))
                log_file.write(pprint.pformat(locals()))
                traceback.TracebackException.from_exception(e).print(file=log_file)
            raise
    print(f"Created {len(instances)} instances across {NUM_THREADS} threads")
