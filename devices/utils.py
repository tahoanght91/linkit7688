from config import *


def _read_attribute(key, value):
    if client_attributes.get(key) != value:
        client_attributes[key] = value
        update_attributes_lock.acquire()
        update_attributes[key] = value
        update_attributes_lock.release()


def _read_telemetry(key, value):
    telemetries_lock.acquire()
    telemetries[key] = value
    telemetries_lock.release()


def read_services(key, value):
    services_lock.acquire()
    services[key] = value
    services_lock.release()

