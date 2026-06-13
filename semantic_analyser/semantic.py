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


class SemanticAnalyser:
    def __init__(self):
        self.symbol_table = {}   

    def _error(self, message):
        raise Exception(f'Erro Semântico: {message}')

    # Percorrendo a AST
    def analyse(self, node):

        # Vai percorre todos os comandos
        if isinstance(node, Program):
            for command in node.commands:
                self.analyse(command)

        # Duplicidade e inserção na tabela
        elif isinstance(node, Declaration):
            if node.name in self.symbol_table:
                self._error(f'Variável "{node.name}" já foi declarada')
            self.symbol_table[node.name] = node.type

        # Existência e Compatibilidade dos tipos Atribuição 
        elif isinstance(node, Assignment):
            if node.name not in self.symbol_table:
                self._error(f'Variável "{node.name}" sem declaração prévia')
            var_type  = self.symbol_table[node.name]
            expression_type = self._check_expression(node.expression)
            if var_type != expression_type:
                self._error(
                    f'Tipo incompatável: "{node.name}" é tipo "{var_type}", '
                    f'expressão retorna tipo "{expression_type}"'
                )

        # Existência da variável
        elif isinstance(node, Read):
            if node.name not in self.symbol_table:
                self._error(f'Variável "{node.name}" sem declaração prévia')

        # Verificação da expressão semântica
        elif isinstance(node, Write):
            self._check_expression(node.expression)

        # Validação de blocos IF, condição booleana 
        elif isinstance(node, If):
            condition_type = self._check_condition(node.condition)
            if condition_type != 'bool':
                self._error(f'A condição IF deve retornar valor booleano, retornou tipo "{condition_type}"')
            self.analyse(node.code_block)
            if node.else_block is not None:
                self.analyse(node.else_block)

        # Validação de blocos WHILE, condição booleana 
        elif isinstance(node, While):
            condition_type = self._check_condition(node.condition)
            if condition_type != 'bool':
                self._error(f'A condição WHILE deve retornar valor booleano, retornou tipo "{condition_type}"')
            self.analyse(node.code_block)

        # Percorrer comandos internos 
        elif isinstance(node, Code_Block):
            for command in node.commands:
                self.analyse(command)

    # Verificação de tipos, expressão_esquerda operador expressão_direita, retorna booleano
    def _check_condition(self, node):
        left_type  = self._check_expression(node.left)
        right_type = self._check_expression(node.right)
        if left_type != right_type:
            self._error(
                f'Tipo das Condições incompatíveis: '
                f'tipo da expressão da esquerda é "{left_type}", tipo da expressão da direita é "{right_type}"'
            )
        return 'bool'

    # Retorna o tipo resultante do nó, expressão
    def _check_expression(self, node):

        # Número int 
        if isinstance(node, Number):
            return 'int'

        # Verificação de validade e retorno de booleano
        elif isinstance(node, Boolean):
            if node.value not in (True, False):
                self._error(f'Valor booleano inválido: "{node.value}"')
            return 'bool'

        #Buscar identificador na tabela
        elif isinstance(node, Identifier):
            if node.name not in self.symbol_table:
                self._error(f'Variável "{node.name}" sem declaração prévia')
            return self.symbol_table[node.name]

        # Operação binária, os lados devem ser de mesmo tipo 
        elif isinstance(node, BinaryOperation):
            left_type  = self._check_expression(node.left)
            right_type = self._check_expression(node.right)
            if left_type != right_type:
                self._error(
                    f'Tipo incompatível da operação "{node.operator}": '
                    f'esquerda é tipo "{left_type}", direita é tipo "{right_type}"'
                )
            return left_type

        # Condição - expressão,  retorna booleano 
        elif isinstance(node, Condition):
            return self._check_condition(node)

        self._error(f'Nó da expressão desconhecida: {type(node).__name__}')

# Teste

if __name__ == "__main__":

    from lexical_analyser.scanner import Scanner
    from syntatic_analyser.parser import Parser

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

    print("Análise semântica completa.")
    print("\nTabela de Símbolo:")
    print("--------------------------------------------------")
    for name, var_type in semantic.symbol_table.items():
        print(f"  {name}: {var_type}")