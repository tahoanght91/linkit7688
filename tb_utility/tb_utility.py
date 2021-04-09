from re import search
from os import path, listdir
from inspect import getmembers, isclass
from logging import getLogger
from simplejson import dumps, loads, JSONDecodeError
from platform import system

log = getLogger("service")


class TBUtility:
    # Buffer for connectors/converters
    # key - class name
    # value - loaded class
    loaded_extensions = {}

    @staticmethod
    def decode(message):
        try:
            if isinstance(message.payload, bytes):
                content = loads(message.payload.decode("utf-8", "ignore"))
            else:
                content = loads(message.payload)
        except JSONDecodeError:
            try:
                content = message.payload.decode("utf-8", "ignore")
            except JSONDecodeError:
                content = message.payload
        return content

    @staticmethod
    def validate_converted_data(data):
        error = None
        if error is None and not data.get("deviceName"):
            error = 'deviceName is empty in data: '
        if error is None and not data.get("deviceType"):
            error = 'deviceType is empty in data: '
        if error is None and not data.get("attributes") and not data.get("telemetry"):
            error = 'No telemetry and attributes in data: '
        if error is not None:
            json_data = dumps(data)
            if isinstance(json_data, bytes):
                log.error(error + json_data.decode("UTF-8"))
            else:
                log.error(error + json_data)
            return False
        return True

    @staticmethod
    def topic_to_regex(topic):
        return topic.replace("+", "[^/]+").replace("#", ".+")

    @staticmethod
    def regex_to_topic(regex):
        return regex.replace("[^/]+", "+").replace(".+", "#")

    # @staticmethod
    # def get_value(expression, body=None, value_type="string", get_tag=False, expression_instead_none=False):
    #     if isinstance(body, str):
    #         body = loads(body)
    #     if not expression:
    #         return ''
    #     positions = search(r'\${(?:(.*))}', expression)
    #     if positions is not None:
    #         p1 = positions.regs[-1][0]
    #         p2 = positions.regs[-1][1]
    #     else:
    #         p1 = 0
    #         p2 = len(expression)
    #     target_str = str(expression[p1:p2])
    #     if get_tag:
    #         return target_str
    #     full_value = None
    #     try:
    #         if isinstance(body, dict) and target_str.split()[0] in body:
    #             if value_type.lower() == "string":
    #                 full_value = expression[0: max(abs(p1 - 2), 0)] + body[target_str.split()[0]] + expression[
    #                                                                                                 p2 + 1:len(
    #                                                                                                     expression)]
    #             else:
    #                 full_value = body.get(target_str.split()[0])
    #         elif isinstance(body, (dict, list)):
    #             try:
    #                 jsonpath_expression = parse(target_str)
    #                 jsonpath_match = jsonpath_expression.find(body)
    #                 if jsonpath_match:
    #                     full_value = jsonpath_match[0].value
    #             except Exception as e:
    #                 log.debug(e)
    #         elif isinstance(body, (str, bytes)):
    #             search_result = search(expression, body)
    #             if search_result.groups():
    #                 full_value = search_result.group(0)
    #         if expression_instead_none and full_value is None:
    #             full_value = expression
    #     except Exception as e:
    #         log.exception(e)
    #     return full_value

    @staticmethod
    def install_package(package, version="upgrade"):
        from sys import executable
        from subprocess import check_call, CalledProcessError
        result = False
        if version.lower() == "upgrade":
            try:
                result = check_call([executable, "-m", "pip", "install", package, "--upgrade", "--user"])
            except CalledProcessError:
                result = check_call([executable, "-m", "pip", "install", package, "--upgrade"])
        else:
            from pkg_resources import get_distribution
            current_package_version = None
            try:
                current_package_version = get_distribution(package)
            except Exception:
                pass
            if current_package_version is None or current_package_version != version:
                installation_sign = "==" if ">=" not in version else ""
                try:
                    result = check_call(
                        [executable, "-m", "pip", "install", package + installation_sign + version, "--user"])
                except CalledProcessError:
                    result = check_call([executable, "-m", "pip", "install", package + installation_sign + version])
        return result
