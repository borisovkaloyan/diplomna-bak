from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.entry_data_model import EntryDataModel
from ...models.http_validation_error import HTTPValidationError
from ...models.registration_model import RegistrationModel
from ...types import Response


def _get_kwargs(
    *,
    body: RegistrationModel,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/entry/data",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, List["EntryDataModel"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EntryDataModel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, List["EntryDataModel"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegistrationModel,
) -> Response[Union[Any, HTTPValidationError, List["EntryDataModel"]]]:
    """Get Entry Data

     Gets entry data

    Args:
        registration (RegistrationModel): Input data

    Returns:
        list[EntryDataModel]: Entry data

    Args:
        body (RegistrationModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['EntryDataModel']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegistrationModel,
) -> Optional[Union[Any, HTTPValidationError, List["EntryDataModel"]]]:
    """Get Entry Data

     Gets entry data

    Args:
        registration (RegistrationModel): Input data

    Returns:
        list[EntryDataModel]: Entry data

    Args:
        body (RegistrationModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['EntryDataModel']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegistrationModel,
) -> Response[Union[Any, HTTPValidationError, List["EntryDataModel"]]]:
    """Get Entry Data

     Gets entry data

    Args:
        registration (RegistrationModel): Input data

    Returns:
        list[EntryDataModel]: Entry data

    Args:
        body (RegistrationModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['EntryDataModel']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RegistrationModel,
) -> Optional[Union[Any, HTTPValidationError, List["EntryDataModel"]]]:
    """Get Entry Data

     Gets entry data

    Args:
        registration (RegistrationModel): Input data

    Returns:
        list[EntryDataModel]: Entry data

    Args:
        body (RegistrationModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['EntryDataModel']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
