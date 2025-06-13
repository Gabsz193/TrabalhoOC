import sys, re

def two_complement_bin(num, bit_width):
    return format(num % (1 << bit_width), f'0{bit_width}b')

class CommandMap:
    def __init__(self):
        two_params_command = r'^\s*(\w+)\s*(-?\w+)\s*,\s*(-?\w+)\s*(;.*)?$'
        one_param_command = r'^\s*(\w+)\s*(-?\w+)\s*(;.*)?$'
        no_param_command = r'^\s*(\w+)\s*(;.*)?$'

        self.commands: dict[str, tuple[int, int, str, int]] = {
            "LD": (0, 1, two_params_command, 2, 'reg', 'reg'),
            "ST": (1, 1, two_params_command, 2, 'reg', 'reg'),
            "DATA": (2, 2, two_params_command, 2, 'reg', 'num'),
            "JMPR": (3, 1, one_param_command, 1, 'reg', 'none'),
            "JMP": (4, 2, one_param_command, 1, 'num', 'none'),
            "J": (5, 2, one_param_command, 1, 'num', 'none'),
            "CLF": (6, 1, no_param_command, 0, 'none', 'none'),
            "IN": (7, 1, two_params_command, 2, 'type', 'reg'),
            "OUT": (7, 1, two_params_command, 2, 'type', 'reg'),
            "ADD": (8, 1, two_params_command, 2, 'reg', 'reg'),
            "SHR": (9, 1, two_params_command, 2, 'reg', 'reg'),
            "SHL": (10, 1, two_params_command, 2, 'reg', 'reg'),
            "NOT": (11, 1, two_params_command, 2, 'reg', 'reg'),
            "AND": (12, 1, two_params_command, 2, 'reg', 'reg'),
            "OR": (13, 1, two_params_command, 2, 'reg', 'reg'),
            "XOR": (14, 1, two_params_command, 2, 'reg', 'reg'),
            "CMP": (15, 1, two_params_command, 2, 'reg', 'reg'),
        }

    def reg_decode(self, reg: str) -> int:
        match reg.upper():
            case 'R0':
                return 0
            case 'R1':
                return 1
            case 'R2':
                return 2
            case 'R3':
                return 3
            case _:
                raise Exception("Invalid Register in compilation.")
    
    def param_decode(self, param : str, type: str):
        match type:
            case 'reg':
                return self.reg_decode(param)
            case 'num':
                if param.startswith("0x"):
                    return int(param, 16)
                elif param.startswith("0b"):
                    return int(param, 2)
                else:
                    return int(param)
            case 'none':
                return ''
            case 'type':
                match param.upper():
                    case 'DATA':
                        return 0
                    case 'ADDR':
                        return 1
                    case _:
                        raise Exception("Invalid Param in compilation")
            case _:
                raise Exception("Invalid Param Type in compilation")


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
    
    def command_qtd_params(self, command: str) -> str:
        if command.upper().startswith("J") and not command.upper().startswith("JMP"):
            return self.commands["J"][3]
        return self.commands[command.upper()][3]
    
    def command_type_params(self, command: str) -> tuple[str, str]:
        if command.upper().startswith("J") and not command.upper().startswith("JMP"):
            return self.commands["J"][4], self.commands["J"][5]
        return self.commands[command.upper()][4], self.commands[command.upper()][5]


class Montador:
    lines: list[str]
    memory: list[str]
    commands: list[tuple[str, str, str]]

    def __init__(self, input_path):
        self.commands = []
        self.lines = self.read_input(input_path)
        self.memory = ["00"] * 256

    def mount(self):
        command_map = CommandMap()

        memory_i = 0
        for op, param1, param2 in self.commands:
            print(op, param1, param2)
            code = command_map.command_code(op)
            op_binary = f'{code:04b}'
            qtd_bytes = command_map.command_size(op)
            qtd_params = command_map.command_qtd_params(op)
            param1_t, param2_t = command_map.command_type_params(op)

            ans = []

            if qtd_params == 0:
                ans.append(op_binary + '0000')
            elif qtd_params == 1:
                param1_num = command_map.param_decode(param1, param1_t)

                if qtd_bytes == 1:
                    ans.append(op_binary + '00' + two_complement_bin(param1_num, 2))
                elif qtd_bytes == 2:
                    j_ans = 0b0000

                    if code == 5:

                        has_C = True if op.find("C") != -1 else False
                        has_A = True if op.find("A") != -1 else False
                        has_E = True if op.find("E") != -1 else False
                        has_Z = True if op.find("Z") != -1 else False

                        if has_C:
                            j_ans |= 0b1000
                        if has_A:
                            j_ans |= 0b0100
                        if has_E:
                            j_ans |= 0b0010
                        if has_Z:
                            j_ans |= 0b0001
                    ans.append(op_binary + f'{j_ans:04b}')
                    ans.append(two_complement_bin(param1_num, 8))                    
                
            elif qtd_params == 2:
                param1_num = command_map.param_decode(param1, param1_t)
                param2_num = command_map.param_decode(param2, param2_t)

                if qtd_bytes == 1:
                    if op.upper() == "IN":
                        ans.append(op_binary + "0" + two_complement_bin(param1_num, 1) + two_complement_bin(param2_num, 2))
                    elif op.upper() == "OUT":
                        ans.append(op_binary + "1" + two_complement_bin(param1_num, 1) + two_complement_bin(param2_num, 2))
                    else:
                        ans.append(op_binary + two_complement_bin(param1_num, 2) + two_complement_bin(param2_num, 2))
                elif qtd_bytes == 2:
                    ans.append(op_binary + two_complement_bin(param1_num, 4))
                    ans.append(two_complement_bin(param2_num, 8))

            ans = list(map(lambda x: f'{int(x, 2):02x}', ans))

            for i in ans:
                self.memory[memory_i] = i
                memory_i += 1

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
    montador.show_memory()

    print(f"Arquivo de input: {input_file}")
    print(f"Arquivo de output: {output_file}")


if __name__ == "__main__":
    main()
