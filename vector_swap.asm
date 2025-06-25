; Colocando 7 números nos últimos endereços
DATA R0, 1
DATA R1, 0xff
ST R1, R0

DATA R0, 2
DATA R1, 0xfe
ST R1, R0

DATA R0, 3
DATA R1, 0xfd
ST R1, R0

DATA R0, 4
DATA R1, 0xfc
ST R1, R0

DATA R0, 5
DATA R1, 0xfb
ST R1, R0

DATA R0, 6
DATA R1, 0xfa
ST R1, R0

DATA R0, 7
DATA R1, 0xf9
ST R1, R0

; Pegar cada número no endereço i e fazer swap com o n - i
DATA R0, 0xf9
DATA R2, 0xf9
DATA R1, 0xff
DATA R3, 0xff
LD R0, R0
LD R1, R1
ST R3, R0
ST R2, R1

DATA R0, 0xfa
DATA R2, 0xfa
DATA R1, 0xfe
DATA R3, 0xfe
LD R0, R0
LD R1, R1
ST R3, R0
ST R2, R1

DATA R0, 0xfb
DATA R2, 0xfb
DATA R1, 0xfd
DATA R3, 0xfd
LD R0, R0
LD R1, R1
ST R3, R0
ST R2, R1

JMP 71 ; halt


