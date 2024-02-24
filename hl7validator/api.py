from hl7apy.parser import parse_message
from hl7apy import parser, utils
from hl7apy.exceptions import (
    UnsupportedVersion,
)
from hl7apy.core import Field
from flask import abort
from hl7validator import app
import re
import pandas as pd
from hl7apy.parser import parse_segment
from datetime import datetime
import re

import os

classes_list = {}


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


class resultMessage:
    statusCode: str
    message: str
    details: list
    resource: str
    hl7version: str

    def __init__(self):
        self.details = ""


def check_simple_format(value):
    # Define pattern for checking the format
    date_pattern = r"\d{4}(\d{2}(\d{2})?)?"

    # Check if the value matches the expected pattern
    if not re.match(date_pattern, value):
        return False, "Value does not match the expected format."

    # Try to parse the value up to the highest precision provided
    format_str = "%Y"
    if len(value) > 4:
        format_str += "%m"
    if len(value) > 6:
        format_str += "%d"

    try:
        parsed_date = datetime.strptime(value, format_str)
    except ValueError:
        return False, "Failed to parse date."

    return True, "Format is valid."


def check_format(value):
    # Split the datetime and timezone parts, if a timezone is present
    parts = value.split("+") if "+" in value else value.split("-")
    datetime_part = parts[0]
    timezone_part = (
        "+" + parts[1]
        if len(parts) > 1 and "+" in value
        else "-" + parts[1]
        if len(parts) > 1
        else None
    )

    # Define patterns for checking the format
    datetime_pattern = r"\d{4}(\d{2}(\d{2}(\d{2}(\d{2}(\d{2}(\.\d{1,4})?)?)?)?)?)?"
    timezone_pattern = r"[+-]\d{4}"

    # Check if the datetime part matches the expected pattern
    if not re.match(datetime_pattern, datetime_part):
        return False, "Datetime part does not match the expected format."

    # If a timezone part is present, check if it matches the expected pattern
    if timezone_part and not re.match(timezone_pattern, timezone_part):
        return False, "Timezone part does not match the expected format."

    # Try to parse the datetime part up to the highest precision provided
    # The format varies depending on the length of the datetime part
    format_str = "%Y"
    if len(datetime_part) > 4:
        format_str += "%m"
    if len(datetime_part) > 6:
        format_str += "%d"
    if len(datetime_part) > 8:
        format_str += "%H"
    if len(datetime_part) > 10:
        format_str += "%M"
    if len(datetime_part) > 12:
        format_str += "%S"

    try:
        parsed_datetime = datetime.strptime(datetime_part, format_str)
    except ValueError:
        return False, "Failed to parse datetime part."

    return True, "Format is valid."


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
    elif "\r" not in msg:
        return msg + "\r"
    else:
        return msg


def read_report(report, details, error):
    with open(report, "r") as file:
        # Read and print each line
        for line in file:
            # print(line)
            level, message_level = line.split(":", 1)
            if level == "Error":
                error = True
            print(level, message_level)
            details.append(
                {
                    "level": level,
                    "message": message_level,
                }
            )
    os.remove(report)

    return details, error


def hl7validatorapi(msg):
    app.logger.info("message received in hl7validatorapi: {}".format(msg))
    resultmessage = resultMessage()
    custom_chars = define_custom_chars(msg)
    details = []
    status = "Success"
    hl7version = None
    if not msg:
        abort(404)
    error = False
    setmsg = set_message_to_validate(msg)
    try:
        hl7version = parse_message(setmsg).version
        msh_9 = parse_message(setmsg).msh.msh_9.value
        print(msh_9)
        message = "Message v" + hl7version + " Valid"
        msh_18 = parse_message(setmsg).msh.msh_18.value
    except Exception as err:
        app.logger.error(
            "Not able to parse message: {} ----> ERROR {}".format(msg, err)
        )
        print(err)
        resultmessage.statusCode = "Failed"
        resultmessage.hl7version = hl7version
        resultmessage.message = "[Error parsing message] " + str(err)
        return resultmessage.__dict__
    if msh_9 == "":
        resultmessage.statusCode = "Failed"
        resultmessage.hl7version = hl7version
        resultmessage.message = "[Error parsing message] No MSH9"
        return resultmessage.__dict__
    if msh_18 == "ASCII" or msh_18 == "":
        if not setmsg.isascii():
            details.append(
                {
                    "level": "Error",
                    "message": "Message is not ASCII encoded",
                }
            )

    try:
        # print(msg)
        app.logger.info(
            "Validating this message after transformation: {}".format(setmsg)
        )
        parse_message(setmsg, find_groups=True).validate(
            report_file="report.txt",
        )

    except Exception as err:
        app.logger.error(
            "Strange error with message: {} ----> ERROR {}".format(msg, err)
        )

    details, error = read_report("report.txt", details, error)

    if error:
        status = "Failed"
        message = "Message v" + hl7version + " not valid"
    resultmessage.statusCode = status
    resultmessage.details = details
    resultmessage.hl7version = hl7version
    resultmessage.message = message

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


def highlight_message(msg, validation):
    hl7version = validation["hl7version"]

    setmsg = set_message_to_validate(msg)
    # print(hl7version)
    highligmsg = ""
    for seg in setmsg.split("\r"):
        segment_id = seg[0:3]
        if len(segment_id) < 3:
            continue
        try:
            p = parse_segment(seg, version=hl7version)

        except Exception as e:
            return "<p> [Error parsing message] </p>" + str(e), validation
        max_field = 0
        list_of_segments = []
        for s in p.children:
            # print(s)
            if "Field of type None" not in str(s) and str(s) not in list_of_segments:
                max_field += 1
                list_of_segments.append(str(s))
        newseg = (
            '<span style="margin-right: 5px;"><b>'
            + '<a href="https://hl7-definition.caristix.com/v2/HL7v'
            + hl7version
            + "/Segments/"
            + segment_id
            + '" target="_blank">'
            + segment_id
            + "</a></b></span>"
        )
        counter = 0
        for idx, field in enumerate(seg.split("|")[1:]):
            warningfield = False
            field_name = "Unknown field"
            if segment_id == "MSH":
                add = 2
            else:
                add = 1
            try:
                f = Field(segment_id + "_" + str(idx + add), version=hl7version)
                f.value = field
                field_name = f.long_name.replace("_", " ").lower().title()
                f.validate()
                if f.datatype == "DTM" and f.value != "":  # check date format
                    print(f.value)
                    chk, _ = check_format(f.value)
                    if not chk:
                        warningfield = True

                        validation["details"].append(
                            {
                                "level": "Error",
                                "message": "Invalid datetime format on field "
                                + segment_id
                                + "."
                                + f.name,
                            }
                        )
                if f.datatype == "DT" and f.value != "":  # check date format
                    print(f.value)
                    chk, _ = check_simple_format(f.value)
                    if not chk:
                        warningfield = True

                        validation["details"].append(
                            {
                                "level": "Error",
                                "message": "Invalid date format on field "
                                + segment_id
                                + "."
                                + f.name,
                            }
                        )

            except Exception as e:
                #  print(e)
                warningfield = True
                counter -= 1
            class_ = "note"
            if field != "":
                # print(field != "", field)
                counter += 1

                if counter > max_field or warningfield:
                    #  print(counter, max_field)
                    #  print("error on", field)
                    class_ = "note error"
            if segment_id == "MSH" and idx == 0:
                newseg += (
                    '<span class="span-group"><span class="tooltiptext">'
                    + "Field Separator"
                    + '</span><span  class="'
                    + class_
                    + '">'
                    + segment_id
                    + "-"
                    + "1"
                    + '</span><span class="field main-content">'
                    + "|"
                    + "</span></span>"
                )
            newseg += (
                '<span class="span-group"><span class="tooltiptext">'
                + field_name
                + '</span><span class="'
                + class_
                + '">'
                + segment_id
                + "-"
                + str(idx + add)
                + '</span><span class="field main-content">'
                + field
                + "</span></span>"
            )
        highligmsg += '<p class="segment ' + segment_id + '">' + newseg + "</p>"
    # print(highligmsg)
    return highligmsg, validation
