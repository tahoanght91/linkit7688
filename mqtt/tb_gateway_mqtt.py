import logging
import time
from json import dumps
from collections import OrderedDict

from mqtt.tb_device_mqtt import TBDeviceMqttClient
from tb_utility.tb_utility import TBUtility

GATEWAY_ATTRIBUTES_TOPIC = "v1/gateway/attributes"
GATEWAY_ATTRIBUTES_REQUEST_TOPIC = "v1/gateway/attributes/request"
GATEWAY_ATTRIBUTES_RESPONSE_TOPIC = "v1/gateway/attributes/response"
GATEWAY_MAIN_TOPIC = "v1/gateway/"
GATEWAY_RPC_TOPIC = "v1/gateway/rpc"
GATEWAY_RPC_RESPONSE_TOPIC = "v1/gateway/rpc/response"

log = logging.getLogger("App")


class TBGatewayAPI:
    pass


class TBGatewayMqttClient(TBDeviceMqttClient):
    def __init__(self, host, port, token=None, gateway=None, quality_of_service=1):
        TBDeviceMqttClient.__init__(self, host, port, token, quality_of_service)
        self.quality_of_service = quality_of_service
        self.__max_sub_id = 0
        self.__sub_dict = {}
        self.__connected_devices = set("*")
        self.devices_server_side_rpc_request_handler = None
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_subscribe = self._on_subscribe
        self._client._on_unsubscribe = self._on_unsubscribe
        self._gw_subscriptions = {}
        self.gateway = gateway
        self._attr_request_number = 0

    def _on_connect(self, client, userdata, flags, result_code, *extra_params):
        TBDeviceMqttClient._on_connect(self, client, userdata, flags, result_code, *extra_params)
        if result_code == 0:
            self._gw_subscriptions[
                int(self._client.subscribe(GATEWAY_ATTRIBUTES_TOPIC, qos=1)[1])] = GATEWAY_ATTRIBUTES_TOPIC
            self._gw_subscriptions[int(self._client.subscribe(GATEWAY_ATTRIBUTES_RESPONSE_TOPIC, qos=1)[
                                           1])] = GATEWAY_ATTRIBUTES_RESPONSE_TOPIC
            self._gw_subscriptions[int(self._client.subscribe(GATEWAY_RPC_TOPIC, qos=1)[1])] = GATEWAY_RPC_TOPIC
            # self._gw_subscriptions[int(self._client.subscribe(GATEWAY_RPC_RESPONSE_TOPIC)[1])] = GATEWAY_RPC_RESPONSE_TOPIC

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        subscription = self._gw_subscriptions.get(mid)
        if subscription is not None:
            if mid == 128:
                log.error("Service subscription to topic %s - failed.", subscription)
                del self._gw_subscriptions[mid]
            else:
                log.debug("Service subscription to topic %s - successfully completed.", subscription)
                del self._gw_subscriptions[mid]

    def _on_unsubscribe(self, *args):
        log.debug(args)

    def get_subscriptions_in_progress(self):
        return True if self._gw_subscriptions else False

    def _on_message(self, client, userdata, message):
        content = TBUtility.decode(message)
        TBDeviceMqttClient._on_decoded_message(self, content, message)
        self._on_decoded_message(content, message)

    def _on_decoded_message(self, content, message):
        if message.topic.startswith(GATEWAY_ATTRIBUTES_RESPONSE_TOPIC):
            with self._lock:
                req_id = content["id"]
                # pop callback and use it
                if self._attr_request_dict[req_id]:
                    if 'value' in content:
                        key = self._attr_key_request_dict.pop(0)
                    else:
                        key = ''
                    content['key'] = key
                    self._attr_request_dict.pop(req_id)(content, None)
                else:
                    log.error("Unable to find callback to process attributes response from TB")
        elif message.topic == GATEWAY_ATTRIBUTES_TOPIC:
            with self._lock:
                # callbacks for everything
                if self.__sub_dict.get("*|*"):
                    for callback in self.__sub_dict["*|*"]:
                        self.__sub_dict["*|*"][callback](content)
                # callbacks for device. in this case callback executes for all attributes in message
                target = content["device"] + "|*"
                if self.__sub_dict.get(target):
                    for callback in self.__sub_dict[target]:
                        self.__sub_dict[target][callback](content)
                # callback for atr. in this case callback executes for all attributes in message
                targets = [content["device"] + "|" + attribute for attribute in content["data"]]
                for target in targets:
                    if self.__sub_dict.get(target):
                        for sub_id in self.__sub_dict[target]:
                            self.__sub_dict[target][sub_id](content)
        elif message.topic == GATEWAY_RPC_TOPIC:
            if self.devices_server_side_rpc_request_handler:
                self.devices_server_side_rpc_request_handler(self, content)

    def __request_attributes(self, device, keys, callback, type_is_client=False):
        if not keys:
            log.error("There are no keys to request")
            return False
        ts_in_millis = int(round(time.time() * 1000))
        attr_request_number = self._add_attr_request_callback(callback)

        if len(keys) > 1:
            msg = OrderedDict([("id", attr_request_number), ("device", device), ("client", type_is_client), ("keys", keys)])
        elif len(keys) == 1:
            key = keys[0]
            self._attr_key_request_dict.update({self._attr_request_number: key})
            msg = OrderedDict([("id", attr_request_number), ("device", device), ("client", type_is_client), ("key", key)])

        info = self._client.publish(GATEWAY_ATTRIBUTES_REQUEST_TOPIC, dumps(msg), 1)
        self._add_timeout(attr_request_number, ts_in_millis + 30000)
        return info

    def gw_request_shared_attributes(self, device_name, keys, callback):
        return self.__request_attributes(device_name, keys, callback, False)

    def gw_request_client_attributes(self, device_name, keys, callback):
        return self.__request_attributes(device_name, keys, callback, True)

    def gw_send_attributes(self, device, attributes, quality_of_service=1):
        return self.publish_data({device: attributes}, GATEWAY_MAIN_TOPIC + "attributes", quality_of_service)

    def gw_send_telemetry(self, device, telemetry, quality_of_service=1):
        if not isinstance(telemetry, list) and not (isinstance(telemetry, dict) and telemetry.get("ts") is not None):
            telemetry = [telemetry]
        return self.publish_data({device: telemetry}, GATEWAY_MAIN_TOPIC + "telemetry", quality_of_service, )

    def gw_connect_device(self, device_name, device_type):
        info = self._client.publish(topic=GATEWAY_MAIN_TOPIC + "connect",
                                    payload=dumps({"device": device_name, "type": device_type}),
                                    qos=self.quality_of_service)
        self.__connected_devices.add(device_name)
        # if self.gateway:
        #     self.gateway.on_device_connected(device_name, self.__devices_server_side_rpc_request_handler)
        log.debug("Connected device %s", device_name)
        return info

    def gw_disconnect_device(self, device_name):
        info = self._client.publish(topic=GATEWAY_MAIN_TOPIC + "disconnect", payload=dumps({"device": device_name}),
                                    qos=self.quality_of_service)
        self.__connected_devices.remove(device_name)
        # if self.gateway:
        #     self.gateway.on_device_disconnected(self, device_name)
        log.debug("Disconnected device %s", device_name)
        return info

    def gw_subscribe_to_all_attributes(self, callback):
        return self.gw_subscribe_to_attribute("*", "*", callback)

    def gw_subscribe_to_all_device_attributes(self, device, callback):
        return self.gw_subscribe_to_attribute(device, "*", callback)

    def gw_subscribe_to_attribute(self, device, attribute, callback):
        if device not in self.__connected_devices:
            log.error("Device %s is not connected", device)
            return False
        with self._lock:
            self.__max_sub_id += 1
            key = device + "|" + attribute
            if key not in self.__sub_dict:
                self.__sub_dict.update({key: {self.__max_sub_id: callback}})
            else:
                self.__sub_dict[key].update({self.__max_sub_id: callback})
            log.info("Subscribed to %s with id %i", key, self.__max_sub_id)
            return self.__max_sub_id

    def gw_unsubscribe(self, subscription_id):
        with self._lock:
            for attribute in self.__sub_dict:
                if self.__sub_dict[attribute].get(subscription_id):
                    del self.__sub_dict[attribute][subscription_id]
                    log.info("Unsubscribed from %s, subscription id %i", attribute, subscription_id)
            if subscription_id == '*':
                self.__sub_dict = {}

    def gw_set_server_side_rpc_request_handler(self, handler):
        self.devices_server_side_rpc_request_handler = handler

    def gw_send_rpc_reply(self, device, req_id, resp, quality_of_service):
        if quality_of_service is None:
            quality_of_service = self.quality_of_service
        if quality_of_service not in (0, 1):
            log.error("Quality of service (qos) value must be 0 or 1")
            return None
        info = self._client.publish(GATEWAY_RPC_TOPIC,
                                    dumps({"device": device, "id": req_id, "data": resp}),
                                    qos=quality_of_service)
        return info
