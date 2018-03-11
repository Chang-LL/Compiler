INTEGER,PLUS,MINUS,MUL,DIV,EOF='INTEGER','PLUS','MINUS','MUL','DIV','EOF'

class Token():
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __str__(self):
        return f'Token({self.type},{repr(self.value)})'

    def __repr__(self):
        return self.__str__()

class Interpreter():
    def __init__(self, text):
        self.text=text
        self.pos=0
        self.current_token=None
        self.current_char=self.text[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        self.pos+=1
        if self.pos>=len(self.pos):
            self.current_char=None
        else:
            self.current_char=self.text[self.pos]

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
                self.advance()
                continue
            elif self.current_char.isdigit():
                return Token(INTEGER,self.integer())
            elif self.current_char=='+':
                self.advance()
                return Token(PLUS,'+')
            elif self.current_char=='-':
                self.advance()
                return Token(MINUS,'-')
            else:
                self.error()
        return Token(EOF,None)

    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.get_next_token()
        else:
            self.error()

    def term(self):
        token=self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.current_token=self.get_next_token()
        result=self.term()
        while self.current_token.type in (PLUS,MINUS):
            token=self.current_token
            if token.type==PLUS:
                self.eat(PLUS)
                self.eat(PLUS)
                result+=self.term()
            elif token.type==MINUS:
                self.eat(MINUS)
                result-=self.term()
            else:
                self.error()
        return result

def main():
    while True:
        try:
            text=input('calc> ')
        except EOFError:
            print()
            break

        if not text:
            continue
        interpreter=Interpreter(text)
        result=interpreter.expr()
        print(result)

if __name__=='__main__':
    main()
