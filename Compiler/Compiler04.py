INTEGER,PLUS,MINUS,MUL,DIV,EOF='INTEGER','PLUS','MINUS','MUL','DIV','EOF'

class Token():
    def __init__(self, type, value):
        self.type=type
        self.value=value

    def __str__(self):
        return f'Token({self.type},{repr(self.value)})'

    def __repr__(self):
        return self.__str__()

class Lexer():
    def __init__(self,text):
        self.text=text
        self.pos=0
        self.current_char=self.text[self.pos]

    def error(self):
        raise Exception('Parse error')

    def advance(self):
        self.pos+=1
        if self.pos<len(self.text):
            self.current_char=self.text[self.pos]
        else:
            self.current_char=None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        value=''
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
            elif self.current_char=='*':
                self.advance()
                return Token(MUL,'*')
            elif self.current_char=='/':
                self.advance()
                return Token(DIV,'/')
            else:
                self.error()
        return Token(EOF,None)

class Interpreter():
    def __init__(self,lexer):
        self.lexer=lexer
        self.current_token=self.lexer.get_next_token()

    def error(self):
        raise Exception('Interpret error')

    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error()        

    def factor(self):
        token=self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        value=self.factor()
        while self.current_token.type in (MUL,DIV):
            token_type=self.current_token.type
            if token_type==MUL:
                self.eat(MUL)
                value*=self.factor()
            elif token_type==DIV:
                self.eat(DIV)
                value/=self.factor()
            
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
            interpreter=Interpreter(Lexer(text))
            result=interpreter.parse()
            print(result)

if __name__=='__main__':
    main()
