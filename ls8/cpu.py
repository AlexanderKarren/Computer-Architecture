"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.equal_flag = False
        self.less_than_flag = False
        self.greater_than_flag = False

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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # NOT
        if op == 105:
            self.reg[reg_a] = ~self.reg[reg_a]
        # LDI
        elif op == 130:
            self.ram_write(reg_a, reg_b)
        # ADD
        elif op == 160:
            self.reg[reg_a] += self.reg[reg_b]
        # MUL
        elif op == 162:
            self.reg[reg_a] *= self.reg[reg_b]
        # MOD
        elif op == 164:
            self.reg[reg_a] %= self.reg[reg_b]
        # CMP
        elif op == 167:
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
        # AND
        elif op == 168:
            self.reg[reg_a] &= self.reg[reg_b]
        # OR
        elif op == 170:
            self.reg[reg_a] |= self.reg[reg_b]
        # XOR
        elif op == 171:
            self.reg[reg_a] ^= self.reg[reg_b]
        # SHL
        elif op == 172:
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        # SHR
        elif op == 173:
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        stack_pointer = len(self.ram) - 1
        op_size = 0
        running = True
        ir = [0] * 256
        for i in range(len(self.ram)):
            ir[i] = self.ram[i]

        # print(ir)

        while running:
            # print(self.pc, "running op_code", ir[self.pc])
            # print(self.pc, "program:", self.ram, "registers:", self.reg, ir[self.pc])
            op_code = ir[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            op_size = (op_code >> 6) + 1

            # NOP
            if op_code == 0:
                pass
            # HLT
            elif op_code == 1:
                running = False
            # RET
            elif op_code == 17:
                address = self.ram[stack_pointer]
                stack_pointer += 1
                self.pc = address
            # PUSH
            elif op_code == 69:
                stack_pointer -= 1
                value = self.reg[operand_a]
                self.ram[stack_pointer] = value
            # POP
            elif op_code == 70:
                value = self.ram[stack_pointer]
                stack_pointer += 1
                self.reg[operand_a] = value
            # PRN
            elif op_code == 71:
                print(self.ram_read(operand_a))
            # CALL
            elif op_code == 80:
                stack_pointer -= 1
                self.ram[stack_pointer] = self.pc + 1
                self.pc = self.reg[operand_a]
                continue
            # JMP
            elif op_code == 84:
                self.pc = self.reg[operand_a]
                continue
            # JEQ
            elif op_code == 85:
                if self.equal_flag is True:
                    # print("jeq: jumping to", self.reg[operand_a], "op_code:", self.ram[self.reg[operand_a]])
                    self.pc = self.reg[operand_a]
                    continue
                # else:
                #     print("jeq: flag not true, not jumping")
            # JNE
            elif op_code == 86:
                if self.equal_flag is False:
                    # print("jne: jumping to", self.reg[operand_a], "op_code:", self.ram[self.reg[operand_a]])
                    self.pc = self.reg[operand_a]
                    continue
                # else:
                #     print("jne: flag not false, not jumping")
            else:
                self.alu(op_code, operand_a, operand_b)

            self.pc += op_size
