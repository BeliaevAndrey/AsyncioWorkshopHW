from multiprocessing import Process, Array as MPArr     # , Pipe
# from time import time_ns

__all__ = ['multiproc_count', ]


def _gen_counter_mp(start: int, end: int, arr: MPArr, index: int):
    result = sum((i for i in range(start, end)))
    arr[index] = result


def _tear_apart(number: int, parts: int) -> list[(int, int)]:
    portions = []
    check = 0
    part = number // parts
    n1 = 0
    n2 = part

    while check < number:
        portions.append((n1, n2))
        n1 = n2
        n2 += part
        if n2 > number:
            portions[-1] = (n1 - part, number + 1)
        check = portions[-1][1]
    # print(f'{portions = }')
    return portions


def multiproc_count(number: int, parts: int) -> int:
    arr = MPArr('Q', [0] * parts)
    portions = _tear_apart(number, parts)
    processes = []
    for index, portion in enumerate(portions):
        processes.append(
            Process(
                target=_gen_counter_mp,
                args=(*portion, arr, index)
            )
        )

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    result = sum(arr[:])
    # print(f"\n\nmultiproc_count\n{result=}\n\n")
    return result
