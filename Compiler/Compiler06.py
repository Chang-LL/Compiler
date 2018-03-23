INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF')

class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type},{repr(self.value)}_'
    
    def __repr__(self):
        return self.__str__()

class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Lexer error')

    def advance(self):
        self.pos+=1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        value = ''
        while self.current_char is not None and self.current_char.isdigit():
            value+=self.current_char
            self.advance()
        return int(value)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return Token(INTEGER,self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS,'-')
            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            else:
                self.error()
        return Token(EOF, None)

class Interperter():
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Interperter error')

    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token=self.current_token
        if token.type==INTEGER:
            self.eat(INTEGER)
            return token.value
        elif self.current_token.type==LPAREN:
            self.eat(LPAREN)
            value=self.expr()
            self.eat(RPAREN)
            return value

    def term(self):
        value=self.factor()
        while self.current_token.type in (MUL,DIV):
            token_type=self.current_token.type
            if token_type==MUL:
                self.eat(MUL)
                value *=self.factor()
            elif token_type==DIV:
                self.eat(DIV)
                value /=self.factor()
        return value
    
    def expr(self):
        value=self.term()
        while self.current_token.type in (PLUS,MINUS):
            token_type =self.current_token.type
            if token_type==PLUS:
                self.eat(PLUS)
                value+=self.term()
            elif token_type==MINUS:
                self.eat(MINUS)
                value-=self.term()
        return value

    def parse(self):
        return self.expr()

def main():
    while True:
        try:
            text=input('calc> ')
        except EOFError:
            print()
            break

        if len(text.strip()):
            interpreter=Interperter(Lexer(text))
            print(interpreter.parse())
        else:
            continue

if __name__=='__main__':
    main()


        

