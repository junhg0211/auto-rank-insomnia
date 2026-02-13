from json import load, dump
from pyautogui import click, position, moveTo, dragTo
from math import inf
from time import sleep

RANKS = [
    "병1",
    "병2",
    "병3",
    "병4",
    "사1",
    "사2",
    "사3",
    "사4",
    "위1",
    "위2",
    "위3",
    "영1",
    "영2",
    "영3",
    "장1",
    "장2",
    "장3",
    "장4",
    "장5",
    "대1",
    "대2",
    "대3",
    "대4",
    "대5",
]

Board = dict["board" : list[str], "new":str, "wait":float]


def print_board(board: Board) -> bool:
    print("-" * 20)
    for i in range(7):
        for j in range(7):
            cell = board["board"][i * 7 + j]
            index = RANKS.index(cell) if cell in RANKS else -1
            print(format(index, "2d"), end=" ")
        print()


def is_board_full(board: Board) -> int:
    count = 0
    for cell in board["board"]:
        if cell == "":
            count += 1
    return count


def get_lowest_mergeable_positions(board: Board) -> tuple[int, int]:
    lowest_rank = inf
    lowest_points = (-1, -1)

    for i in range(49):
        for j in range(49):
            if (
                i != j
                and board["board"][i] != ""
                and board["board"][i] == board["board"][j]
            ):
                rank = RANKS.index(board["board"][i])
                if rank < lowest_rank:
                    lowest_rank = rank
                    lowest_points = (i, j)
    return lowest_points


def save_board(board: Board):
    with open("board.json", "w", encoding="utf-8") as f:
        dump(board, f, ensure_ascii=False, indent=2)


MOVE_DURATION = 0.15


def main():
    with open("board.json", "r", encoding="utf-8") as f:
        board = load(f)
    newing = board["max_news"]
    newing += MOVE_DURATION * board["max_news"] / board["wait"]

    lu = position() if input("LU") is not None else (0, 0)
    rd = position() if input("RD") is not None else (0, 0)
    new = position() if input("NEW") is not None else (0, 0)

    moveTo(new, _pause=False)
    click(_pause=False)
    sleep(MOVE_DURATION)

    while True:
        # merge
        pos1, pos2 = get_lowest_mergeable_positions(board)
        if pos1 == -1 or pos2 == -1:
            break

        x1 = lu[0] + (rd[0] - lu[0]) / 6 * (pos1 % 7)
        y1 = lu[1] + (rd[1] - lu[1]) / 6 * (pos1 // 7)
        x2 = lu[0] + (rd[0] - lu[0]) / 6 * (pos2 % 7)
        y2 = lu[1] + (rd[1] - lu[1]) / 6 * (pos2 // 7)

        moveTo(x1, y1, _pause=False)
        dragTo(x2, y2, button="left", duration=MOVE_DURATION, _pause=False)
        board["board"][pos1] = ""
        board["board"][pos2] = RANKS[RANKS.index(board["board"][pos2]) + 1]

        # new piece
        moveTo(new, _pause=False)
        click(_pause=False)
        board["board"][board["board"].index("")] = board["new"]

        # save board
        print_board(board)
        if newing > 0:
            newing -= 1
        else:
            try:
                sleep(board["wait"] - MOVE_DURATION)
            except KeyboardInterrupt:
                print("SAVING BOARD")
                save_board(board)
                break


if __name__ == "__main__":
    main()
