import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryDataModel")


@_attrs_define
class EntryDataModel:
    """
    Attributes:
        id (Union[Unset, int]):  Default: 0.
        entry_time (Union[Unset, datetime.datetime]):  Default: isoparse('2024-05-31T11:46:01.983995').
        exit_time (Union[Unset, datetime.datetime]):  Default: isoparse('2024-05-31T11:46:01.984004').
        is_paid (Union[Unset, bool]):  Default: False.
        registration_plate (Union[Unset, str]):  Default: ''.
    """

    id: Union[Unset, int] = 0
    entry_time: Union[Unset, datetime.datetime] = isoparse("2024-05-31T11:46:01.983995")
    exit_time: Union[Unset, datetime.datetime] = isoparse("2024-05-31T11:46:01.984004")
    is_paid: Union[Unset, bool] = False
    registration_plate: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        entry_time: Union[Unset, str] = UNSET
        if not isinstance(self.entry_time, Unset):
            entry_time = self.entry_time.isoformat()

        exit_time: Union[Unset, str] = UNSET
        if not isinstance(self.exit_time, Unset):
            exit_time = self.exit_time.isoformat()

        is_paid = self.is_paid

        registration_plate = self.registration_plate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if entry_time is not UNSET:
            field_dict["entry_time"] = entry_time
        if exit_time is not UNSET:
            field_dict["exit_time"] = exit_time
        if is_paid is not UNSET:
            field_dict["is_paid"] = is_paid
        if registration_plate is not UNSET:
            field_dict["registration_plate"] = registration_plate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _entry_time = d.pop("entry_time", UNSET)
        entry_time: Union[Unset, datetime.datetime]
        if isinstance(_entry_time, Unset):
            entry_time = UNSET
        else:
            entry_time = isoparse(_entry_time)

        _exit_time = d.pop("exit_time", UNSET)
        exit_time: Union[Unset, datetime.datetime]
        if isinstance(_exit_time, Unset):
            exit_time = UNSET
        else:
            exit_time = isoparse(_exit_time)

        is_paid = d.pop("is_paid", UNSET)

        registration_plate = d.pop("registration_plate", UNSET)

        entry_data_model = cls(
            id=id,
            entry_time=entry_time,
            exit_time=exit_time,
            is_paid=is_paid,
            registration_plate=registration_plate,
        )

        entry_data_model.additional_properties = d
        return entry_data_model

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
