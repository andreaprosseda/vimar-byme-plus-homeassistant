"""Knx Group Address Conversion."""

#  business logic taken from https://knxer.net/?p=49
import logging

_LOGGER = logging.getLogger(__name__)


#     HEX TO GROUP ADDRESS CONVERSION
#     a. 0x1073
#     b. remove 0x -> 1073
#     c. convert each digit in binary         ->      0001 0000 0111 0010
#     d. take main(H) middle(M) and sub(U)    ->      HHHH HMMM UUUU UUUU
#         H = 00010
#         M = 000
#         Y = 01110011
#     d. convert H, M, Y in decimal
#         H = 2
#         M = 0
#         Y = 115
#     e. merge 2/0/115


def get_knx_group_address(hex: str) -> str | None:
    """Hex to Group Address Conversion."""
    hex_value = _get_hex_value(hex)
    if not hex_value:
        return None

    result = _convert_digits_in_binary(hex_value)
    h = result[0:5]
    m = result[5:8]
    u = result[8:]

    address = (
        _from_binary_to_decimal(h)
        + "/"
        + _from_binary_to_decimal(m)
        + "/"
        + _from_binary_to_decimal(u)
    )
    if address == "0/0/0":
        # 0/0/0 is reserved
        return "1/0/0"

    _LOGGER.debug("Hex: %s - Knx: %s", hex_value, address)
    return address


# HEX TO PHYSICAL ADDRESS CONVERSION
# a. 0x1073
# b. remove 0x -> 1073
# c. convert each digit in binary         ->      0001 0000 0111 0010
# d. take main(A) middle(L) and sub(M)    ->      AAAA LLLL MMMM MMMM
#     A = 0010
#     L = 0000
#     M = 01110011
# d. convert A, L, M in decimal
#     A = 2
#     L = 0
#     M = 115
# e. merge 2/0/115


def get_knx_physical_address(hex: str) -> str | None:
    """Hex to Physical Address Conversion."""
    hex_value = _get_hex_value(hex)
    if not hex_value:
        return None

    result = _convert_digits_in_binary(hex_value)

    a_value = result[0:4]
    l_value = result[4:8]
    m_value = result[8:]

    return (
        _from_binary_to_decimal(a_value)
        + "."
        + _from_binary_to_decimal(l_value)
        + "."
        + _from_binary_to_decimal(m_value)
    )


def _convert_digits_in_binary(hex_value: str) -> str:
    digit_1 = hex_value[0:1]
    digit_1_binary = _from_hex_to_binary(digit_1)

    digit_2 = hex_value[1:2]
    digit_2_binary = _from_hex_to_binary(digit_2)

    digit_3 = hex_value[2:3]

    digit_3_binary = _from_hex_to_binary(digit_3)
    digit4 = hex_value[3:4]
    digit4_binary = _from_hex_to_binary(digit4)

    return digit_1_binary + digit_2_binary + digit_3_binary + digit4_binary


def _get_hex_value(hex: str) -> str | None:
    if not hex:
        return None
    return hex.replace("0x", "")


def _from_hex_to_binary(value: str) -> str:
    decimal_value = _from_hex_to_decimal(value)
    binary_value = _from_decimal_to_binary(decimal_value)
    return _fill_hex_with_zero(binary_value)


def _from_hex_to_decimal(value) -> str:
    return str(int(value, 16))


def _from_decimal_to_binary(value) -> str:
    return bin(int(value))[2:]


def _from_binary_to_decimal(value: str) -> str:
    return str(int(value, 2))


def _fill_hex_with_zero(binary_value) -> str:
    hex_length = 4
    padding = _repeat_zero(hex_length - len(binary_value))
    return padding + binary_value


def _repeat_zero(times: int) -> str:
    return "".join("0" for _ in range(times))


def _test():
    _assert_group_address("0x1073", "2/0/115")
    _assert_group_address("0x190F", "3/1/15")
    _assert_group_address("0x78FF", "15/0/255")
    _assert_group_address("0x0000", "1/0/0")
    _assert_group_address("0xFFFF", "31/7/255")
    _assert_group_address("0x0C81", "1/4/129")

    _assert_physical_address("0x1073", "1.0.115")
    _assert_physical_address("0x190F", "1.9.15")
    _assert_physical_address("0x78FF", "7.8.255")
    _assert_physical_address("0x0000", "0.0.0")
    _assert_physical_address("0xFFFF", "15.15.255")
    _assert_physical_address("0x0C81", "0.12.129")


def _assert_group_address(input: str, expected: str) -> None:
    address = get_knx_group_address(input)
    result = address is not None and address == expected
    print(  # noqa: T201
        "GROUP ADDRESS:\t\t["
        + str(result)
        + "]"
        + "\t\tINPUT: "
        + input
        + "\t\tACTUAL: "
        + address
        + "   \t\tEXPECTED: "
        + expected
    )


def _assert_physical_address(input: str, expected: str) -> None:
    address = get_knx_physical_address(input)
    result = address is not None and address == expected
    print(  # noqa: T201
        "PHYSICAL ADDRESS:\t["
        + str(result)
        + "]"
        + "\t\tINPUT: "
        + input
        + "\t\tACTUAL: "
        + address
        + "   \t\tEXPECTED: "
        + expected
    )


# _test()
