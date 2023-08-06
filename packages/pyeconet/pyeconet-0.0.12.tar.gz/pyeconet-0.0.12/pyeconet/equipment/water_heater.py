import logging
import json
import time

from ..vacation import EcoNetVacation

_LOGGER = logging.getLogger(__name__)


class EcoNetWaterHeater(object):
    """
    Represents an EcoNet water heater.
    This is a combination of five API endpoints.
    /locations/
    /equipment/{ID}
    /equipment/{ID}/modes
    /equipment/{ID}/usage
    /vacations/
    """

    def __init__(self, device_as_json, device_modes_as_json, device_usage_json, location_id, vacations, api_interface):
        self.api_interface = api_interface
        self.json_state = device_as_json
        self._usage = device_usage_json
        self._modes = []
        self.location_id = location_id
        self.vacations = vacations
        self._last_update = time.time()
        for mode in device_modes_as_json:
            self._modes.append(mode.get("name"))

    @property
    def name(self):
        return self.json_state.get('name')

    @property
    def id(self):
        return self.json_state.get('id')

    @property
    def set_point(self):
        return self.json_state.get("setPoint")

    @property
    def min_set_point(self):
        return self.json_state.get("minSetPoint")

    @property
    def max_set_point(self):
        return self.json_state.get("maxSetPoint")

    @property
    def is_on_vacation(self):
        return self.json_state.get("isOnVacation")

    @property
    def is_connected(self):
        return self.json_state.get("isConnected")

    @property
    def is_enabled(self):
        return self.json_state.get("isEnabled")

    @property
    def in_use(self):
        return self.json_state.get("inUse")

    @property
    def mode(self):
        return self.json_state.get("mode")
    
    @property
    def upper_temp(self):
        return self.json_state.get('upperTemp')

    @property
    def lower_temp(self):
        return self.json_state.get('lowerTemp')

    @property
    def ambient_temp(self):
        return self.json_state.get('ambientTemp')

    @property
    def supported_modes(self):
        return self._modes

    @property
    def usage_unit(self):
        if self._usage and self._usage.get('energyUsage'):
            return self._usage['energyUsage'].get('unit')

    @property
    def total_usage_for_today(self):
        if self._usage and self._usage.get('energyUsage'):
            hours = self._usage['energyUsage'].get('hours', {})
            return sum((usage for usage in hours.values()))

    @property
    def total_usage_for_month(self):
        if self._usage and self._usage.get('energyUsage'):
            days = self._usage['energyUsage'].get('days', {})
            return sum((usage for usage in days.values()))

    @property
    def total_usage_for_year(self):
        if self._usage and self._usage.get('energyUsage'):
            months = self._usage['energyUsage'].get('months', {})
            return sum((usage for usage in months.values()))

    @property
    def waterusage_unit(self):
        if self._usage and self._usage.get('waterUsage'):
            return self._usage['waterUsage'].get('unit')

    @property
    def total_water_for_today(self):
        if self._usage and self._usage.get('waterUsage'):
            hours = self._usage['waterUsage'].get('hours', {})
            return sum((usage for usage in hours.values()))

    @property
    def total_water_for_month(self):
        if self._usage and self._usage.get('waterUsage'):
            days = self._usage['waterUsage'].get('days', {})
            return sum((usage for usage in days.values()))

    @property
    def total_water_for_year(self):
        if self._usage and self._usage.get('waterUsage'):
            months = self._usage['waterUsage'].get('months', {})
            return sum((usage for usage in months.values()))

    def get_vacations(self):
        return self.vacations

    def dump_usage_json(self):
        if self._usage:
            return json.dumps(self._usage, indent=4, sort_keys=True)

    def update_state(self):
        now = time.time()
        # Only call the API once to obtain all devices
        if now - self._last_update > 300:
            _LOGGER.info("Calling API to get updated state.")
            device_state = self.api_interface.get_device(self.id)
            if device_state:
                _LOGGER.debug(device_state)
                self.json_state = device_state
            usage = self.api_interface.get_usage(self.id)
            if usage:
                _LOGGER.debug(usage)
                self._usage = usage
            vacations = self.api_interface.get_vacations()
            if vacations:
                self.vacations = []
                for vacation in vacations:
                    for equipment in vacation.get("participatingEquipment"):
                        if equipment.get("id") == self.id:
                            self.vacations.append(EcoNetVacation(vacation, self.api_interface))
            self._last_update = now

    def set_target_set_point(self, temp):
        if self.min_set_point <= temp <= self.max_set_point:
            self.api_interface.set_state(self.id, {"setPoint": temp})
            self._last_update = 0
        else:
            error = "Invalid set point. Must be <= {} and => {}".format(self.max_set_point, self.min_set_point)
            _LOGGER.error(error)

    def set_vacation_mode(self, start_date, end_date):
        _location_id = self.location_id
        _id = self.id

        start_date_string = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_date_string = end_date.strftime("%Y-%m-%dT%H:%M:%S")

        body = {"startDate": start_date_string, "endDate": end_date_string,
                "location": { "id": _location_id },
                "participatingEquipment": [{"id": _id}]}
        self.api_interface.create_vacation(body)
        self._last_update = 0

    def set_mode(self, mode):
        if mode in self._modes:
            self.api_interface.set_state(self.id, {"mode": mode})
            self._last_update = 0
        else:
            _LOGGER.error("Invalid mode: " + str(mode))
