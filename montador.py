import sys, re

from typing_extensions import Match


class CommandMap:
    def __init__(self):
        two_params_command = r'^\s*(\w+)\s*(-?\w+)\s*,\s*(-?\w+)\s*(;.*)?$'
        one_param_command = r'^\s*(\w+)\s*(-?\w+)\s*(;.*)?$'
        no_param_command = r'^\s*(\w+)\s*(;.*)?$'

        self.commands: dict[str, tuple[int, int, str]] = {
            "LD": (0, 1, two_params_command),
            "ST": (1, 1, two_params_command),
            "DATA": (2, 2, two_params_command),
            "JMPR": (3, 1, one_param_command),
            "JMP": (4, 2, one_param_command),
            "J": (5, 2, one_param_command),
            "CLF": (6, 1, no_param_command),
            "IN": (7, 1, two_params_command),
            "OUT": (8, 1, two_params_command),
            "ADD": (9, 1, two_params_command),
            "SHR": (10, 1, two_params_command),
            "SHL": (11, 1, two_params_command),
            "NOT": (12, 1, two_params_command),
            "AND": (13, 1, two_params_command),
            "OR": (14, 1, two_params_command),
            "XOR": (15, 1, two_params_command),
            "CMP": (16, 1, two_params_command),
        }

    def command_code(self, command: str) -> int:
        if command.upper().startswith("J") and not command.upper().startswith("JMP"):
            return self.commands["J"][0]

        return self.commands[command.upper()][0]

    def command_size(self, command: str) -> int:
        if command.upper().startswith("J") and not command.upper().startswith("JMP"):
            return self.commands["J"][1]
        return self.commands[command.upper()][1]

    def command_match(self, command: str) -> str:
        if command.upper().startswith("J") and not command.upper().startswith("JMP"):
            return self.commands["J"][2]
        return self.commands[command.upper()][2]


class Montador:
    lines: list[str]
    memory: list[str]
    commands: list[tuple[str, str, str]]

    def __init__(self, input_path):
        self.commands = []
        self.lines = self.read_input(input_path)
        self.memory = ["00"] * 256

    def mount(self):
        commands = CommandMap()
        print(self.commands)

        pass

    def show_memory(self, cols=8):
        for offset in range(0, len(self.memory), cols):
            print(f"{offset:03}-{offset + cols - 1:03}:", end=" ")
            for i in range(cols):
                print(f"0x{self.memory[offset + i]}", end=" ") if offset + i < len(self.memory) else print("   ",
                                                                                                           end=" ")
            print("\n")

    def check_syntax(self, line_number: int, line: str) -> tuple[str, str, str] | None:
        line_number += 1
        commands = CommandMap()
        check_code = r'^\s*(\w+|;)'
        command = re.search(check_code, line).group().strip()

        if command == ';': return None

        try:
            command_check = commands.command_match(command)
        except KeyError:
            raise Exception(f"Invalid command {line_number}: {line}")

        command_match = re.match(command_check, line)

        if command_match is None:
            raise Exception(f"Bad syntax {line_number}: {line}")

        command_groups = command_match.groups()

        match len(command_groups):
            case 2:
                commands = (command_groups[0].upper(), '', '')
            case 3:
                commands = (command_groups[0].upper(), command_groups[1], '')
            case 4:
                commands = (command_groups[0].upper(), command_groups[1], command_groups[2])
            case _:
                raise Exception(f"Not a valid error ??? {line_number}: {line}")

        return commands

    def read_input(self, input_path: str) -> list[str]:
        has_error = False

        with open(input_path, "r") as f:
            lines = f.read().splitlines()
            for i, line in enumerate(lines):
                if line == '': continue
                try:
                    command = self.check_syntax(i, line)

                    if command is not None:
                        self.commands.append(command)
                except Exception as e:
                    has_error = True
                    print(f"{e}")

        if has_error:
            sys.exit(1)

        return lines


def main():
    # Certifique-se de que dois argumentos foram fornecidos
    if len(sys.argv) != 3:
        print("Uso: python script.py <arquivo_de_input> <arquivo_de_output>")
        sys.exit(1)

    # Pegue os argumentos da linha de comando
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    montador = Montador(input_file)

    montador.mount()

    print(f"Arquivo de input: {input_file}")
    print(f"Arquivo de output: {output_file}")


if __name__ == "__main__":
    main()
