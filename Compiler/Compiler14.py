import collections
(INTEGER, PLUS, MINUS, MUL, INTEGER_DIV, LPAREN, 
RPAREN, EOF,DOT,BEGIN,END,SEMI,ID,ASSIGN,COLON,COMMA,
FLOAT_DIV,VAR,PROGRAM,INTEGER_CONST,REAL_CONST,REAL,
PROCEDURE) = ('INTEGER', 'PLUS', 'MINUS', 
                   'MUL', 'INTEGER_DIV', 'LPAREN', 'RPAREN', 'EOF','DOT',
                   'BEGIN','END','SEMI','ID','ASSIGN','COLON','COMMA',
                   'FLOAT_DIV','VAR','PROGRAM','INTEGER_CONST','REAL_CONST',
                   'REAL','PROCEDURE')

class Token():
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type},{repr(self.value)})'
    
    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    'PROGRAM':Token('PROGRAM','PROGRAM'),
    'VAR':Token('VAR','VAR'),
    'DIV':Token('INTEGER_DIV','DIV'),
    'INTEGER':Token('INTEGER','INTEGER'),
    'REAL':Token('REAL','REAL'),
    'BEGIN':Token('BEGIN','BEGIN'),
    'END':Token('END','END'),
    'PROCEDURE':Token('PROCEDURE','PROCEDURE')
    }
class Lexer():
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Lexer error')
    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def advance(self):
        self.pos+=1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result+=self.current_char.upper()
            self.advance()
        token = RESERVED_KEYWORDS.get(result,Token(ID,result))
        return token

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        if self.current_char == '.':
            result+=self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result+=self.current_char
                self.advance()
            token = Token('REAL_CONST',float(result))
        else:
            token = Token('INTEGER_CONST',int(result))
        return token

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        else:
            return self.text[peek_pos]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char == '{':
                self.skip_comment()
                continue
            elif self.current_char.isdigit():
                return self.number()
            elif self.current_char.isalpha():
                return self._id()
            elif self.current_char == ':' :
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(ASSIGN,':=')
                self.advance()
                return Token(COLON,':')
            elif self.current_char == ';':
                self.advance()
                return Token(SEMI,';')
            elif self.current_char == ',':
                self.advance()
                return Token(COMMA,',')
            elif self.current_char == '.':
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
                return Token(FLOAT_DIV, '/')
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

class Program(AST):
    def __init__(self,proc_name,block_node):
        self.proc_name = proc_name
        self.block = block_node
class ProcedureDecl(AST):
    def __init__(self,proc_name,params,block_name):
        self.proc_name = proc_name
        self.params = params
        self.block_name = block_name
class Block(AST):
    def __init__(self,declarations,compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self,var_node,type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value
class Compound(AST):
    def __init__(self):
        self.child = []

class Assign(AST):
    def __init__(self, left,op,right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class UnaryOp(AST):
    def __init__(self,op,expr):
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    def __init__(self, left,op,right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Param(AST):
    def __init__(self,var_node,type_node):
        self.var_node = var_node
        self.type_node = type_node

class Symbol():
    def __init__(self,name,type=None):
        self.name = name
        self.type = type
        #self.catetory=catetory
class BuiltinTypeSymbol(Symbol):
    def __init__(self,name):
        super(BuiltinTypeSymbol,self).__init__(name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class ScopedSymbolTable():
    def __init__(self,scope_name,scope_level,enclosing_scope=None):
        self._symbols = collections.OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self._init_builtins()
    
    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))
    def __str__(self):
        #s='Symbols:{symbols}'.format(
        #    symbols=[value for value in self._symbols.values()]
        #    )
        #symtab_header='Symbol table contents'
        #lines=['\n',symtab_header,'_'*len(symtab_header)]
        #lines.extend(
        #    ('%7s: %r '%(key,value))
        #    for key,value in self._symbols.items()
        #    )
        #lines.append('\n')
        #s='\n'.join(lines)
        #return s
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n',h1,'=' * len(h1)]
        for header_name,header_value in (('Scope name',self.scope_name),
            ('Scope level',self.scope_level),
            ('Enclosing scope',
             self.enclosing_scope.scope_name if self.enclosing_scope else None)):
            lines.append('%-15s: %s' % (header_name,header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2,'-' * len(h2)])
        lines.extend(('%7s: %r' % (key,value))
            for key,value in self._symbols.items())
        lines.append('\n')   
        s = '\n'.join(lines)
        return s
    __repr__ = __str__

    def insert(self,symbol):
        print(f"Insert: {symbol.name}")
        self._symbols[symbol.name] = symbol
    def define(self,symbol):
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self,name,current_scope_only=False):
        print('Lookup: %s. (Scope name: %s)' % (name, self.scope_name))
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol
        if current_scope_only:
            return None
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

class VarSymbol(Symbol):
    def __init__(self,name,type):
        super(VarSymbol,self).__init__(name,type)

    def __str__(self):
        #return f'<{self.name}:{self.type}>'
        return f"<{self.__class__.__name__}(name='{self.name}',type='{self.type})>'"
    __repr__ = __str__

class ProcedureSymbol(Symbol):
    def __init__(self,name,params=None):
        super(ProcedureSymbol,self).__init__(name)
        self.params = params if params is not None else []

    def __str__(self):
        return '<{class_name}(name={name},parameters={params})>'.format(class_name=self.__class__.__name__,
            name=self.name,
            params=self.params)
    __repr__ = __str__
class Parser():
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self,token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token,self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token,self.factor())
            return node
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL,INTEGER_DIV,FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
            node = BinOp(left=node,op=token,right=self.factor())
        return node
    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node,op=token,right=self.term())
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node
    
    def empty(self):
        return NoOp()

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left,token,right)
        return node


    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type == ID:
            self.error()
        return results

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        for node in nodes:
            root.child.append(node)
        return root

    def program(self):
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name,block_node)
        self.eat(DOT)
        return program_node

    def type_spec(self):
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        node = Type(token)
        return node

    def variable_declaration(self):
        var_nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)
        
        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node,type_node)
            for var_node in var_nodes]
        return var_declarations

    def declarations(self):
        declarations = []
        while True:
            if self.current_token.type == VAR:
                self.eat(VAR)
                while self.current_token.type == ID:
                    var_decl = self.variable_declaration()
                    declarations.extend(var_decl)
                    self.eat(SEMI)
            elif self.current_token.type == PROCEDURE:
                self.eat(PROCEDURE)
                proc_name = self.current_token.value
                self.eat(ID)
                params = []
                if self.current_token.type == LPAREN:
                    self.eat(LPAREN)
                    params = self.formal_parameter_list()
                    self.eat(RPAREN)
                self.eat(SEMI)
                block_node = self.block()
                proc_decl = ProcedureDecl(proc_name,params,block_node)
                declarations.append(proc_decl)
                self.eat(SEMI)
            else:
                break
        return declarations

    def formal_parameters(self):
        param_nodes = []
        param_tokens = [self.current_token]
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            param_tokens.append(self.current_token)
            self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        for param_token in param_tokens:
            param_node = Param(Var(param_token),type_node)
            param_nodes.append(param_node)
        return param_nodes
    def formal_parameter_list(self):
        if not self.current_token.type == ID:
            return []
        param_nodes = self.formal_parameters()
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            param_nodes.extend(self.formal_parameters())

        return param_nodes
    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes,compound_statement_node)
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node

class NodeVistor():
    def visit(self,node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)
    def generic_visit(self,node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVistor):

    def __init__(self,tree):
        self.tree = tree
        self.GLOBAL_MEMORY = collections.OrderedDict()
    
    def visit_BinOp(self,node):        
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Num(self,node):
        return node.value

    def visit_Compound(self,node):
        for child in node.child:
            self.visit(child)

    def visit_NoOp(self,node):
        pass
    def visit_Assign(self,node):
        var_name = node.left.value
        self.GLOBAL_MEMORY[var_name] = self.visit(node.right)
    def visit_Var(self,node):
        var_name = node.value
        var = self.GLOBAL_MEMORY.get(var_name)
        if var is None:
            raise NameError(repr(var_name))
        else:
            return var

    def visit_Program(self,node):
        self.visit(node.block)
    def visit_ProcedureDecl(self,node):
        pass
    def visit_Block(self,node):
        for declaration in node.declarations:
            self.visit(declaration)
            #if type(declaration) is ProcedureDecl:
            #   continue
            #for var in declaration:
            #    self.visit(var)
        self.visit(node.compound_statement)

    def visit_VarDecl(self,node):
        pass

    def visit_Type(self,node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)


    def visit_UnaryOp(self,node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)


class SemanticAnalyzer(NodeVistor):
    def __init__(self):
        #self.symtab=ScopedSymbolTable()
        self.current_scope = None
    def visit_Block(self,node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self,node):
        print('ENTER scope:global')
        global_scope = ScopedSymbolTable(scope_name='global',
            scope_level=1,enclosing_scope=self.current_scope)
        self.current_scope = global_scope
        self.visit(node.block)
        print(global_scope)
        self.current_scope=self.current_scope.enclosing_scope
        print('LEAVE scope: global')
    def visit_Compound(self,node):
        for child in node.child:
            self.visit(child)

    def visit_NoOp(slef,node):
        pass

    def visit_VarDecl(self,node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)
        self.current_scope.insert(type_symbol)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name,type_symbol)
        #if self.symtab.lookup(var_name) is not None:
        #    raise Exception(
        #        f"Error: Duplicate identifier {var_name} found"
        #        )
        if self.current_scope.lookup(var_name,current_scope_only=True):
            raise Exception(
                f"Error: Duplicate identifier {var_name} found")
        self.current_scope.insert(var_symbol)

    def visit_Var(self,node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise  Exception(f"Error: Symbol(identifier) not found {var_name}")
    def visit_Assign(self,node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_ProcedureDecl(self,node):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.insert(proc_symbol)
        print(f"ENTER scope:{proc_name}")
        procedure_scope = ScopedSymbolTable(scope_name=proc_name,
            scope_level=self.current_scope.scope_level+1,
            enclosing_scope=self.current_scope)
        self.current_scope = procedure_scope

        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name,param_type)
            self.current_scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self.visit(node.block_name)
        print(procedure_scope)
        self.current_scope=self.current_scope.enclosing_scope
        print(f'LEAVE scope: {proc_name}')
def main():
    while True:
        try:
            text = input('spi> ')
            s = input()
            while s != '$':
                text+=s
                s = input()
        except EOFError:
            print()
            break

        if len(text.strip()):
            parser = Parser(Lexer(text))
            tree = parser.parse()
            symtab_builder = SemanticAnalyzer()
            symtab_builder.visit(tree)
            print(symtab_builder.current_scope)    
            interpreter = Interpreter(tree)
            result = interpreter.interpret()
            print(interpreter.GLOBAL_MEMORY)
if __name__ == '__main__':
    main()

