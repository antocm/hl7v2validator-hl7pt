from hl7apy.parser import parse_message, parse_field, parse_segment
from hl7apy import parser
from hl7apy.exceptions import UnsupportedVersion
from hl7apy.core import Field
from hl7apy.consts import VALIDATION_LEVEL
from flask import abort
from hl7validator import app
import os
import re
import pandas as pd
from datetime import datetime

classes_list = {}


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


class resultMessage:
    statusCode: str
    message: str
    details: list
    warnings: list
    resource: str
    hl7version: str

    def __init__(self):
        self.details = ""
        self.warnings = []


def set_reference(setmsg, hl7version):
    """
    Add MSH-9.3 (message structure) when missing for v2.3.1 and earlier.

    hl7apy can automatically infer message structure as MESSAGE_CODE_TRIGGER_EVENT
    (e.g., ADT^A01 -> ADT_A01), which works for most messages. However, some special
    cases need explicit handling:
    - ACK messages: structure is "ACK" (not "ACK_ACK")
    - Some ADT variants share the same structure (e.g., A04/A08/A13 all use ADT_A01)

    MSH-9.3 by HL7 standard:
    - v2.3.1 and earlier: Optional
    - v2.4 and later: Required

    We only add MSH-9.3 for v2.3.1 and earlier where it's optional. For v2.4+,
    it should already be present per the standard.
    """
    # Normalize ACK messages across all versions
    # Handle incomplete ACK formats: |ACK| or |ACK^|
    if "|ACK|" in setmsg and "|ACK^" not in setmsg:
        setmsg = setmsg.replace("|ACK|", "|ACK^ACK|")
    if "|ACK^|" in setmsg:
        setmsg = setmsg.replace("|ACK^|", "|ACK^ACK|")

    # Handle ACK messages missing MSH-9.3 for ALL versions
    # ACK is special: structure is "ACK" not "ACK_ACK"
    if "|ACK^ACK|" in setmsg and "|ACK^ACK^" not in setmsg:
        setmsg = setmsg.replace("|ACK^ACK|", "|ACK^ACK^ACK|", 1)
        app.logger.info(f"Auto-added MSH-9.3 for ACK message: ACK^ACK -> ACK^ACK^ACK")
        return setmsg

    # Only auto-add MSH-9.3 for v2.3.1 and earlier (where it's optional per HL7 standard)
    # For v2.4+, MSH-9.3 is required, so missing it is an error that should be reported
    if hl7version not in ["2.1", "2.2", "2.3", "2.3.1"]:
        return setmsg

    # Extract MSH-9 to check if MSH-9.3 is missing
    try:
        msh_segment = setmsg.split('\r')[0]
        fields = msh_segment.split('|')

        if len(fields) <= 9:
            return setmsg

        msh_9 = fields[8]
        components = msh_9.split('^')

        # Only process if we have exactly 2 components (message_code^trigger_event)
        if len(components) != 2:
            return setmsg

        message_code = components[0].strip()
        trigger_event = components[1].strip()

        if not message_code or not trigger_event:
            return setmsg

        # Special cases that don't follow MESSAGE_CODE_TRIGGER_EVENT pattern
        # For everything else, hl7apy's automatic inference works fine
        special_structures = {
            # ACK is just "ACK", not "ACK_ACK"
            ("ACK", "ACK"): "ACK",
            # ADT messages that share structures
            ("ADT", "A04"): "ADT_A01",
            ("ADT", "A08"): "ADT_A01",
            ("ADT", "A13"): "ADT_A01",
            ("ADT", "A07"): "ADT_A06",
            ("ADT", "A10"): "ADT_A09",
            ("ADT", "A11"): "ADT_A09",
            ("ADT", "A12"): "ADT_A09",
            ("ADT", "A14"): "ADT_A05",
            ("ADT", "A28"): "ADT_A05",
            ("ADT", "A31"): "ADT_A05",
        }

        structure = special_structures.get((message_code, trigger_event))

        # If it's a special case, add the structure
        if structure:
            old_msh9 = f"|{message_code}^{trigger_event}|"
            new_msh9 = f"|{message_code}^{trigger_event}^{structure}|"
            setmsg = setmsg.replace(old_msh9, new_msh9, 1)
            app.logger.info(f"Auto-added MSH-9.3: {message_code}^{trigger_event} -> {message_code}^{trigger_event}^{structure}")
        # Otherwise, let hl7apy infer it automatically (no need to add MSH-9.3)

    except Exception as e:
        app.logger.error(f"Error in set_reference: {e}")

    return setmsg


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
        for line in file:
            level, message_level = line.split(":", 1)
            if level == "Error":
                error = True
            app.logger.debug(f"Validation {level}: {message_level.strip()}")
            if {
                "level": level,
                "message": message_level,
            } not in details:
                details.append(
                    {
                        "level": level,
                        "message": message_level,
                    }
                )
    os.remove(report)

    return details, error


def hl7validatorapi(msg, validation_level='tolerant'):
    """
    Validate an HL7 v2 message.

    :param msg: The HL7 message to validate
    :param validation_level: Validation level - 'strict' or 'tolerant' (default)
    :return: Dictionary with validation results
    """
    app.logger.info("message received in hl7validatorapi: {}".format(msg))
    app.logger.info(f"validation level: {validation_level}")

    # Convert validation level string to hl7apy constant
    if validation_level and validation_level.lower() == 'strict':
        val_level = VALIDATION_LEVEL.STRICT
    else:
        val_level = VALIDATION_LEVEL.TOLERANT

    resultmessage = resultMessage()
    custom_chars = define_custom_chars(msg)
    details = []
    warnings = []  # Collect validation warnings
    status = "Success"
    msh_18 = "ASCII"
    hl7version = None
    if not msg:
        abort(404)
    error = False
    setmsg = set_message_to_validate(msg)
    try:
        parsed_msg = parse_message(setmsg, validation_level=val_level)
        hl7version = parsed_msg.version
        msh_9 = parsed_msg.msh.msh_9

        message = "Valid"
    except Exception as err:
        app.logger.error(
            "Not able to parse message: {} ----> ERROR {}".format(msg, err)
        )
        resultmessage.statusCode = "Failed"
        resultmessage.hl7version = hl7version
        resultmessage.message = "[Error parsing message] " + str(err)
        return resultmessage.__dict__
    try:
        msh_18 = parsed_msg.msh.msh_18.value
    except:
        pass
    if msh_9.value == "":
        resultmessage.statusCode = "Failed"
        resultmessage.hl7version = hl7version
        resultmessage.message = "[Error parsing message] No MSH9"
        return resultmessage.__dict__

    if msh_18 == "ASCII":
        if not setmsg.isascii():
            details.append(
                {
                    "level": "Error",
                    "message": "Message is not ASCII encoded",
                }
            )

    try:
        ### if i used parsed_msg returns error on report creation for some messages....dont know why
        parse_message(set_reference(setmsg, hl7version)).validate(
            report_file="report.txt"
        )

    except Exception as err:
        app.logger.error("Error Creating Report: {}".format(err))
        if "reference" in str(err):
            # For v2.3 and earlier, skip structure validation if reference error
            if hl7version in ["2.1", "2.2", "2.3"]:
                app.logger.info("Skipping structure validation for v2.3 message due to reference error")
                # Create empty report file so the rest of the code works
                with open("report.txt", "w") as f:
                    pass
            else:
                resultmessage.statusCode = "Failed"
                resultmessage.hl7version = hl7version
                resultmessage.message = "[Error parsing message] Error on detecting message structure. Try changing MSH-9.3"
                return resultmessage.__dict__

    details, error = read_report("report.txt", details, error)

    for seg in parse_message(setmsg).children:
        try:
            seg.validate(report_file="report.txt")

        except Exception as e:
            details, error = read_report("report.txt", details, error)
        for child in seg.children:
            try:
                child.validate(report_file="report.txt")
            except Exception as e:
                error_msg = str(e)
                # Log more descriptive error messages
                if "reference" in error_msg:
                    warning_msg = f"Validation skipped for segment {seg.name} child: missing reference structure"
                    app.logger.warning(warning_msg)
                    warnings.append(warning_msg)
                else:
                    warning_msg = f"Error validating segment {seg.name} child: {error_msg}"
                    app.logger.warning(warning_msg)
                    warnings.append(warning_msg)
                    details, error = read_report("report.txt", details, error)
    if error:
        status = "Failed"
        message = "Not valid"
    resultmessage.statusCode = status
    resultmessage.details = details
    resultmessage.warnings = warnings
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
                keyvalue = re.search(r"\S+\s\(.+\)", str(hl7)).group()
                result2[str(num) + "_" + keyvalue] = hl7.value
            except:
                result2[str(num) + "_UNKNOWN"] = hl7.value  # unknown cases

    try:
        m = parser.parse_message(msg.replace("\n", "\r"))
    except UnsupportedVersion:
        m = parser.parse_message(msg)

    file = m.msh.msh_10.value + ".csv"
    for index, child in enumerate(m.children):
        get_field(child, index)

    df = pd.DataFrame.from_dict(result2, orient="index")
    df.to_csv(file)
    return file


def build_tree_structure(msg, validation):
    """
    Build a hierarchical tree structure of the HL7 message with segments, fields, components, and subcomponents.
    Returns HTML for a collapsible tree view.
    """
    hl7version = validation["hl7version"]
    setmsg = set_message_to_validate(msg)

    # Extract field locations with errors from validation details
    error_fields = set()
    if "details" in validation and validation["details"]:
        for detail in validation["details"]:
            if detail.get("level") in ["Error", "Warning"]:
                message = detail.get("message", "")
                # Parse error messages to extract field locations
                # Examples: "Invalid datetime format on field PID.PID_7"
                #           "PID.PID_5.2: max_length is 50 and length is 51"
                import re
                # Pattern 1: "on field SEG.SEG_N" or "field SEG.SEG_N"
                match = re.search(r'field\s+([A-Z]{3})\.([A-Z]{3}_\d+)', message)
                if match:
                    segment = match.group(1)
                    field_name = match.group(2)
                    # Extract field number from field name (e.g., PID_7 -> 7)
                    field_num = field_name.split('_')[1]
                    error_fields.add(f"{segment}-{field_num}")
                else:
                    # Pattern 2: "SEG.SEG_N.C" or "SEG.SEG_N.C.S"
                    match = re.search(r'^([A-Z]{3})\.([A-Z]{3}_\d+)(\.(\d+))?(\.(\d+))?:', message)
                    if match:
                        segment = match.group(1)
                        field_name = match.group(2)
                        component = match.group(4)
                        subcomponent = match.group(6)
                        field_num = field_name.split('_')[1]

                        location = f"{segment}-{field_num}"
                        if component:
                            location += f".{component}"
                        if subcomponent:
                            location += f".{subcomponent}"
                        error_fields.add(location)

    def process_segment(segment, segment_id, hl7version):
        """Process a single segment and return HTML"""
        segment_html = ''

        # This is an actual segment - render it
        segment_html += f'''
        <div class="tree-node segment-node">
            <div class="tree-toggle" onclick="toggleNode(this)">
                <span class="toggle-icon">▶</span>
                <span class="node-id">{segment_id}</span>
                <a href="https://hl7-definition.caristix.com/v2/HL7v{hl7version}/Segments/{segment_id}"
                   target="_blank" class="spec-link" onclick="event.stopPropagation()">📖</a>
            </div>
            <div class="tree-children" style="display: none;">
        '''

        # Process fields
        for field_idx, field in enumerate(segment.children, 1):
            # Extract the actual field number from the field name (e.g., ORC_14 -> 14)
            actual_field_num = field_idx
            if hasattr(field, 'name') and '_' in field.name:
                try:
                    actual_field_num = int(field.name.split('_')[1])
                except (ValueError, IndexError):
                    actual_field_num = field_idx

            # Skip only if field has no value AND no children with values
            has_value = hasattr(field, 'value') and field.value is not None and field.value != ''
            has_children_with_values = (hasattr(field, 'children') and len(field.children) > 0
                                       and any(hasattr(c, 'value') and c.value is not None and c.value != '' for c in field.children))

            if not has_value and not has_children_with_values:
                continue

            field_long_name = getattr(field, 'long_name', None)
            # Get datatype directly from the field object
            field_datatype = getattr(field, 'datatype', None)
            field_name = (field_long_name.replace("_", " ").title() if field_long_name else 'Unknown Field')
            if field_datatype:
                field_name = f"{field_name} ({field_datatype})"

            # Debug logging for first few fields
            if segment_id == 'PID' and actual_field_num <= 5:
                app.logger.info(f"PID-{actual_field_num}: datatype={field_datatype}, field_name={field_name}")

            field_location = f"{segment_id}-{actual_field_num}"
            field_value = str(getattr(field, 'value', '')) if hasattr(field, 'value') else ''

            # Check if this field has an error
            field_has_error = field_location in error_fields
            error_class = ' error' if field_has_error else ''

            # Check if field has components
            has_components = hasattr(field, 'children') and len(field.children) > 0

            if has_components and has_children_with_values:
                # Field with components
                segment_html += f'''
                <div class="tree-node field-node">
                    <div class="tree-toggle" onclick="toggleNode(this)">
                        <span class="toggle-icon">▶</span>
                        <span class="node-id{error_class}">{field_location}</span>
                        <span class="node-name{error_class}">{field_name}</span>
                        <span class="node-value{error_class}">{field_value[:50]}{'...' if len(field_value) > 50 else ''}</span>
                    </div>
                    <div class="tree-children" style="display: none;">
                '''

                # Process components
                for comp_idx, component in enumerate(field.children, 1):
                    if not hasattr(component, 'value') or component.value is None:
                        continue

                    comp_long_name = getattr(component, 'long_name', None)
                    # Get datatype directly from the component object
                    comp_datatype = getattr(component, 'datatype', None)
                    comp_name = (comp_long_name.replace("_", " ").title() if comp_long_name else f'Component {comp_idx}')
                    if comp_datatype:
                        comp_name = f"{comp_name} ({comp_datatype})"
                    comp_location = f"{field_location}.{comp_idx}"
                    comp_value = str(component.value) if component.value else ''

                    # Check if this component has an error
                    comp_has_error = comp_location in error_fields
                    comp_error_class = ' error' if comp_has_error else ''

                    # Check if component has subcomponents
                    has_subcomponents = hasattr(component, 'children') and len(component.children) > 0

                    if has_subcomponents and any(hasattr(sc, 'value') and sc.value for sc in component.children):
                        # Component with subcomponents
                        segment_html += f'''
                        <div class="tree-node component-node">
                            <div class="tree-toggle" onclick="toggleNode(this)">
                                <span class="toggle-icon">▶</span>
                                <span class="node-id{comp_error_class}">{comp_location}</span>
                                <span class="node-name{comp_error_class}">{comp_name}</span>
                                <span class="node-value{comp_error_class}">{comp_value[:50]}{'...' if len(comp_value) > 50 else ''}</span>
                            </div>
                            <div class="tree-children" style="display: none;">
                        '''

                        # Process subcomponents
                        for subcomp_idx, subcomponent in enumerate(component.children, 1):
                            if not hasattr(subcomponent, 'value') or subcomponent.value is None:
                                continue

                            subcomp_long_name = getattr(subcomponent, 'long_name', None)
                            # Get datatype directly from the subcomponent object
                            subcomp_datatype = getattr(subcomponent, 'datatype', None)
                            subcomp_name = (subcomp_long_name.replace("_", " ").title() if subcomp_long_name else f'Subcomponent {subcomp_idx}')
                            if subcomp_datatype:
                                subcomp_name = f"{subcomp_name} ({subcomp_datatype})"
                            subcomp_location = f"{comp_location}.{subcomp_idx}"
                            subcomp_value = str(subcomponent.value) if subcomponent.value else ''

                            # Check if this subcomponent has an error
                            subcomp_has_error = subcomp_location in error_fields
                            subcomp_error_class = ' error' if subcomp_has_error else ''

                            segment_html += f'''
                            <div class="tree-node subcomponent-node">
                                <div class="tree-item">
                                    <span class="node-id{subcomp_error_class}">{subcomp_location}</span>
                                    <span class="node-name{subcomp_error_class}">{subcomp_name}</span>
                                    <span class="node-value{subcomp_error_class}">{subcomp_value}</span>
                                </div>
                            </div>
                            '''

                        segment_html += '''
                            </div>
                        </div>
                        '''
                    else:
                        # Component without subcomponents (leaf node)
                        segment_html += f'''
                        <div class="tree-node component-node">
                            <div class="tree-item">
                                <span class="node-id{comp_error_class}">{comp_location}</span>
                                <span class="node-name{comp_error_class}">{comp_name}</span>
                                <span class="node-value{comp_error_class}">{comp_value}</span>
                            </div>
                        </div>
                        '''

                segment_html += '''
                    </div>
                </div>
                '''
            else:
                # Field without components (leaf node)
                segment_html += f'''
                <div class="tree-node field-node">
                    <div class="tree-item">
                        <span class="node-id{error_class}">{field_location}</span>
                        <span class="node-name{error_class}">{field_name}</span>
                        <span class="node-value{error_class}">{field_value}</span>
                    </div>
                </div>
                '''

        segment_html += '''
            </div>
        </div>
        '''

        return segment_html

    tree_html = '<div class="hl7-tree">'

    # Parse segments directly from raw message like highlight_message does
    for seg_line in setmsg.split("\r"):
        segment_id = seg_line[0:3]
        if len(segment_id) < 3:
            continue
        try:
            parsed_segment = parse_segment(seg_line, version=hl7version)
            tree_html += process_segment(parsed_segment, segment_id, hl7version)
        except Exception as e:
            app.logger.error(f"Error parsing segment {segment_id}: {e}")
            continue

    tree_html += '</div>'

    return tree_html, validation


def highlight_message(msg, validation):
    hl7version = validation["hl7version"]

    setmsg = set_message_to_validate(msg)
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
                field_identifier = segment_id + "_" + str(idx + add)
                f = Field(field_identifier, version=hl7version)
                f.value = field

                if (
                    f.datatype == "DTM" or f.datatype == "TS"
                ) and f.value != "":  # check date format
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
                field_name = f.long_name.replace("_", " ").lower().title()
                f.validate()
            except AttributeError as e:
                # Field object is None or doesn't have expected attributes
                warning_msg = f"Could not validate field {segment_id}-{idx + add}: field may not be defined in HL7 v{hl7version} specification or has unexpected structure"
                app.logger.warning(warning_msg)
                if "warnings" not in validation:
                    validation["warnings"] = []
                validation["warnings"].append(warning_msg)
                warningfield = True
                counter -= 1
            except Exception as e:
                # Other validation errors (invalid field name, etc.)
                error_msg = str(e)
                if "Invalid name" in error_msg or "not found" in error_msg.lower():
                    warning_msg = f"Field {segment_id}-{idx + add} not found in HL7 v{hl7version} specification: {error_msg}"
                else:
                    warning_msg = f"Error validating field {segment_id}-{idx + add}: {error_msg}"
                app.logger.warning(warning_msg)
                if "warnings" not in validation:
                    validation["warnings"] = []
                validation["warnings"].append(warning_msg)
                warningfield = True
                counter -= 1

            class_ = "note"
            if field != "":
                counter += 1

                if counter > max_field or warningfield:
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
    return highligmsg, validation
