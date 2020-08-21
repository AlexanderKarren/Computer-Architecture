"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.stack_pointer = len(self.ram) - 1
        self.running = True
        self.equal_flag = False
        self.less_than_flag = False
        self.greater_than_flag = False
        self.op_codes = {
            # NOP
            0: lambda a, b: print("NOP"),
            # HLT
            1: self.hlt,
            # RET
            17: self.ret,
            # PUSH
            69: self.push,
            # POP
            70: self.pop,
            # PRN
            71: lambda a, b: print(self.ram_read(a)),
            # CALL
            80: self.call,
            # JMP
            84: self.jmp,
            # JEQ
            85: self.jeq,
            # JNE
            86: self.jne,
            # NOT
            87: self.alu_not,
            # LDI
            130: lambda a, b: self.ram_write(a, b),
            # ADD
            160: self.alu_add,
            # MULT
            162: self.alu_mult,
            # MOD
            164: self.alu_mod,
            # CMP
            167: self.alu_cmp,
            # AND
            168: self.alu_and,
            # OR
            170: self.alu_or,
            # XOR
            171: self.alu_xor,
            # SHL
            172: self.alu_shl,
            # SHR
            173: self.alu_shr
        }

    def hlt(self, reg_a, reg_b):
        self.running = False

    def ret(self, reg_a, reg_b):
        address = self.ram[self.stack_pointer]
        self.stack_pointer += 1
        self.pc = address

    def push(self, reg_a, reg_b):
        self.stack_pointer -= 1
        value = self.reg[reg_a]
        self.ram[self.stack_pointer] = value

    def pop(self, reg_a, reg_b):
        value = self.ram[self.stack_pointer]
        self.stack_pointer += 1
        self.reg[reg_a] = value

    def call(self, reg_a, reg_b):
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = self.pc + 1
        self.pc = self.reg[reg_a] - 2
        # continue
    
    def jmp(self, reg_a, reg_b):
        self.pc = self.reg[reg_a] - 2
        # continue

    def jeq(self, reg_a, reg_b):
        if self.equal_flag is True:
            # print("jeq: jumping to", self.reg[reg_a], "op_code:", self.ram[self.reg[reg_a]])
            self.pc = self.reg[reg_a] - 2
            # continue
        # else:
        #     print("jeq: flag not true, not jumping")

    def jne(self, reg_a, reg_b):
        if self.equal_flag is False:
            # print("jne: jumping to", self.reg[reg_a], "op_code:", self.ram[self.reg[reg_a]])
            self.pc = self.reg[reg_a] - 2
            # continue
        # else:
        #     print("jne: flag not false, not jumping")

    def alu_not(self, reg_a, reg_b):
        self.reg[reg_a] = ~self.reg[reg_a]

    def alu_add(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]

    def alu_mult(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]

    def alu_mod(self, reg_a, reg_b):
        self.reg[reg_a] %= self.reg[reg_b]

    def alu_cmp(self, reg_a, reg_b):
        if self.reg[reg_a] == self.reg[reg_b]:
                self.equal_flag = True
        else:
            self.equal_flag = False
        if self.reg[reg_a] < self.reg[reg_b]:
            self.less_than_flag = True
        else:
            self.less_than_flag = False
        if self.reg[reg_a] > self.reg[reg_b]:
            self.greater_than_flag = True
        else:
            self.greater_than_flag = False

    def alu_and(self, reg_a, reg_b):
        self.reg[reg_a] &= self.reg[reg_b]

    def alu_or(self, reg_a, reg_b):
        self.reg[reg_a] |= self.reg[reg_b]

    def alu_xor(self, reg_a, reg_b):
        self.reg[reg_a] ^= self.reg[reg_b]

    def alu_shl(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]

    def alu_shr(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        if len(sys.argv) > 1:
            try:
                file = open(sys.argv[1], 'r')
            except FileNotFoundError:
                print(f"{sys.argv[1]} not found in local directory")
                sys.exit(1)
            program = []
            for instruction in file.read().split('\n'):
                trimmed_instruction = ""
                if len(instruction) >= 8:
                    for i in range(8):
                        if instruction[i] == '0' or instruction[i] == '1':
                            trimmed_instruction += instruction[i]
                instruction = trimmed_instruction
                if len(instruction) == 8:
                    # print(instruction)
                    program.append(int(instruction, 2))
            # print(program)
            file.close()
        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def ram_read(self, address):
        return self.reg[address]


    def ram_write(self, address, value):
        self.reg[address] = value


    # def alu_if_else(self, op, reg_a, reg_b):
    #     """ALU operations."""
    #     # NOT
    #     if op == 105:
    #         self.reg[reg_a] = ~self.reg[reg_a]
    #     # LDI
    #     elif op == 130:
    #         self.ram_write(reg_a, reg_b)
    #     # ADD
    #     elif op == 160:
    #         self.reg[reg_a] += self.reg[reg_b]
    #     # MUL
    #     elif op == 162:
    #         self.reg[reg_a] *= self.reg[reg_b]
    #     # MOD
    #     elif op == 164:
    #         self.reg[reg_a] %= self.reg[reg_b]
    #     # CMP
    #     elif op == 167:
    #         if self.reg[reg_a] == self.reg[reg_b]:
    #             self.equal_flag = True
    #         else:
    #             self.equal_flag = False
    #         if self.reg[reg_a] < self.reg[reg_b]:
    #             self.less_than_flag = True
    #         else:
    #             self.less_than_flag = False
    #         if self.reg[reg_a] > self.reg[reg_b]:
    #             self.greater_than_flag = True
    #         else:
    #             self.greater_than_flag = False
    #     # AND
    #     elif op == 168:
    #         self.reg[reg_a] &= self.reg[reg_b]
    #     # OR
    #     elif op == 170:
    #         self.reg[reg_a] |= self.reg[reg_b]
    #     # XOR
    #     elif op == 171:
    #         self.reg[reg_a] ^= self.reg[reg_b]
    #     # SHL
    #     elif op == 172:
    #         self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
    #     # SHR
    #     elif op == 173:
    #         self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
    #     else:
    #         raise Exception("Unsupported ALU operation:", op)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if self.op_codes.get(op):
            self.op_codes.get(op)(reg_a, reg_b)
        else:
            raise Exception("Unsupported ALU operation:", op)

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # def run_if_else(self):
    #     """Run the CPU."""
    #     op_size = 0
    #     ir = [0] * 256
    #     for i in range(len(self.ram)):
    #         ir[i] = self.ram[i]

    #     # print(ir)

    #     while self.running:
    #         # print(self.pc, "running op_code", ir[self.pc])
    #         # print(self.pc, "program:", self.ram, "registers:", self.reg, ir[self.pc])
    #         op_code = ir[self.pc]
    #         operand_a = self.ram[self.pc + 1]
    #         operand_b = self.ram[self.pc + 2]
    #         op_size = (op_code >> 6) + 1

    #         print("pc:", self.pc, "op_code:", op_code, "registers:", self.reg)

    #         # NOP
    #         if op_code == 0:
    #             pass
    #         # HLT
    #         elif op_code == 1:
    #             self.running = False
    #         # RET
    #         elif op_code == 17:
    #             address = self.ram[self.stack_pointer]
    #             self.stack_pointer += 1
    #             self.pc = address
    #         # PUSH
    #         elif op_code == 69:
    #             self.stack_pointer -= 1
    #             value = self.reg[operand_a]
    #             self.ram[self.stack_pointer] = value
    #         # POP
    #         elif op_code == 70:
    #             value = self.ram[self.stack_pointer]
    #             self.stack_pointer += 1
    #             self.reg[operand_a] = value
    #         # PRN
    #         elif op_code == 71:
    #             print(self.ram_read(operand_a))
    #         # CALL
    #         elif op_code == 80:
    #             self.stack_pointer -= 1
    #             self.ram[self.stack_pointer] = self.pc + 1
    #             self.pc = self.reg[operand_a]
    #             continue
    #         # JMP
    #         elif op_code == 84:
    #             self.pc = self.reg[operand_a]
    #             continue
    #         # JEQ
    #         elif op_code == 85:
    #             if self.equal_flag is True:
    #                 print("jeq: jumping to", self.reg[operand_a], "op_code:", self.ram[self.reg[operand_a]])
    #                 self.pc = self.reg[operand_a]
    #                 continue
    #             else:
    #                 print("jeq: flag not true, not jumping")
    #         # JNE
    #         elif op_code == 86:
    #             if self.equal_flag is False:
    #                 print("jne: jumping to", self.reg[operand_a], "op_code:", self.ram[self.reg[operand_a]])
    #                 self.pc = self.reg[operand_a]
    #                 continue
    #             else:
    #                 print("jne: flag not false, not jumping")
    #         else:
    #             self.alu(op_code, operand_a, operand_b)

    #         self.pc += op_size

    def run(self):
        """Run the CPU."""
        op_size = 0
        ir = [0] * 256
        for i in range(len(self.ram)):
            ir[i] = self.ram[i]

        print("ir:", ir)

        while self.running:
            # print(self.pc, "running op_code", ir[self.pc])
            # print(self.pc, "program:", self.ram, "registers:", self.reg, ir[self.pc])
            op_code = ir[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            op_size = (op_code >> 6) + 1

            # print("pc:", self.pc, "op_code:", op_code, "registers:", self.reg)

            if self.op_codes.get(ir[self.pc]):
                self.op_codes.get(ir[self.pc])(operand_a, operand_b)
            else:
                self.alu(op_code, operand_a, operand_b)

            self.pc += op_size
