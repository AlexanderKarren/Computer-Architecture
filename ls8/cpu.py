"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        if len(sys.argv) > 1:
            file = open(sys.argv[1], 'r')
            program = []
            for instruction in file.read().split('\n'):
                trimmed_instruction = ""
                if len(instruction) >= 8:
                    for i in range(8):
                        if instruction[i] == '0' or instruction[i] == '1':
                            trimmed_instruction += instruction[i]
                instruction = trimmed_instruction
                if len(instruction) > 0:
                    # print(instruction)
                    program.append(int(instruction, 2))
            # print(program)
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
        # LDI
        if op == 130:
            self.ram_write(reg_a, reg_b)
        # PRN
        elif op == 71:
            print(self.ram_read(reg_a))
        # ADD
        elif op == 160:
            self.reg[reg_a] += self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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
        op_size = 0
        running = True
        ir = [0] * 256
        for i in range(len(self.ram)):
            ir[i] = self.ram[i]

        print(ir)

        while running:
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            op_size = (ir[self.pc] >> 6) + 1

            if ir[self.pc] == 1:
                running = False
            else:
                self.alu(ir[self.pc], operand_a, operand_b)

            self.pc += op_size
