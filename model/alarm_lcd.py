class Alarm_lcd:
    _mccSmokeState = 0
    _mccFireState = 0
    _mccMoveState = 0
    _mccDoorState = 0
    _mccFloodState = 0
    _acmTempIndoor = 0

    @property
    def mccSmokeState(self):
        return self._mccSmokeState

    @mccSmokeState.setter
    def mccSmokeState(self, mccSmokeState):
        self._mccSmokeState = mccSmokeState

    @property
    def mccFireState(self):
        return self._mccFireState

    @mccFireState.setter
    def mccFireState(self, mccFireState):
        self._mccFireState = mccFireState

    @property
    def mccMoveState(self):
        return self._mccMoveState

    @mccMoveState.setter
    def mccMoveState(self, mccMoveState):
        self._mccMoveState = mccMoveState

    @property
    def mccDoorState(self):
        return self._mccDoorState

    @mccDoorState.setter
    def mccDoorState(self, mccDoorState):
        self._mccDoorState = mccDoorState

    @property
    def mccFloodState(self):
        return self._mccFloodState

    @mccFloodState.setter
    def mccFloodState(self, mccFloodState):
        self._mccFloodState = mccFloodState

    @property
    def acmTempIndoor(self):
        return self._acmTempIndoor

    @acmTempIndoor.setter
    def acmTempIndoor(self, acmTempIndoor):
        self._acmTempIndoor = acmTempIndoor
