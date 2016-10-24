import re,json

class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        stop  = tokens.index(']')
        arg = tokens[1:stop]
        tokens = tokens[stop+1:]
        while (')' in tokens):
            stopin = tokens.index(')')
            for i in range(stopin):
                if tokens[i] == '(':
                    startin = i
            temple = tokens[startin + 1:stopin]
            temple = self.pass1listtodict(arg,temple,['*','/']) 
            temple = self.pass1listtodict(arg,temple,['+','-'])
            other = tokens[0:startin]
            other.append(temple[0])
            tokens = other + tokens[stopin+1:]
        tokens = self.pass1listtodict(arg,tokens,['*','/']) 
        tokens = self.pass1listtodict(arg,tokens,['+','-'])
        return tokens[0]

    def pass1listtodict(self, arg, temple, op):
        while (op[0] in temple or op[1] in temple):
            if op[0] in temple and op[1] in temple:
                point = min(temple.index(op[0]), temple.index(op[1]))
            elif op[0] in temple:
                point = temple.index(op[0])
            else:
                point = temple.index(op[1])   
            part  = {}
            part['op'] = temple[point]
            if type(temple[point - 1]) == dict:
                part['a'] = temple[point - 1]
                
            else:
                if temple[point - 1] not in arg:
                    part['a'] = {'op': 'imm', 'n': temple[point -1 ]}
                else:
                    part['a'] = {'op': 'arg', 'n': arg.index(temple[point-1])}
                    
            if type(temple[point + 1]) == dict:
                part['b'] = temple[point + 1]
                
            else:
                if temple[point + 1] not in arg:
                    part['b'] = {'op': 'imm', 'n': temple[point + 1 ]}
                else:
                    part['b'] = {'op': 'arg', 'n': arg.index(temple[point + 1])}
            some = temple[:point-1]
            some.append(part)
            temple = some + temple[point+2:]
        return temple
         
         
        
    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        cata = []
        self.reduce(ast,'a','b',cata)
        return ast

    
    def reduce(self,ast,a,b,cata):
        need = ast
        for i in cata:
            need = need[i]
        if len(need) == 2:
            while len(cata) != 0 and cata[-1] == b:
                cata.pop()
            if len(cata) != 0 :
                cata[-1] = b
                self.reduce(ast,a,b,cata)
            
        elif len(need[a]) == 2:
            if len(need[b]) == 3:
                cata.append(b)
                self.reduce(ast,a,b,cata)

            else:
                if need[a]['op'] == 'imm' and need[b]['op'] == 'imm':
                    self.merge(ast,a,b,cata)
                    if cata != 0:
                        cata.pop()
                        self.reduce(ast,a,b,cata)
                else:
                    while len(cata) != 0 and cata[-1] == b:
                        cata.pop()
                    if len(cata) != 0:
                        cata[-1] = b
                        self.reduce(ast,a,b,cata)
        else:
            cata.append(a)
            self.reduce(ast,a,b,cata)

    def merge(self,ast,a,b,cata):
        "the cata is a path of ast which point to a dict, and this time, what it point have ['a'] and ['b'] both are constant number"
        
        need = ast
        for i in cata:
            need = need[i]
        if need['op'] == '*':
            need['n']  = (need[a]['n'] * need[b]['n'])
            need['op'] = 'imm'
            del need[a]
            del need[b]

        if need['op'] == '+':
            need['n']  = (need[a]['n'] + need[b]['n'])
            need['op'] = 'imm'
            
            del need[a]
            del need[b]

        if need['op'] == '-':
            need['n']  = (need[a]['n'] - need[b]['n'])
            need['op'] = 'imm'
            del need[a]
            del need[b]

        if need['op'] == '/':
            need['n']  = (need[a]['n'] / need[b]['n'])
            need['op'] = 'imm'
            del need[a]
            del need[b]

    def pass3(self, ast):
        """Returns assembly instructions,path contain the path which represent by such as['a','b','a'],
           op contain operator like['+','-','*','/'],result contain all command such as ['AR','AD']
            """
        path = []
        op   = []  
        result = []
        return self.construct(ast, 'a', 'b', path, op, result)
                              

    def construct(self, ast, a, b, path, op, result):
        if len(path) == 0 and len(result) != 0:
            return result   
        need = ast
        for i in path:
            need = need[i]
        
            
        if len(need) == 2:
            
            if len(path) != 0 and path[-1] == b:
                if len(result) != 0 and result[-1] == a:
                    result.pop()
                result.append('SW')
                if need['op'] == 'imm':
                    step = 'IM ' + str(need['n'])
                else:
                    step = 'AR ' + str(need['n'])
                result.append(step)
                if op[-1] == '-' or op[-1] == '/':
                    result.append('SW')
                self.operator(op,  path, result)
                while len(path) != 0 and path[-1] == b:
                    result.append('SW')
                    result.append('PO')
                    self.operator(op, path, result)
                    

                if len(path) == 0:
                    return result
                else:
                    result.append(a)
                    path[-1] = b
                    return self.construct(ast, a, b, path, op, result)
            else:
                if len(result) != 0 and result[-1] == a:
                    result.pop()
                    result.append('PU')
                if need['op'] == 'imm':
                    step = 'IM ' + str(need['n'])
                else:
                    step = 'AR ' + str(need['n'])
                result.append(step)
                result.append(a)
                path[-1] = b
                return self.construct(ast, a, b, path, op, result)           
        else:
            path.append(a)
            op.append(need['op'])
            return self.construct(ast, a, b, path,op, result)

    def operator(self, op, path, result):
        
        "path is the map and it point to the place where we can do some op */+-,and result is contain all the command till now"
        if op[-1] == '*':
            result.append('MU')
        if op[-1] == '+':
            result.append('AD')
        if op[-1] == '/':
            result.append('DI')
        if op[-1] == '-':
            result.append('SU')
        op.pop()
        path.pop()
                        
        
##print(Compiler().compile('[ a b c ] ( a + b + 5 + 5*6) * ( b + c )*(2+ 4+6+6+7 * 9)'))

print(Compiler().compile('[ x y z ] x - y - (z + 10 / 5 / 2 - 7 ) * 1 / 7'))
    
##test.assert_equals(Compiler().compile('[ a b c ] ( a + b + 5 + 5*6) * ( b + c )*(2+ 4+6+6+7 * 9)'),
##                   ['AR 0', 'SW', 'AR 1', 'AD', 'SW', 'IM 5', 'AD', 'SW', 'IM 30', 'AD', 'PU', 'AR 1', 'SW', 'AR 2', 'AD', 'SW', 'PO', 'AR 2', 'MU', 'SW', 'IM 81', 'MU'])
