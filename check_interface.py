import check as C
import argparse


def check_interface(args):
    input_path = args.input_path
    if input_path == '':
        raise ValueError('Usage: ./datacheck -i <path>')

    ret = C.check(input_path)
    # ret form: (is_pass, message)
    output_info = ""
    is_pass, message = ret
    if is_pass is True:
        output_info = 'Check Pass!\t' + message
    else:
        output_info = 'Check Fail!\t' + message
    print(output_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='elevator datacheck')
    parser.add_argument('-i', dest='input_path', default='')
    #parser.add_argument('-o', dest='output_path', default='')
    args = parser.parse_args()

    check_interface(args)
