import sys
import getopt
from typing import Tuple
import json


def read_command_args(argv: list) -> Tuple[str, str]:
    """
    Reads and decodes the command line arguments
    :param argv: list of command line arguments, containing the names of the input and output files
    :return: the name of the files with the input and output values
    """
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <input_file> -o <output_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    if not input_file or not output_file:
        # input and output are mandatory
        print('ERROR: please specify <input_file> and <output_file>')
        print('test.py -i <input_file> -o <output_file>')
        sys.exit(3)

    return input_file, output_file


def decode_input(input_filename: str) -> dict:
    """
    Reads the input file
    :param input_filename: name of the file with the JSON input
    :return: the json-like dict with the input information
    """

    with open(input_filename) as json_file:
        try:
            decoded_data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("ERROR: input JSON is malformatted")
            sys.exit(4)

    if "keywords" not in decoded_data or not decoded_data["keywords"]:
        print("ERROR: keywords are mandatory in input")
        sys.exit(2)

    if "proxies" not in decoded_data or not decoded_data["proxies"]:
        print("ERROR: proxies are mandatory in input")
        sys.exit(3)

    return decoded_data


def write_output(json_output: list, output_filename: str):
    """
    Writes the encoded json_output the the output file
    :param json_output: JSON-like dict with the output data
    :param output_filename: filename where to write the output to
    """
    with open(output_filename, 'w') as outfile:
        json.dump(json_output, outfile)
