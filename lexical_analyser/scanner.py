import re
from lexical_analyser.tokens import Token

RESERVED_WORDS = {
    'int':   'INT',
    'bool':  'BOOL',
    'if':    'IF',
    'else':  'ELSE',
    'while': 'WHILE',
    'write': 'WRITE',
    'read':  'READ',
    'true':  'TRUE',
    'false': 'FALSE',
}

OPERATORS = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVIDE',
    '=': 'ASSIGN',
    '<': 'LESS_THAN',
    '>': 'GREATER_THAN',
    '==': 'EQUAL',
    '!=': 'NOT_EQUAL',
}

DELIMITERS  = {
    ';': 'SEMICOLON',
    '(': 'LEFT_PARENTHESIS',
    ')': 'RIGHT_PARENTHESIS',
    '{': 'LEFT_BRACE',
    '}': 'RIGHT_BRACE',
}


class Scanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position   = 0

    def _error(self, char):
        raise Exception(f'Erro léxico: caractere inválido {char!r} na posição {self.position}')

    def _actual(self):
        if self.position < len(self.source_code):
            return self.source_code[self.position]
        return None

    def _foward(self):
        self.position += 1

    def tokenization(self):
        tokens = []

        while self.position < len(self.source_code):
            char = self._actual()

            #Ignora espaço em branco
            if char in (' ', '\t', '\n', '\r'):
                self._foward()
                continue

            #Reconhece identificadores e palavras reservadas
            if char.isalpha():
                beginning = self.position
                while self.position < len(self.source_code) and (self._actual().isalpha() or self._actual().isdigit()):
                    self._foward()
                word = self.source_code[beginning:self.position]
                if word in RESERVED_WORDS:
                    tokens.append(Token(RESERVED_WORDS[word], word))
                else:
                    tokens.append(Token('ID', word))
                continue

            #Reconhece constantes numéricas inteiras
            if char.isdigit():
                beginning = self.position
                while self.position < len(self.source_code) and self._actual().isdigit():
                    self._foward()
                # Erro: número seguido diretamente de letra (ex: 10abc)
                if self.position < len(self.source_code) and self._actual().isalpha():
                    self._error(self._actual())
                tokens.append(Token('NUMBER', int(self.source_code[beginning:self.position])))
                continue

            #Operadores duplos
            if self.position + 1 < len(self.source_code):
                double_operator = self.source_code[self.position:self.position + 2]

                if double_operator in OPERATORS:
                    tokens.append(Token(OPERATORS[double_operator], double_operator))
                    self.position += 2
                    continue

            #Operadores simples
            if char in OPERATORS:
                tokens.append(Token(OPERATORS[char], char))
                self._foward()
                continue

            
            #Delimitadores
            if char in DELIMITERS:
                tokens.append(Token(DELIMITERS[char], char))
                self._foward()
                continue

            #Nenhuma opção válida: erro léxico
            self._error(char)

        #Token de finalização
        tokens.append(Token('END', None))
        return tokens


# -----------------------------------
# Teste
# -----------------------------------
if __name__ == "__main__":

    source_code = """
    int x;
    x = 10;

    if (x > 5) {
        write(x);
    }
    """

    scanner = Scanner(source_code)

    tokens = scanner.tokenization()

    for token in tokens:
        print(token)