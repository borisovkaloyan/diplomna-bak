from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDataModel")


@_attrs_define
class UserDataModel:
    """
    Attributes:
        username (Union[Unset, str]):  Default: ''.
        email (Union[Unset, str]):  Default: ''.
        registration_plates (Union[Unset, List[str]]):
    """

    username: Union[Unset, str] = ""
    email: Union[Unset, str] = ""
    registration_plates: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        email = self.email

        registration_plates: Union[Unset, List[str]] = UNSET
        if not isinstance(self.registration_plates, Unset):
            registration_plates = self.registration_plates

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if email is not UNSET:
            field_dict["email"] = email
        if registration_plates is not UNSET:
            field_dict["registration_plates"] = registration_plates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username", UNSET)

        email = d.pop("email", UNSET)

        registration_plates = cast(List[str], d.pop("registration_plates", UNSET))

        user_data_model = cls(
            username=username,
            email=email,
            registration_plates=registration_plates,
        )

        user_data_model.additional_properties = d
        return user_data_model

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
