import io
import re
from typing import List

from pyspj import pyspj_entry

from judge import judge

__VERSION__ = '0.0.2'

PRETIME_PATTERN = re.compile(r'^\[\s*\d+\.\d+\](.*)')


def _remove_pretime(s: str) -> str:
    match = PRETIME_PATTERN.match(s)
    return match.group(1)


def _tail_strip(lst: List[str]) -> List[str]:
    i = len(lst)
    while i > 0 and not lst[i - 1]:
        i -= 1
    return lst[:i]


def spj_func(stdin: io.TextIOBase, stdout: io.TextIOBase,
             check_max_time=None, need_decrypt=None):
    check_max_time = not not check_max_time
    need_decrypt = not not need_decrypt
    no_pretime = True

    input_list = _tail_strip(list(map(str.strip, stdin)))
    output_list = _tail_strip(list(map(str.strip, stdout)))
    print(output_list)
    if no_pretime:
        output_list = list(map(_remove_pretime, output_list))

    _correct, _message, decrypted_output_list, _score = judge(
        input_list, output_list,
        check_max_time, need_decrypt
    )

    message_and_content = _message.split(' | ')
    if len(message_and_content) != 2:
        _message = _message
        _content = ''
    else:
        _message = message_and_content[0]
        _content = message_and_content[1] + '\n'
    _content += 'Your real output is listed as follows:\n'
    for output in decrypted_output_list:
        _content += output + '\n'

    return _correct, _message, _content


if __name__ == '__main__':
    pyspj_entry(
        'elevator-2-spj', spj_func,
        version=__VERSION__,  # optional
        author='HansBug',  # optional
        email='hansbug@buaa.edu.cn',  # optional
    )()
