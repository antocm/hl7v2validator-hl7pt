from hl7apy.parser import parse_segments, parse_message
from hl7apy import parser
from hl7apy.exceptions import UnsupportedVersion, ChildNotFound, ValidationError,InvalidName
from hl7apy.core import Component, Field
import re

def message_preprocessor(msg):
    """
    Takes a message fhir and preprocesses. Checks if is a dict and if not replaces boolean and newlines.
    :return processed message
    """
    if type(msg) == dict:
        return msg
    else:
        return (msg.replace('\r\n', '').replace("True", "\"True\"").replace("False", "\"False\""))



def define_custom_chars(msg):
    """
    Create dict for custom espace characters for HL7v2 messages
    :param msg: msg to be evaluated
    :return: custom characters, nOne if default.
    """
    if "\r\n" in msg:
        return {'FIELD': '|', 'COMPONENT': '^', 'REPETITION': '~', 'ESCAPE': '\\',
                'SUBCOMPONENT': '&', 'GROUP': '\r\n', 'SEGMENT': '\r\n'}
    elif "\r" in msg:
        return None
    else:
        return {'FIELD': '|', 'COMPONENT': '^', 'REPETITION': '~', 'ESCAPE': '\\',
                'SUBCOMPONENT': '&', 'GROUP': '\r', 'SEGMENT': '\n'}


def hl7construct_error(err):
    """
    function for creating readable messages for hl7v2 error exceptions, in order to not create a NoneType exception and be more readable.
    :param err: error object
    :return: error as string human-readable
    """
    if type(err) == ChildNotFound:
        return "Segment with Fields with unknown children"
    if type(err)== ValidationError and re.search("Datatype None is not correct for \w{3}.", err.args[0]):
        hl7field=re.findall("\w{3}.\w{3}_\d+",err.args[0])
        return "Datatype correct for "+hl7field[0]
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


def hl7validatorapi(msg):
 #   app.logger.info('message received in hl7validatorapi: {}'.format(msg))

    custom_chars = define_custom_chars(msg)
    hl7version="2.4"
    details = []
    if not msg:
        pass
     #   abort(404)
    error = False
    setmsg=set_message_to_validate(msg)
    try:
        hl7version = parse_message(setmsg).version
        msh_10 = parse_message(setmsg).msh.msh_10.value
    except Exception as err:
      #      print(err)
        return {'statusCode': 'Failed', 'message': "Error parsing message"}
    try:
        parse_message(setmsg).validate(report_file="report.txt")
    except (ValidationError, AttributeError, InvalidName) as err:
        if re.search("Missing required child \w{3}_", err.args[0]):
                return {'statusCode': 'Failed', 'message': "Message Not Valid",
                                       "details": [{"error": str(err.args[0])}]}
        else:
         #  app.logger.info('Strange error with message: {} ----> ERROR {}'.format(msg, err))
            pass
            #                     "details": [{"error": str(err.args[0])}]}

    try:
        for index, n in enumerate(parse_segments(msg, encoding_chars=custom_chars, version=hl7version)):

            try:
                n.validate(report_file="report.txt")
                if not error:
                    response = {'statusCode': "Success", "message": "Message Valid", "details": ""}
                if n.name == 'MSH':
                    title = n.msh_9.msh_9_1.value + "^" + n.msh_9.msh_9_2.value

            except Exception as err:
                err_constructed = hl7construct_error(err)
                error = True
                details.append({"index": str(index + 1), "segment": n.name, "error": err_constructed})

                errors = "error"
                if len(details) > 1:
                    errors = "errors"
                response = {'statusCode': "Failed",
                            "message": "Message not valid with " + str(len(details)) + " " + errors,
                            "details":
                                details}
    except Exception as err:
        response = {'statusCode': 'Failed', 'message': "Error validating message", "details": ""}
    return response


message="""MSH|^~\&|SONHO|CHTV|SIEMENS|CHTV|20200213090006||ADT^A01^ADT_A01|11915430-3deb-4bff-8b09-b6f82163f5ea|P|2.5||||||
EVN|A01|20200213120000|20200213120000||1532^ESMERALDA MARISA ALVES^^^^^^^SONHO||CHTV
PID|1||191929^^^SONHO^NS~285151651^^^RNU^SNS~03137340^^^IRN^B~119768062^^^AT^NIF||COSTA^MANUEL^PAIS^^^^L||19471015000000|M|||AVD AFONSO CERQUEIRA, LTE 2. B, 2.FTE^^VISEU^VISEU^3500-031^^^VISEU^182324||^PRN^PH^^^^^^^^^920397335|||M||98000862^^^SONHO|||||PT 180000 182309|||PT^^ISO 3166||||N|||20200107000000|
PV1|1|CON|3^60^^^^^^^^^SONHO|||20637^^^^^^^^CONS. OFTALMOLOGIA|47235^MIGUEL COSTA RIBEIRO^^^^^^^SONHO|||||||2^CONSULTA EXTERNA|||||^^^|||||||||||||||||||||||||||||||^^^^TAX~80002114^^^^BLO_NUM_REG
PV2|^^^^^^^^
IN1|1|935601^SERVICO NACIONAL DE SAUDE^SONHO|||||||||||||||||||||||||||||||||||||||||||||||285151651^^^SONHO"""


print(hl7validatorapi(message))