from lexical_analyser.scanner import Scanner
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
    Boolean
)


# Analisador sintático - Parser Descendente Recursivo
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position    = 0

    def _actual(self):
        return self.tokens[self.position]

    def _consume(self, expected_type):
        token = self._actual()
        if token.type != expected_type:
            raise Exception(f'Erro sintático: esperado "{expected_type}", 'f'encontrado "{token.type}" (value: "{token.value}")')
        self.position += 1
        return token

    def analyse(self):
        commands = []
        while self._actual().type != 'END':
            commands.append(self._analyse_commands())
        return Program(commands)

    def _analyse_commands(self):
        token = self._actual()

        if token.type in ('INT', 'BOOL'):
            return self._analyse_declaration()
        elif token.type == 'ID':
            return self._analyse_Assignment()
        elif token.type == 'READ':
            return self._analyse_read()
        elif token.type == 'WRITE':
            return self._analyse_write()
        elif token.type == 'IF':
            return self._analyse_if()
        elif token.type == 'WHILE':
            return self._analyse_while()
        else:
            raise Exception(f'Erro sintático: início de command inválido 'f'"{token.type}" (value: "{token.value}")')
            

    # Analisa declaração de variáveis ((INT | BOOL) ID));
    def _analyse_declaration(self):
        type_token = self._actual()
        self._consume(type_token.type)      
        name = self._consume('ID')
        self._consume('SEMICOLON')
        return Declaration(type_token.value, name.value)

    # Analisa a atribuição de valores de variáveis (ID = expressao ;)
    def _analyse_Assignment(self):
        name = self._consume('ID')
        self._consume('ASSIGN')
        expression = self._analyse_expression()
        self._consume('SEMICOLON')
        return Assignment(name.value, expression)

    # Analisa leitura de IDs (READ ( ID )) ;
    def _analyse_read(self):
        self._consume('READ')
        self._consume('LEFT_PARENTHESIS')
        name = self._consume('ID')
        self._consume('RIGHT_PARENTHESIS')
        self._consume('SEMICOLON')
        return Read(name.value)

    # Analisa Escrita de expressões (WRITE ( expressao ) ;)
    def _analyse_write(self):
        self._consume('WRITE')
        self._consume('LEFT_PARENTHESIS')
        expression = self._analyse_expression()
        self._consume('RIGHT_PARENTHESIS')
        self._consume('SEMICOLON')
        return Write(expression)

    # Analisa bloco de código Se ( IF ( condition ) { code_block } [ ELSE { code_block } ] ;)
    def _analyse_if(self):
        self._consume('IF')
        self._consume('LEFT_PARENTHESIS')
        condition = self._analyse_condition()
        self._consume('RIGHT_PARENTHESIS')
        self._consume('LEFT_BRACE')
        code_block = self._analyse_code_block()
        self._consume('RIGHT_BRACE')

        else_block = None
        if self._actual().type == 'ELSE':
            self._consume('ELSE')
            self._consume('LEFT_BRACE')
            else_block = self._analyse_code_block()
            self._consume('RIGHT_BRACE')

        self._consume('SEMICOLON')
        return If(condition, code_block, else_block)

    # Analisa estrutura enquanto( WHILE ( condition ) { code_block } ;)
    def _analyse_while(self):
        self._consume('WHILE')
        self._consume('LEFT_PARENTHESIS')
        condition = self._analyse_condition()
        self._consume('RIGHT_PARENTHESIS')
        self._consume('LEFT_BRACE')
        code_block = self._analyse_code_block()
        self._consume('RIGHT_BRACE')
        self._consume('SEMICOLON')
        return While(condition, code_block)

    # Analisa o bloco de código do Se Code_block (lista de commands (os { } são consumidos pelo chamador))
    def _analyse_code_block(self):
        commands = []
        while self._actual().type != 'RIGHT_BRACE':
            if self._actual().type == 'END':
                raise Exception('Erro sintático: esperado "}" mas chegou ao fim do arquivo')
            commands.append(self._analyse_commands())
        return Code_Block(commands)

    # Analisa condição de comparação ( expressao (== | != | < | >) expressao)
    def _analyse_condition(self):
        left  = self._analyse_expression()
        operator_token  = self._actual()
        if operator_token.type not in ('EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'GREATER_THAN'):
            raise Exception(f'Erro sintático: operador relacional esperado (==, !=, <, >), 'f'encontrado "{operator_token.type}" (value: "{operator_token.value}")')
        self._consume(operator_token.type)
        right = self._analyse_expression()
        return Condition(left, operator_token.value, right)

    # Analisa expressão de soma e subtração (termo ( (+ | -) termo )*)
    def _analyse_expression(self):
        left = self._analyse_term()
        while self._actual().type in ('PLUS', 'MINUS'):
            operator     = self._consume(self._actual().type)
            right = self._analyse_term()
            left     = BinaryOperation(left, operator.value, right)
        return left

    # Analisa termo de multiplicação e divisor (fator ( (* | /) fator )*)
    def _analyse_term(self):
        left = self._analyse_factor()
        while self._actual().type in ('TIMES', 'DIVIDE'):
            operator = self._consume(self._actual().type)
            right = self._analyse_factor()
            left = BinaryOperation(left, operator.value, right)
        return left

    # Analisa fator mínimo(NUMBER | ID | TRUE | FALSE | ( expressao ) )
    def _analyse_factor(self):
        token = self._actual()
        if token.type == 'NUMBER':
            self._consume('NUMBER')
            return Number(token.value)
        elif token.type == 'ID':
            self._consume('ID')
            return Identifier(token.value)
        elif token.type == 'TRUE':
            self._consume('TRUE')
            return Boolean(True)
        elif token.type == 'FALSE':
            self._consume('FALSE')
            return Boolean(False)
        elif token.type == 'LEFT_PARENTHESIS':
            self._consume('LEFT_PARENTHESIS')
            expression = self._analyse_expression()
            self._consume('RIGHT_PARENTHESIS')
            return expression
        else:
            raise Exception(f'Erro sintático: fator inválido 'f'"{token.type}" (value: "{token.value}")')



# TESTE DO ANALISADOR SINTÁTICO

if __name__ == "__main__":

    source_code = """
    int x;
    x = 10;
    if (x > 5) {
        write(x+10);
    };
    """

    # Análise Léxica
    scanner = Scanner(source_code)
    tokens = scanner.tokenization()

    print("\nTOKENS:")

    for i, token in enumerate(tokens, start=1):
        print(f"{i:02d}: {token}")

    # Análise Sintática
    parser = Parser(tokens)
    ast = parser.analyse()

    print("\nAST:")

    print("Program")
    print("{")

    for i, command in enumerate(ast.commands, start=1):
        print(f"  {i:02d}: {command}")

    print("}")

    print("\nCOMANDOS:")

    for i, command in enumerate(ast.commands, start=1):
        print(f"\nCommand {i}:")
        print(command)