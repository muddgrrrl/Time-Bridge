#!/usr/bin/env python3
"""Convert an ISO timestamp between IANA time zones."""
import argparse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def localize(wall, zone, fold=None):
    candidates = {}
    for choice in (0, 1):
        candidate = wall.replace(tzinfo=zone, fold=choice)
        instant = candidate.astimezone(timezone.utc)
        if instant.astimezone(zone).replace(tzinfo=None) == wall:
            candidates[choice] = candidate
    if not candidates:
        raise ValueError("this local time does not exist because the clock jumps forward")
    offsets = {candidate.utcoffset() for candidate in candidates.values()}
    if len(offsets) > 1 and fold is None:
        raise ValueError("this time occurs twice; choose --fold 0 (first) or --fold 1 (second)")
    return candidates[fold or 0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("time", help="ISO date and time, for example 2026-11-23T14:30")
    parser.add_argument("zones", nargs="+", help="destination zones, for example America/Chicago Asia/Tokyo")
    parser.add_argument("--from", dest="source", help="source zone for a time without an offset")
    parser.add_argument("--fold", type=int, choices=(0, 1))
    args = parser.parse_args()
    try:
        if "T" not in args.time and " " not in args.time:
            raise ValueError("include a time as well as a date")
        instant = datetime.fromisoformat(args.time.removesuffix("Z") + "+00:00" if args.time.endswith("Z") else args.time)
        if instant.tzinfo is None:
            instant = localize(instant, ZoneInfo(args.source or "UTC"), args.fold)
        elif args.source is not None or args.fold is not None:
            raise ValueError("an offset timestamp already identifies an instant")
        results = []
        for name in args.zones:
            target = instant.astimezone(ZoneInfo(name))
            results.append(f"{name:<25} {target.isoformat(sep=' ')}  {target.tzname()}")
    except (ValueError, OverflowError, ZoneInfoNotFoundError) as error:
        parser.error(str(error))
    print("\n".join(results))


if __name__ == "__main__":
    main()
