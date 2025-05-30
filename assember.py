variables = {}

def decode_command(command : str, i) -> str | None:

    if command.startswith(".") or len(command.split(" = ")) > 1:
        # variables[command] = i
        return None

    def switch_reg(reg : str) -> str:
        if reg == "R0":
            return "00"
        elif reg == "R1":
            return "01"
        elif reg == "R2":
            return "10"
        elif reg == "R3":
            return "11"
        else:
            raise Exception("Registrador Inválido")


    subcommands = command.split(" ")
    command_name = subcommands[0]
    arg1 = ""
    arg2 = ""
    if len(subcommands) > 1:
        arg1 = subcommands[1]
        if len(subcommands) > 2:
            arg2 = subcommands[2]
            
    # if command_name == "JMP":
    #     print(subcommands)
    #     print(command, arg1, arg2)

    if command_name == "ADD":
        return f"1000{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "SHR":
        return f"1001{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "SHL":
        return f"1010{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "NOT":
        return f"1011{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "AND":
        return f"1100{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "OR":
        return f"1101{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "XOR":
        return f"1110{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "CMP":
        return f"1111{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "LD":
        return f"0000{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "ST":
        return f"0001{switch_reg(arg1)}{switch_reg(arg2)}"
    elif command_name == "DATA":
        if variables.get(arg2) != None:
            return f"001000{switch_reg(arg1)}\n{format(int(variables[arg2]), '08b')}"
        return f"001000{switch_reg(arg1)}\n{format(int(arg2), '08b')}"
    elif command_name == "JMPR":
        return f"001100{switch_reg(arg1)}"
    elif command_name == "JMP":
        if variables.get(arg1) != None:
            return f"01000000\n{format(int(variables[arg1]), '08b')}" 
        return f"01000000\n{format(int(arg1), '08b')}"
    elif command_name == "JCAEZ":
        if variables.get(arg2):
            return f"0101{arg1}\n{format(int(variables[arg2]), '08b')}"
        return f"0101{arg1}\n{format(int(arg2), '08b')}"
    elif command_name == "CLF":
        return "01100000"
    elif command_name == "IN":
        a = "0"
        if arg1 == "ADDR":
            a = "1"
        elif arg1 != "DATA":
            raise SyntaxError("Comando inválido: ADDR ou DATA")
        return f"01110{a}{switch_reg(arg2)}"
    elif command_name == "OUT":
        a = "0"
        if arg1 == "ADDR":
            a = "1"
        elif arg1 != "DATA":
            raise SyntaxError("Comando inválido: ADDR ou DATA")
        return f"01111{a}{switch_reg(arg2)}"
    else:
        raise SyntaxError("Comando inválido")

with open("program.pc", 'r', encoding='UTF-8') as file:
    content = file.read()
    lines = content.split("\n")
    full_command = []
    index = 0
    
    for line in lines:
        if(line):
            print(line)
            
            if(line.startswith(".")):
                print(f"Definiu variável {line} = {index}")
                variables[line] = index
                
            elif(len(line.split(" = ")) > 1):
                (name, value) = line.split(" = ")
                variables[name] = int(value)
                
            else:
                try:
                    a = decode_command(line, index).split("\n")
                except:
                    a = [1,1]
                finally:
                    if(len(a) == 1):
                        index += 1
                    else:
                        index += 2
    
    index = 0
    
    for line in lines:
        if(line):
            converted_text = decode_command(line, index)

            if converted_text == None:
                continue

            a = converted_text.split("\n")

            if(len(a) == 1):
                full_command.append(int(a[0], 2))
                index += 1
            else:
                full_command.append(int(a[0], 2))
                full_command.append(int(a[1], 2))
                index += 2

    exit_file = open("content_rom.o", "wb")
    for i in full_command:
        exit_file.write(i.to_bytes(1, byteorder='big'))