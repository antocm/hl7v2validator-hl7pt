from hl7apy.parser import parse_segments, parse_message
from hl7apy import parser
from hl7apy.exceptions import (
    UnsupportedVersion,
    ChildNotFound,
    ValidationError,
    InvalidName,
)
from hl7apy.core import Field
from flask import abort
from message_validation_logger import app
import re
import pandas as pd


classes_list = {}


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


class resultMessage:
    statusCode: str
    message: str
    details: list
    resource: str

    def __init__(self):
        self.details = ""


def message_preprocessor(msg):
    """
    Takes a message fhir and preprocesses. Checks if is a dict and if not replaces boolean and newlines.
    :return processed message
    """
    if type(msg) == dict:
        return msg
    else:
        return (
            msg.replace("\r\n", "")
            .replace("True", '"True"')
            .replace("False", '"False"')
        )


def define_custom_chars(msg):
    """
    Create dict for custom escape characters for HL7v2 messages
    :param msg: msg to be evaluated
    :return: custom characters, nOne if default.
    """
    if "\r\n" in msg:
        return {
            "FIELD": "|",
            "COMPONENT": "^",
            "REPETITION": "~",
            "ESCAPE": "\\",
            "SUBCOMPONENT": "&",
            "GROUP": "\r\n",
            "SEGMENT": "\r\n",
        }
    elif "\r" in msg:
        return None
    else:
        return {
            "FIELD": "|",
            "COMPONENT": "^",
            "REPETITION": "~",
            "ESCAPE": "\\",
            "SUBCOMPONENT": "&",
            "GROUP": "\r",
            "SEGMENT": "\n",
        }


def hl7construct_error(err):
    """
    function for creating readable messages for hl7v2 error exceptions, in order to not create a NoneType exception and be more readable.
    :param err: error object
    :return: error as string human-readable
    """
    if type(err) == ChildNotFound:
        return "Segment with Fields with unknown children"
    return err.args[0]


def set_message_to_validate(msg):
    """
    replace newline chars for messages since parse_message does not take into account custom_chars
    :param msg:
    :return:
    """
    if "\r\n" in msg:
        return msg.replace("\r\n", "\r")
    elif "\n" in msg:
        return msg.replace("\n", "\r")
    else:
        return msg


def hl7validatorapi2(msg):
    app.logger.info("message received in hl7validatorapi: {}".format(msg))
    resultmessage = resultMessage()
    custom_chars = define_custom_chars(msg)
    details = []
    status = "Success"

    if not msg:
        abort(404)
    error = False
    setmsg = set_message_to_validate(msg)
    try:
        hl7version = parse_message(setmsg).version
        msh_10 = parse_message(setmsg).msh.msh_10.value
    except Exception as err:
        app.logger.info(
            "Strange error with message: {} ----> ERROR {}".format(msg, err)
        )
        resultmessage.statusCode = "Failed"
        resultmessage.message = "Error parsing message"
        return resultmessage.__dict__
    try:
        parse_message(setmsg).validate(report_file="report.txt")
    except:
        pass
    message = "Message v" + hl7version + " Valid"
    # read result

    # Open the file (make sure to replace 'your_file.txt' with your actual file name)
    with open("report.txt", "r") as file:
        # Read and print each line
        for idx, line in enumerate(file):
            level, message_level = line.split(":", 1)
            if level == "Error":
                error = True
            print(level, message_level)
            details.append(
                {
                    "index": str(idx + 1),
                    "level": level,
                    "message": message_level,
                }
            )
            if error:
                status = "Failed"
                message = "Message v" + hl7version + " not valid"
            resultmessage.statusCode = status
            resultmessage.details = details
            resultmessage.message = message
        # print(line.strip())  # .strip() removes leading/trailing whitespace,
    return resultmessage.__dict__


def from_hl7_to_df(msg):
    result2 = {}

    def get_field(hl7, num):
        if type(hl7) != Field:
            for child in hl7.children:
                get_field(child, num)
        else:
            try:
                # print(hl7)
                keyvalue = re.search("\S+\s\(.+\)", str(hl7)).group()
                result2[str(num) + "_" + keyvalue] = hl7.value
            except:
                result2[str(num) + "_UNKNOWN"] = hl7.value  ##unknown cases

    try:
        m = parser.parse_message(msg.replace("\n", "\r"))
    except UnsupportedVersion:
        m = parser.parse_message(msg)

    file = m.msh.msh_10.value + ".csv"
    for index, child in enumerate(m.children):
        # print(child, index)
        get_field(child, index)

    df = pd.DataFrame.from_dict(result2, orient="index")
    df.to_csv(file)
    return file
