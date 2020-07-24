import logging
from typing import Any, Union, Collection

import data_processor

logging.basicConfig(level=logging.DEBUG)


def before_process(data: Collection[Any]) -> None:
    logging.info(f'Iniciando o processamento de {len(data)} itens')


def process(item: Any) -> Any:
    return item * 2


def done(item: Any, result: Union[Any, BaseException]) -> None:
    if isinstance(result, BaseException):
        logging.error(str(result))
        return

    logging.info(f'{str(item)}: {str(result)}')


def main() -> None:
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    processed_data = data_processor.process(data,
                                            process_callback=process,
                                            before_process_callback=before_process,
                                            done_callback=done)
    print(processed_data)


if __name__ == '__main__':
    main()
