# Máquina virtual para executar bytecode
class VirtualMachine:

    def __init__(self):
        self.stack = []          # pilha da máquina
        self.memory = {}         # memória: { variavel: valor }
        self.labels = {}         # labels: { L1: posição }
        self.program_counter = 0 # instrução atual

    # Primeira etapa: percorre o bytecode para encontrar os labels e suas posições
    def _find_labels(self, bytecode):

        for position, instruction in enumerate(bytecode):

            instruction = instruction.strip()

            # Label encontrado
            if instruction.endswith(':'):
                label_name = instruction[:-1]
                self.labels[label_name] = position

    # Executa as instruções do programa
    def run(self, bytecode):

        # Procura os labels antes da execução
        self._find_labels(bytecode)

        self.program_counter = 0

        while self.program_counter < len(bytecode):

            instruction = bytecode[self.program_counter].strip()

            # Ignora labels durante a execução
            if instruction.endswith(':'):
                self.program_counter += 1
                continue

            parts = instruction.split()

            opcode = parts[0]

            # Finaliza o programa
            
            if opcode == 'HALT':
                print("\nPrograma finalizado.")
                break

            # Cria a variável na memória

            elif opcode == 'alloc':

                variable_name = parts[1]

                self.memory[variable_name] = 0

            
            # Adiciona um valor na pilha
            
            elif opcode == 'PUSH':

                value = parts[1]

                # inteiro
                if value.isdigit():
                    value = int(value)

                # boolean
                elif value == 'true':
                    value = True

                elif value == 'false':
                    value = False

                self.stack.append(value)

            # Carrega o valor da variável para a pilha
            elif opcode == 'LOAD':

                variable_name = parts[1]

                value = self.memory[variable_name]

                self.stack.append(value)

            # Salva o valor da pilha na variável
            elif opcode == 'STORE':

                variable_name = parts[1]

                value = self.stack.pop()

                self.memory[variable_name] = value

            # Operações aritméticas
            elif opcode == 'ADD':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left + right)

            elif opcode == 'SUB':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left - right)

            elif opcode == 'MUL':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left * right)

            elif opcode == 'DIV':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left // right)

            # Operações de comparação
            elif opcode == 'CMP_EQ':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left == right)

            elif opcode == 'CMP_NEQ':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left != right)

            elif opcode == 'CMP_LT':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left < right)

            elif opcode == 'CMP_GT':

                right = self.stack.pop()
                left  = self.stack.pop()

                self.stack.append(left > right)

            # Salto incondicional
            elif opcode == 'JMP':

                label = parts[1]

                self.program_counter = self.labels[label]

                continue

            # Salta se a condição for verdadeira
            elif opcode == 'JMP_IF_TRUE':

                label = parts[1]

                condition = self.stack.pop()

                if condition:
                    self.program_counter = self.labels[label]
                    continue

            # Read: lê um valor do usuário e coloca na pilha
            elif opcode == 'READ':

                value = int(input("Entrada: "))

                self.stack.append(value)

            # Write: exibe um valor na saída
            elif opcode == 'WRITE':

                value = self.stack.pop()

                print(f"OUTPUT: {value}")

            # Instrução inválida
            else:
                raise Exception(f'Instrução inválida: {instruction}')

            self.program_counter += 1

# Teste completo

if __name__ == "__main__":

    from lexical_analyser.scanner import Scanner
    from syntatic_analyser.parser import Parser
    from semantic_analyser.semantic import SemanticAnalyser
    from code_generator.intermediate import IntermediateCodeGenerator
    from code_generator.final import FinalCodeGenerator


    source_code = """
    int x;
    int y;

    x = 10;
    y = 3;

    x = x + y * 2;

    if (x > y) {
        write(x);
    } else {
        write(y);
    };

    while (x > 0) {
        x = x - 1;
    };

    write(x);
    """

    # 1. LÉXICO

    scanner = Scanner(source_code)

    tokens = scanner.tokenization()

    # 2. SINTÁTICO

    parser = Parser(tokens)

    ast = parser.analyse()

    # 3. SEMÂNTICO

    semantic = SemanticAnalyser()

    semantic.analyse(ast)

    # 4. CÓDIGO DE TRÊS ENDEREÇOS (TAC)

    intermediate_generator = IntermediateCodeGenerator()

    intermediate_generator.generate(ast)

    tac = intermediate_generator.get_code()

    print("\nTAC:")
    print("--------------------------------------------------")

    for instruction in tac:
        print(instruction)

    # 5. GERAÇÃO DO BYTECODE

    final_generator = FinalCodeGenerator()

    bytecode = final_generator.generate(tac)

    print("\nBYTECODE:")
    print("--------------------------------------------------")

    for instruction in bytecode:
        print(instruction)

    # 6. MÁQUINA VIRTUAL

    vm = VirtualMachine()

    print("\nEXECUÇÃO:")
    print("--------------------------------------------------")

    vm.run(bytecode)

    print("\nMEMÓRIA FINAL:")
    print("--------------------------------------------------")

    for variable, value in vm.memory.items():
        print(f"{variable} = {value}")