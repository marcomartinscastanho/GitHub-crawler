#!/usr/bin/env python3

import sys

from src.io import read_command_args, decode_input, write_output
from src.network import encode_request, get_random_proxy, send, decode_query_response, add_extra_information


def main(argv):
    # read command arguments
    input_filename, output_filename = read_command_args(argv)
    # decode input
    json_input = decode_input(input_filename)
    # encode request
    request_url = encode_request(json_input)
    # get a random proxy
    proxy = get_random_proxy(json_input)
    # send request
    response = send(request_url, proxy)
    # decode response
    json_output = decode_query_response(response["text"])
    # add extras
    if json_input["type"] == 'Repositories':
        add_extra_information(json_output, proxy)
    # write output
    write_output(json_output, output_filename)

    print("Done!")


main(sys.argv[1:])
