import secrets


class ScrambleGenerator:
    def __init__(self, puzzle_type="3x3"):
        self.puzzle_type = puzzle_type
        self.opposite_moves = {
            "U ": "U' ",
            "U' ": "U ",
            "u ": "u' ",
            "u' ": "u ",
            "U2 ": "U2' ",
            "U2' ": "U2 ",
            "U3 ": "U3' ",
            "U3' ": "U3 ",
            "U4 ": "U4' ",
            "U4' ": "U4 ",
            "U5 ": "U5' ",
            "U5' ": "U5 ",
            "D ": "D' ",
            "D' ": "D ",
            "D2 ": "D2' ",
            "D2' ": "D2 ",
            "D3 ": "D3' ",
            "D3' ": "D3 ",
            "D4 ": "D4' ",
            "D4' ": "D4 ",
            "D5 ": "D5' ",
            "D5' ": "D5 ",
            "L ": "L' ",
            "L' ": "L ",
            "l ": "l' ",
            "l' ": "l ",
            "L2 ": "L2' ",
            "L2' ": "L2 ",
            "L3 ": "L3' ",
            "L3' ": "L3 ",
            "L4 ": "L4' ",
            "L4' ": "L4 ",
            "L5 ": "L5' ",
            "L5' ": "L5 ",
            "R ": "R' ",
            "R' ": "R ",
            "r ": "r' ",
            "r' ": "r ",
            "R2 ": "R2' ",
            "R2' ": "R2 ",
            "R3 ": "R3' ",
            "R3' ": "R3 ",
            "R4 ": "R4' ",
            "R4' ": "R4 ",
            "R5 ": "R4' ",
            "R5' ": "R4 ",
            "F ": "F' ",
            "F' ": "F ",
            "F2 ": "F2' ",
            "F2' ": "F2 ",
            "F3 ": "F3' ",
            "F3' ": "F3 ",
            "F4 ": "F4' ",
            "F4' ": "F4 ",
            "F5 ": "F5' ",
            "F5' ": "F5 ",
            "B ": "B' ",
            "B' ": "B ",
            "b ": "b' ",
            "b' ": "b ",
            "B2 ": "B2' ",
            "B2' ": "B2 ",
            "B3 ": "B3' ",
            "B3' ": "B3 ",
            "B4 ": "B4' ",
            "B4' ": "B4 ",
            "B5 ": "B5' ",
            "B5' ": "B5 ",
        }

    def generate_scramble(self, puzzle_type="3x3", num_moves=25):
        puzzle_type = puzzle_type
        moves = self.get_valid_moves(puzzle_type)
        scramble_order = []
        counter = 0

        while counter < num_moves:
            if counter == 0:
                scramble_order.append(secrets.choice(moves))
            else:
                filtered_moves = [
                    move
                    for move in moves
                    if move != self.opposite_moves[scramble_order[-1]]
                ]
                scramble_order.append(secrets.choice(filtered_moves))

            counter += 1

        return "".join(map(str, scramble_order))

    def get_valid_moves(self, puzzle_type):
        match self.puzzle_type:
            case "2x2":
                return ["U ", "U' ", "R ", "R' ", "F ", "F' "]
            case "3x3":
                return [
                    "U ",
                    "U' ",
                    "D ",
                    "D' ",
                    "L ",
                    "L' ",
                    "R ",
                    "R' ",
                    "F ",
                    "F' ",
                    "B ",
                    "B' ",
                ]
            case "4x4":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                ]
            case "5x5":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                ]
            case "6x6":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "U3 ",
                    "U3' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "D3 ",
                    "D3' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "L3 ",
                    "L3' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "R3 ",
                    "R3' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "F3 ",
                    "F3' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                    "B3 ",
                    "B3' ",
                ]
            case "7x7":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "U3 ",
                    "U3' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "D3 ",
                    "D3' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "L3 ",
                    "L3' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "R3 ",
                    "R3' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "F3 ",
                    "F3' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                    "B3 ",
                    "B3' ",
                ]
            case "8x8":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "U3 ",
                    "U3' ",
                    "U4 ",
                    "U4' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "D3 ",
                    "D3' ",
                    "D4 ",
                    "D4' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "L3 ",
                    "L3' ",
                    "L4 ",
                    "L4' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "R3 ",
                    "R3' ",
                    "R4 ",
                    "R4' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "F3 ",
                    "F3' ",
                    "F4 ",
                    "F4' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                    "B3 ",
                    "B3' ",
                    "B4 ",
                    "B4' ",
                ]
            case "9x9":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "U3 ",
                    "U3' ",
                    "U4 ",
                    "U4' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "D3 ",
                    "D3' ",
                    "D4 ",
                    "D4' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "L3 ",
                    "L3' ",
                    "L4 ",
                    "L4' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "R3 ",
                    "R3' ",
                    "R4 ",
                    "R4' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "F3 ",
                    "F3' ",
                    "F4 ",
                    "F4' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                    "B3 ",
                    "B3' ",
                    "B4 ",
                    "B4' ",
                ]
            case "10x10":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "U3 ",
                    "U3' ",
                    "U4 ",
                    "U4' ",
                    "U5 ",
                    "U5' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "D3 ",
                    "D3' ",
                    "D4 ",
                    "D4' ",
                    "D5 ",
                    "D5' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "L3 ",
                    "L3' ",
                    "L4 ",
                    "L4' ",
                    "L5 ",
                    "L5' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "R3 ",
                    "R3' ",
                    "R4 ",
                    "R4' ",
                    "R5 ",
                    "R5' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "F3 ",
                    "F3' ",
                    "F4 ",
                    "F4' ",
                    "F5 ",
                    "F5' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                    "B3 ",
                    "B3' ",
                    "B4 ",
                    "B4' ",
                    "B5 ",
                    "B5' ",
                ]
            case "11x11":
                return [
                    "U ",
                    "U' ",
                    "U2 ",
                    "U2' ",
                    "U3 ",
                    "U3' ",
                    "U4 ",
                    "U4' ",
                    "U5 ",
                    "U5' ",
                    "D ",
                    "D' ",
                    "D2 ",
                    "D2' ",
                    "D3 ",
                    "D3' ",
                    "D4 ",
                    "D4' ",
                    "D5 ",
                    "D5' ",
                    "L ",
                    "L' ",
                    "L2 ",
                    "L2' ",
                    "L3 ",
                    "L3' ",
                    "L4 ",
                    "L4' ",
                    "L5 ",
                    "L5' ",
                    "R ",
                    "R' ",
                    "R2 ",
                    "R2' ",
                    "R3 ",
                    "R3' ",
                    "R4 ",
                    "R4' ",
                    "R5 ",
                    "R5' ",
                    "F ",
                    "F' ",
                    "F2 ",
                    "F2' ",
                    "F3 ",
                    "F3' ",
                    "F4 ",
                    "F4' ",
                    "F5 ",
                    "F5' ",
                    "B ",
                    "B' ",
                    "B2 ",
                    "B2' ",
                    "B3 ",
                    "B3' ",
                    "B4 ",
                    "B4' ",
                    "B5 ",
                    "B5' ",
                ]
            case "pyraminx":
                return [
                    "U ",
                    "U' ",
                    "u ",
                    "u' ",
                    "L ",
                    "L' ",
                    "l ",
                    "l' ",
                    "R ",
                    "R' ",
                    "r ",
                    "r' ",
                    "B ",
                    "B' ",
                    "b ",
                    "b' ",
                ]
            case "skewb":
                return [
                    "L ",
                    "L' ",
                    "R ",
                    "R' ",
                    "F ",
                    "F' ",
                    "B ",
                    "B' ",
                ]
