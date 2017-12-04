#!/usr/bin/env python3
"""Generate A3! team combinations."""
import argparse
import itertools
import sys
from typing import (Iterable, Tuple, Dict, Set)


MEMBERS = {
    "咲也", "真澄", "綴", "至", "シトロン",
    "天馬", "幸", "椋", "三角", "一成",
    "万里", "十座", "太一", "臣", "左京",
    "紬", "丞", "密", "誉", "東"
}  # type: Set[str]
BONUS_COMBINATIONS = (
    (("co", 50), ("天馬", "幸", "椋", "三角", "一成")),
    (("co", 40), ("椋", "十座", "密", "東")),

    (("co", 30), ("咲也", "真澄", "丞")),
    (("co", 30), ("シトロン", "三角", "誉")),
    (("co", 30), ("幸", "椋", "誉")),
    (("co", 30), ("椋", "一成", "左京")),
    (("co", 30), ("三角", "紬", "東")),

    (("co", 10), ("綴", "シトロン")),
    (("co", 10), ("綴", "誉")),
    (("co", 10), ("至", "誉")),
    (("co", 10), ("天馬", "万里")),
    (("co", 10), ("幸", "臣")),
    (("co", 10), ("一成", "太一")),
    (("co", 10), ("一成", "誉")),


    (("ac", 50), ("万里", "十座", "太一", "臣", "左京")),
    (("ac", 40), ("咲也", "天馬", "万里", "紬")),

    (("ac", 30), ("綴", "臣", "丞")),
    (("ac", 30), ("シトロン", "幸", "丞")),
    (("ac", 30), ("天馬", "十座", "太一")),
    (("ac", 30), ("椋", "三角", "密")),

    (("ac", 10), ("咲也", "十座")),
    (("ac", 10), ("真澄", "天馬")),
    (("ac", 10), ("真澄", "幸")),
    (("ac", 10), ("至", "万里")),
    (("ac", 10), ("至", "太一")),
    (("ac", 10), ("一成", "東")),
    (("ac", 10), ("紬", "丞")),
    (("ac", 10), ("密", "誉")),


    (("sr", 50), ("咲也", "真澄", "綴", "至", "シトロン")),
    (("sr", 50), ("紬", "丞", "密", "誉", "東")),
    (("sr", 40), ("シトロン", "一成", "左京", "東")),

    (("sr", 30), ("咲也", "真澄", "万里")),
    (("sr", 30), ("咲也", "密", "東")),
    (("sr", 30), ("三角", "左京", "東")),

    (("sr", 10), ("真澄", "密")),
    (("sr", 10), ("綴", "臣")),
    (("sr", 10), ("至", "紬")),
    (("sr", 10), ("天馬", "幸")),
    (("sr", 10), ("椋", "十座")),
    (("sr", 10), ("太一", "丞")),
    (("sr", 10), ("臣", "左京"))
)  # type: Tuple[Tuple[Tuple[str, int], Tuple[str, ...]], ...]


def main() -> None:
    check_members, number, specified = init()

    for team in gen_teams(check_members, number):
        allteam = team + specified
        bonus = check_bonus(allteam)
        print("{team}: {bonus}"
              .format(team=str(allteam),
                      bonus=str(bonus)))


def gen_teams(members: Iterable[str], num: int=5) -> Iterable[Tuple[str, ...]]:
    return itertools.combinations(members, num)


def has_bonus(team: Iterable[str], bonusmem: Iterable[str]) -> bool:
    for member in bonusmem:
        if member not in team:
            return False
    return True


def check_bonus(team: Iterable[str]) -> Dict[str, int]:
    bonuses = {"co": 0, "ac": 0, "sr": 0}
    for bonus in BONUS_COMBINATIONS:
        bonusdetails, bonusmembers = bonus
        if has_bonus(team, bonusmembers):
            genre, point = bonusdetails
            bonuses[genre] += point
    return bonuses


def parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument(
        "-m", "--members",
        metavar="member",
        nargs="+",
        help="specify members")
    parser.add_argument(
        "-g", "--guest",
        help="include guest",
        action="store_true")
    return parser.parse_args()


def init() -> Tuple[Iterable[str], int, Tuple[str, ...]]:
    number = 5
    args = parse_arg()
    if args.guest:
        if args.members and len(args.members) > 6:
            sys.exit("Too many members")
        number += 1
    else:
        if args.members and len(args.members) > 5:
            sys.exit("Too many members")

    if not args.members:
        return (MEMBERS, number, ())

    specified = set(args.members)
    number -= len(specified)
    check_members = MEMBERS - specified

    for argmember in args.members:
        if argmember not in MEMBERS:
            sys.exit("Invalid member: {}".format(argmember))

    return (check_members, number, tuple(specified))


if __name__ == "__main__":
    main()
