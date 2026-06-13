
from syntatic_analyser.ast_nodes import (
    Program,
    Declaration,
    Assignment,
    If,
    While,
    Read,
    Write,
    Code_Block,
    Condition,
    BinaryOperation,
    Number,
    Identifier,
    Boolean,
)


# Geração da TAC
class IntermediateCodeGenerator:
    def __init__(self):
        self.code           = []   
        self._temporary_counter  = 0   
        self._label_counter = 0    

    # Gerando nomes únicos
    def _new_temporary(self):
        self._temporary_counter += 1
        return f't{self._temporary_counter}'

    def _new_label(self):
        self._label_counter += 1
        return f'L{self._label_counter}'

    # Percorrendo a AST para gerar TAC
    def generate(self, node):

        # Percorrer os comandos 
        if isinstance(node, Program):
            for command in node.commands:
                self.generate(command)

        # Declaração
        elif isinstance(node, Declaration):
            self.code.append(f'DECL {node.type} {node.name}')

        # Atribuição 
        elif isinstance(node, Assignment):
            result = self._generate_expression(node.expression)
            self.code.append(f'{node.name} = {result}')

        # Leitura 
        elif isinstance(node, Read):
            self.code.append(f'READ {node.name}')

        # Escrita 
        elif isinstance(node, Write):
            result = self._generate_expression(node.expression)
            self.code.append(f'WRITE {result}')

        # IF/ELSE
        elif isinstance(node, If):
            self._generate_if(node)

        # WHILE
        elif isinstance(node, While):
            self._generate_while(node)

        # Bloco com comandos internos
        elif isinstance(node, Code_Block):
            for command in node.commands:
                self.generate(command)

    # IF 
    def _generate_if(self, node):
        condition = self._generate_condition(node.condition)

        if node.else_block is not None:
            label_true  = self._new_label()
            label_false = self._new_label()
            label_end   = self._new_label()

            self.code.append(f'IF {condition} GOTO {label_true}')
            self.code.append(f'GOTO {label_false}')
            self.code.append(f'{label_true}:')
            self.generate(node.code_block)
            self.code.append(f'GOTO {label_end}')
            self.code.append(f'{label_false}:')
            self.generate(node.else_block)
            self.code.append(f'{label_end}:')
        else:
            label_true = self._new_label()
            label_end  = self._new_label()

            self.code.append(f'IF {condition} GOTO {label_true}')
            self.code.append(f'GOTO {label_end}')
            self.code.append(f'{label_true}:')
            self.generate(node.code_block)
            self.code.append(f'{label_end}:')

    # WHILE
    def _generate_while(self, node):
        label_start = self._new_label()
        label_body  = self._new_label()
        label_end   = self._new_label()

        self.code.append(f'{label_start}:')
        condition = self._generate_condition(node.condition)
        self.code.append(f'IF {condition} GOTO {label_body}')
        self.code.append(f'GOTO {label_end}')
        self.code.append(f'{label_body}:')
        self.generate(node.code_block)
        self.code.append(f'GOTO {label_start}')
        self.code.append(f'{label_end}:')

    #Condição
    def _generate_condition(self, node):
        left  = self._generate_expression(node.left)
        right = self._generate_expression(node.right)
        temporary  = self._new_temporary()
        # t1 = left operator right
        self.code.append(f'{temporary} = {left} {node.operator} {right}')
        return temporary

   
    #Expressão
    def _generate_expression(self, node):

        #Número literal 
        if isinstance(node, Number):
            return str(node.value)

        #Booleano
        elif isinstance(node, Boolean):
            return str(node.value).lower()

        #Identificador
        elif isinstance(node, Identifier):
            return node.name

        #Operação binária
        elif isinstance(node, BinaryOperation):
            left  = self._generate_expression(node.left)
            right = self._generate_expression(node.right)
            temporary  = self._new_temporary()
            self.code.append(f'{temporary} = {left} {node.operator} {right}')
            return temporary

        return ''

    def get_code(self):
        return self.code


# TESTE

if __name__ == "__main__":

    from lexical_analyser.scanner import Scanner
    from syntatic_analyser.parser import Parser
    from semantic_analyser.semantic import SemanticAnalyser

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

    scanner  = Scanner(source_code)
    tokens   = scanner.tokenization()

    parser   = Parser(tokens)
    ast      = parser.analyse()

    semantic = SemanticAnalyser()
    semantic.analyse(ast)

    intermediary_generator = IntermediateCodeGenerator()
    intermediary_generator.generate(ast)

    print("Código Intermediário(TAC):")
    print("--------------------------------------------------")
    for i, instruction in enumerate(intermediary_generator.get_code(), start=1):
        print(f"  {i:02d}  {instruction}")