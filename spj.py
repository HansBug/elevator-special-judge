from tmodule import *

from judge import open_file, judge

if __name__ == '__main__':
    _args = args_input
    _input_file = _args.input_file
    _output_file = _args.output_file
    _error_file = _args.error_file
    _data = _args.data

    # Do the judge work
    input_list, output_list = open_file(_input_file, _output_file)
    _correct, _message, decrypted_output_list, _score = judge(input_list, output_list, _data['check_max_time'])

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

    _output_data = {}

    # Print judge result
    print(ContinuityOutputResult(
        correct=_correct,
        score=_score,
        message=_message,
        content=_content,
        data=_output_data
    ))
