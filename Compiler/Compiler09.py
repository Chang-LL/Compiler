(INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, 
RPAREN, EOF,DOT,BEGIN,END, 
SEMI,ID,ASSIGN)= ('INTEGER', 'PLUS', 'MINUS', 
                   'MUL', 'DIV', 'LPAREN', 
                   'RPAREN', 'EOF','DOT',
                   'BEGIN','END','SEMI','ID',
                   'ASSIGN')

class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type},{repr(self.value)})'
    
    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS={
    'BEGIN':Token('BEGIN','BEGIN'),
    'END':Token('END','END')}

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
    
    def peek(self):
        peek_pos=self.pos+1
        if peek_pos>=len(self.text):
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        value = ''
        while self.current_char is not None and self.current_char.isdigit():
            value+=self.current_char
            self.advance()
        return int(value)

    def _id(self):
        result=''
        while self.current_char is not None and self.current_char.isalnum():
            result+=self.current_char
            self.advance()
        token=RESERVED_KEYWORDS.get(result,Token(ID,result))
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return Token(INTEGER,self.integer())
            elif self.current_char.isalpha():
                return self._id()
            elif self.current_char==':' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(ASSIGN,':=')
            elif self.current_char==';':
                self.advance()
                return Token(SEMI,';')
            elif self.current_char=='.':
                self.advance()
                return Token(DOT,'.')
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

class AST():
    pass

class Compound(AST):
    def __init__(self):
        self.child=[]

class Assign(AST):
    def __init__(self, left,op,right):
        self.left=left
        self.token=self.op=op
        self.right=right

class Var(AST):
    def __init__(self,token):
        self.token=token
        self.value=token.value

class NoOp(AST):
    pass

class UnaryOp(AST):
    def __init__(self,op,expr):
        self.token=self.op=op
        self.expr=expr

class BinOp(AST):
    def __init__(self, left,op,right):
        self.left=left
        self.token=self.op=op
        self.right=right

class Num(AST):
    def __init__(self,token):
        self.token=token
        self.value=token.value
        
class Parser():
    def __init__(self,lexer):
        self.lexer=lexer
        self.current_token=lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error()

    def variable(self):
        node=Var(self.current_token)
        self.eat(ID)
        return node
    
    def factor(self):
        token=self.current_token
        if token.type==PLUS:
            self.eat(PLUS)
            node=UnaryOp(token,self.factor())
            return node
        elif token.type==MINUS:
            self.eat(MINUS)
            node=UnaryOp(token,self.factor())
            return node
        elif token.type==INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type==LPAREN:
            self.eat(LPAREN)
            node=self.expr()
            self.eat(RPAREN)
            return node
        else:
            node=self.variable()
            return node

    def term(self):
        node=self.factor()
        while self.current_token.type in (MUL,DIV):
            token=self.current_token
            if token.type==MUL:
                self.eat(MUL)
            elif token.type==DIV:
                self.eat(DIV)
            node=BinOp(left=node,op=token,right=self.factor())
        return node
    def expr(self):
        node=self.term()
        while self.current_token.type in (PLUS,MINUS):
            token=self.current_token
            if token.type==PLUS:
                self.eat(PLUS)
            elif token.type==MINUS:
                self.eat(MINUS)
            node=BinOp(left=node,op=token,right=self.term())
        return node


    def empty(self):
        return NoOp()

    def assignment_statement(self):
        left=self.variable()
        token=self.current_token
        self.eat(ASSIGN)
        right=self.expr()
        node=Assign(left,token,right)
        return node


    def statement(self):
        if self.current_token.type==BEGIN:
            node=self.compound_statement()
        elif self.current_token.type==ID:
            node=self.assignment_statement()
        else:
            node=self.empty()
        return node

    def statement_list(self):
        node=self.statement()
        results=[node]
        while self.current_token.type==SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type==ID:
            self.error()
        return results

    def compound_statement(self):
        self.eat(BEGIN)
        nodes=self.statement_list()
        self.eat(END)
        root=Compound()
        for node in nodes:
            root.child.append(node)
        return root

    def program(self):
        node=self.compound_statement()
        self.eat(DOT)
        return node

    def parse(self):
        node=self.program()
        if self.current_token.type!=EOF:
            self.error()
        return node

class NodeVistor():
    def visit(self,node):
        method_name='visit_'+type(node).__name__
        visitor=getattr(self,method_name,self.generic_visit)
        return visitor(node)
    def generic_visit(self):
        raise Exception('No visitor_{} method'.format(type(node).__name__))

class Interpreter(NodeVistor):
    GLOBAL_SCOPE = {}
    def __init__(self,parser):
        self.parser=parser
    
    def visit_BinOp(self,node):        
        if node.op.type==PLUS:
            return self.visit(node.left)+self.visit(node.right)
        elif node.op.type==MINUS:
            return self.visit(node.left)-self.visit(node.right)
        elif node.op.type==MUL:
            return self.visit(node.left)*self.visit(node.right)
        elif node.op.type==DIV:
            return self.visit(node.left)/self.visit(node.right)

    def visit_Num(self,node):
        return node.value

    def visit_Compound(self,node):
        for child in node.child:
            self.visit(child)

    def visit_NoOp(self,node):
        pass
    def visit_Assign(self,node):
        var_name=node.left.value
        self.GLOBAL_SCOPE[var_name]=self.visit(node.right)
    def visit_Var(self,node):
        var_name=node.value
        var=self.GLOBAL_SCOPE.get(var_name)
        if var is None:
            raise NameError(repr(var_name))
        else:
            return var

    def interpret(self):
        tree=self.parser.parse()
        return self.visit(tree)


    def visit_UnaryOp(self,node):
        op=node.op.type
        if op==PLUS:
            return +self.visit(node.expr)
        elif op==MINUS:
            return -self.visit(node.expr)

def main():
    while True:
        try:
            #text=input('spi> ')
            text='BEGIN\n\n    BEGIN\n        number := 2;\n        a := number;\n        b := 10 * a + 10 * number / 4;\n        c := a - - b\n    END;\n\n    x := 11;\nEND.\n'         
        except EOFError:
            print()
            break

    if len(text.strip()):
        parser=Parser(Lexer(text))
        interpreter=Interpreter(parser)
        result=interpreter.interpret()
        print(result)
if __name__=='__main__':
    main()
