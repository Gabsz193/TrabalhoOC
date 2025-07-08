; Get Digits
DATA R0, 0xff
OUT ADDR, R0
IN DATA, R0
IN DATA, R1
DATA R2, 0xD0
ADD R2, R0
ADD R2, R1
; End Get Digits

; Get full result in R0
CLF R2
OR R0, R2
SHL R0, R0
SHL R0, R0
SHL R0, R0
SHL R2, R2
ADD R2, R0
ADD R1, R0
; End Get full result in R0

; Guarda Dividendo
DATA R1, 0xff
ST R1, R0
; End Guarda Dividendo

; Pega Barra de Divisão
IN DATA, R1
; End Pega Barra de Divisão

; Pega divisor
IN DATA, R1
DATA R2, 0xD0
ADD R2, R1
; End Get Divisor in R1

; Guarda Divisor
DATA R2, 0xfe
ST R2, R1
; End Guarda Divisor

; Check if divisor is greater than dividendo
CMP R1, R0
JA .END_PROGRAM
; End Check if divisor is greater than dividendo

; Saving two complement's of divisor
DATA R2, 0x01
NOT R1, R1
ADD R2, R1
; End Saving two complement's of divisor

; R0 é o dividendo
; R1 é o divisor de complemento de 2
; 0xfd é o quociente

; Set quociente space
DATA R2, 0xfd
DATA R3, 0x00
ST R2, R3
; End Set quociente space


.LOOP_DIVISAO
ADD R1, R0 ; Diminui o dividendo pelo divisor

; Increment the quociente
DATA R2, 0xfd
LD R2, R3
DATA R2, 0x01
ADD R2, R3
DATA R2, 0xfd
ST R2, R3
; End Increment the quociente

; Get real divisor in R3
DATA R2, 0xfe
LD R2, R3
; End Get real divisor in R3
CMP R3, R0
JA .END_PROGRAM ; Check if divisor is greater than dividendo

JMP .LOOP_DIVISAO


.END_PROGRAM

DATA R2, 0xfd
LD R2, R3 ; Get Quociente
DATA R1, 10
CMP R3, R1 ; Vê se tem mais de um digito
JAE .DOIS_DIGITOS

DATA R1, 0xfe
OUT ADDR, R1
DATA R1, 0x30
ADD R1, R3
OUT DATA, R3
JMP .END_PROGRAM_END

.DOIS_DIGITOS
DATA R0, 0
; R0 - Contador das dezenas
; R3 - Quociente
.LOOP_DEZENAS
DATA R1, -10
ADD R1, R3
DATA R1, 1
ADD R1, R0
DATA R1, 10
CMP R1, R3
JA .END_LOOP_DEZENAS

JMP .LOOP_DEZENAS

.END_LOOP_DEZENAS

DATA R1, 0xfe
OUT ADDR, R1
DATA R1, 0x30
ADD R1, R0
OUT DATA, R0
ADD R1, R3
OUT DATA, R3

.END_PROGRAM_END
HALT