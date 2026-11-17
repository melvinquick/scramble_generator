import secrets


class ScrambleGenerator:
    def __init__(self, puzzle_type="3x3"):
        self.puzzle_type = puzzle_type

    def generate_scramble(self, puzzle_type="3x3", num_moves=25):
        moves = self.get_valid_moves(puzzle_type)
        scramble_order = []

        for _ in range(num_moves):
            if not scramble_order:
                scramble_order.append(secrets.choice(moves))
            else:
                last_face = scramble_order[-1].strip()[0]
                filtered_moves = [m for m in moves if m.strip()[0] != last_face]
                scramble_order.append(secrets.choice(filtered_moves))

        return "".join(scramble_order)

    def get_valid_moves(self, puzzle_type):
        puzzle_type = puzzle_type.lower()

        if puzzle_type in ["pyraminx", "skewb"]:
            return self._get_face_turn_moves()

        try:
            size = int(puzzle_type.split("x")[0])
        except ValueError:
            size = 3

        return self._get_cube_moves(size)

    def _get_face_turn_moves(self):
        faces = ["U", "L", "R", "B"]
        moves = []
        for face in faces:
            moves.extend(
                [f"{face} ", f"{face}' ", f"{face.lower()} ", f"{face.lower()}' "]
            )
        return moves

    def _get_cube_moves(self, size):
        size = max(size, 2)

        faces = ["U", "D", "L", "R", "F", "B"]
        if size == 2:
            faces = ["U", "R", "F"]

        max_layers = (size - 1) // 2
        moves = []

        for face in faces:
            moves.extend([f"{face} ", f"{face}' "])
            for i in range(2, max_layers + 1):
                moves.extend([f"{face}{i} ", f"{face}{i}' "])

        return moves
