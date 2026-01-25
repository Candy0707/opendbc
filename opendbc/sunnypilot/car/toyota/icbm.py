"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""

from opendbc.car import structs
from opendbc.car.can_definitions import CanData
from opendbc.car.toyota import toyotacan
from opendbc.car.toyota.values import TSS2_CAR
from opendbc.sunnypilot.car.intelligent_cruise_button_management_interface_base import IntelligentCruiseButtonManagementInterfaceBase

ButtonType = structs.CarState.ButtonEvent.Type
SendButtonState = structs.IntelligentCruiseButtonManagement.SendButtonState


class IntelligentCruiseButtonManagementInterface(IntelligentCruiseButtonManagementInterfaceBase):
  def __init__(self, CP, CP_SP):
    super().__init__(CP, CP_SP)

  def update(self, CS, CC_SP, packer, frame) -> list[CanData]:
    can_sends = []
    self.CC_SP = CC_SP
    self.ICBM = CC_SP.intelligentCruiseButtonManagement
    self.frame = frame

    if self.ICBM.sendButton != SendButtonState.none:
      accel = self.ICBM.sendButton == SendButtonState.increase
      decel = self.ICBM.sendButton == SendButtonState.decrease

      if self.CP.carFingerprint in TSS2_CAR:
        can_sends.append(toyotacan.create_cruise_buttons(packer, CS.stock_clutch, accel=accel, decel=decel))

    return can_sends
