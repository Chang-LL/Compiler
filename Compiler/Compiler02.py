INTEGER,PLUS,MINUS,MUL,DIV,EOF='INTEGER','PLUS','MINUS','MUL','DIV','EOF'

class Token():
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __str__(self):
        return f'Token({self.type},{self.value})'

    def __repr__(self):
        return self.__str__()

class Interpreter():
    def __init__(self, text):
        self.text=text
        self.pos=0
        self.current_token=None
        self.current_char=self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos+=1
        if self.pos>=len(self.text):
            self.current_char=None
        else:
            self.current_char=self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result=''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER,self.integer())
            if self.current_char=='+':
                self.advance()
                return Token(PLUS,'+')
            if self.current_char=='-':
                self.advance()
                return Token(MINUS,'-')
            #乘除法
            if self.current_char=='*':
                self.advance()
                return Token(MUL,'*')
            if self.current_char=='/':
                self.advance()
                return Token(DIV,'/')
            self.error()
        return Token(EOF,None)
    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.get_next_token()
        else:
            self.error()
    def expr(self):
        self.current_token=self.get_next_token()
        left=self.current_token
        self.eat(INTEGER)
        #多个表达式
        if self.pos>=len(self.text):
            self.error()
        result=left.value
        while self.pos<len(self.text):
            op=self.current_token
            if op.type==PLUS:
                self.eat(PLUS)
            elif op.type==MINUS:
                self.eat(MINUS)
            #乘除法
            elif op.type==MUL:
                self.eat(MUL)
            elif op.type==DIV:
                self.eat(DIV)
            else:
                self.error()

            right=self.current_token
            self.eat(INTEGER)

            if op.type==PLUS:
                result=result+right.value
            elif op.type==MINUS:
                result=result-right.value
            elif op.type==MUL:
                result=result*right.value
            elif op.type==DIV:
                result=result/right.value
            else:
                self.error()
        return result

def main():
    while True:
        try:
            text=input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter=Interpreter(text)
        result=interpreter.expr()
        print(result)

if __name__=='__main__':
    main()