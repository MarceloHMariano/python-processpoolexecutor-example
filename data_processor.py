import concurrent.futures
from typing import Any, Union, Callable, Collection, List, Tuple

_BeforeProcessCallback = Callable[[Any], None]
_ProcessCallback = Callable[[Any], Any]
_DoneCallback = Callable[[Any, Union[Any, BaseException]], None]


def process(data: Collection[Any],
            process_callback: _ProcessCallback,
            before_process_callback: _BeforeProcessCallback,
            done_callback: _DoneCallback = None,
            max_workers: int = None) -> List[Tuple[Any, Any]]:
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = []

        if before_process_callback is not None:
            before_process_callback(data)

        futures = {
            executor.submit(process_callback, item): item
            for item in data
        }

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except:
                result = future.exception()

            item = futures[future]
            results.append((item, result))

            done_callback(item, result)

        return results
