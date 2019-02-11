import json
import shutil
import sys
from json import JSONDecodeError
from urllib.error import URLError

import config
from function import handler
from function import preprocess_params


def get_params_from_stdin() -> dict:
    buf = ""
    while True:
        line = sys.stdin.readline()
        buf += line
        if line == "":
            break
    return json.loads(buf)


def handle_error(error, message='Unknown error, please ask the admins to check container logs for more info'):
    raise error
    # This will be written to container logs
    sys.stderr.write(str(error))

    # This will be sent back to caller/server
    start = "Error from function: "

    if type(error) is not ValueError:
        content = start + str(message)
    else:
        content = start + str(error)
    print(json.dumps({"function_status": "error",
                      "content": content}))


# Please give me content that JSON-dumpable:
#   e.g. a string, could be base64-encoded, or some JSON-like object
def handle_success(content):
    print(json.dumps({"function_status": "success",
                      "content": content}))


if __name__ == "__main__":

    try:
        # Get and parse params
        # params = get_params_from_stdin()
        params = json.load(open('samples/swz_tiny_req.json'))

        # Mutate the params to get them ready for use
        preprocess_params.preprocess(params)

        # Run!
        function_response = handler.run_function(params)
        handle_success(function_response)

    except JSONDecodeError as e:
        handle_error(e, "Request received by function is not valid JSON. Please check docs")

    except URLError as e:
        handle_error(e, "Problem downloading files. Please check URLs passed as parameters are "
                        "valid, are live and are publicly accessible.")

    # Bare exceptions are not recommended - see https://www.python.org/dev/peps/pep-0008/#programming-recommendations
    # We're using one to make sure that _any_ errors are packaged and returned to the calling server,
    # not just logged at the function gateway
    except Exception as err:
        handle_error(err, "Unknown error")

    finally:
        shutil.rmtree(config.TEMP)
