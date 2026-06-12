
# Operadores TAC(instrução de bytecode)
OPERATOR_TO_BYTECODE = {
    '+':  'ADD',
    '-':  'SUB',
    '*':  'MUL',
    '/':  'DIV',
    '==': 'CMP_EQ',
    '!=': 'CMP_NEQ',
    '<':  'CMP_LT',
    '>':  'CMP_GT',
}

# GERADOR DE CÓDIGO FINAL  (Bytecode)
class FinalCodeGenerator:
    def __init__(self):
        self.bytecode = []   

    def _is_number(self, element):
        try:
            int(element)
            return True
        except ValueError:
            return False
        
# Verifica se é literal númerico oubooleano
    def _is_literal(self, element):
        return self._is_number(element) or element in ('true', 'false')

#Define PUSH para literais e load para variáveis e temposrários
    def _load_value(self, element):
        if self._is_literal(element):
            self.bytecode.append(f'PUSH {element}')
        else:
            self.bytecode.append(f'LOAD {element}')

#Verifica o tipo do lado direito de uma atribuição TAC.
    def _parse_right_hand_side(self, right_hand_side):
        for operator in ('==', '!=', '+', '-', '*', '/', '<', '>'):
            if f' {operator} ' in right_hand_side:
                left, right = right_hand_side.split(f' {operator} ', 1)
                return ('binaryoperation', left.strip(), operator, right.strip())

        if self._is_literal(right_hand_side):
            return ('literal', right_hand_side)

        return ('var', right_hand_side)

  
    #Traduz lista TAC inteira para bytecode
    def generate(self, tac_code):
        for instruction in tac_code:
            self._translate(instruction.strip())
        self.bytecode.append('HALT')
        return self.bytecode

    # Traduz uma instrução TAC
    def _translate(self, instruction):
        parts = instruction.split()

        # Label:  L1:
        if instruction.endswith(':') and len(parts) == 1:
            self.bytecode.append(instruction)   # mantém como está
            return

        # DECL type name vira alloc name 
        if parts[0] == 'DECL':
            var_name = parts[2]
            self.bytecode.append(f'alloc {var_name}') #alloc = Aloca váriavel na memória (Instrunção para máquina)
            return

        #  READ name vira READ / STORE name 
        if parts[0] == 'READ':
            self.bytecode.append('READ')
            self.bytecode.append(f'STORE {parts[1]}')
            return

        # PRINT value vira LOAD/PUSH value + PRINT 
        if parts[0] == 'WRITE':
            self._load_value(parts[1])
            self.bytecode.append('WRITE')
            return

        # GOTO L1  vira JMP L1 
        if parts[0] == 'GOTO':
            self.bytecode.append(f'JMP {parts[1]}')
            return

        #  IF cond GOTO L1  vira LOAD/PUSH cond + JMP_IF_TRUE L1 
        if parts[0] == 'IF' and len(parts) == 4 and parts[2] == 'GOTO':
            self._load_value(parts[1])
            self.bytecode.append(f'JMP_IF_TRUE {parts[3]}')
            return

        #  name = right_hand_side  (atribuição simples ou operação binária) 
        if ' = ' in instruction:
            left_hand_side, right_hand_side = instruction.split(' = ', 1)
            left_hand_side  = left_hand_side.strip()
            right_hand_side  = right_hand_side.strip()
            kind = self._parse_right_hand_side(right_hand_side)

            # Literal vira PUSH valor / STORE left_hand_side
            if kind[0] == 'literal':
                self.bytecode.append(f'PUSH {kind[1]}')
                self.bytecode.append(f'STORE {left_hand_side}')

            # Variável vira LOAD src / STORE left_hand_side
            elif kind[0] == 'var':
                self.bytecode.append(f'LOAD {kind[1]}')
                self.bytecode.append(f'STORE {left_hand_side}')

            # Operação vira LOAD/PUSH esq + LOAD/PUSH dir + OP + STORE left_hand_side
            elif kind[0] == 'binaryoperation':
                _, left, operator, right = kind
                self._load_value(left)
                self._load_value(right)
                self.bytecode.append(OPERATOR_TO_BYTECODE[operator])
                self.bytecode.append(f'STORE {left_hand_side}')

            return

    def get_bytecode(self):
        return self.bytecode



# TESTE COMPILADOR COMPLETO

if __name__ == "__main__":

    from lexical_analyser.scanner import Scanner
    from syntatic_analyser.parser import Parser
    from semantic_analyser.semantic import SemanticAnalyser
    from code_generator.intermediate import IntermediateCodeGenerator

    source_code = """
    int x;
    int y;
    bool flag;
    x = 10;
    y = 3;
    flag = false;
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

    # Analisador Léxico
    scanner = Scanner(source_code)
    tokens  = scanner.tokenization()

    # Analisador Sintático
    parser = Parser(tokens)
    ast    = parser.analyse()

    # Analisador Semântico
    semantic = SemanticAnalyser()
    semantic.analyse(ast)

    # Código Intermediário (TAC)
    ir_gen = IntermediateCodeGenerator()
    ir_gen.generate(ast)
    tac = ir_gen.get_code()

    print("TAC (Intermediate Code):")
    for i, instruction in enumerate(tac, start=1):
        print(f"  {i:02d}  {instruction}")

    # Código Final (Bytecode)
    final_gen = FinalCodeGenerator()
    bytecode  = final_gen.generate(tac)

    print("\nBytecode (Final Code):")
    for i, instruction in enumerate(bytecode, start=1):
        print(f"  {i:02d}  {instruction}")
