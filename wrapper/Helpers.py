import socket

def expand_ranges(range_str):
    numbers = []
    for part in range_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(part))
    return numbers

def collapse_ranges(numbers):
    if not numbers:
        return ""
    numbers = sorted(numbers)
    ranges = []
    start = numbers [0]
    end = start
    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            ranges.append(f"{start}-{end}" if start != end else str(start))
            start = end = num
    ranges.append(f"{start}-{end}" if start != end else str(start))
    return ",".join(ranges)

# This should be multivendor
# But I don't have access to other vendors so will be populated when I encounter issue
_theremightbemore = {
    "Gi": "GigabitEthernet",
    "Fa": "FastEthernet",
    "Te": "TenGigabitEthernet",
    "Vl": "Vlan",
    "Po": "Port-channel"
}

def convertShortIntName(shouldBeShort: str) -> str:
    for key, value in _theremightbemore.items():
        if(key in shouldBeShort and value not in shouldBeShort):
            return shouldBeShort.replace(key, value)
    return shouldBeShort

_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
def isStringIpAddress(string: str) -> bool:
    try:
        socket.inet_aton(string)
        return True
    except Exception:
        return False