import sys
import os

def read_tokens_from_file():
    tokens = []
    file_path ="test_tokens.txt"
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit()

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('#') or line.startswith('='):
                continue
            if line.startswith('Total'):
                break
                
            if line:
                parts = line.split(maxsplit=2)
                
                if len(parts) >= 3:
                    token_type = parts[1]
                    token_value = parts[2]
                    
                    if token_type == 'COMMENT':
                        continue
                        
                    tokens.append((token_type, token_value.strip()))
    return tokens

class Cparser:
    def __init__(self):
        self.tokens = read_tokens_from_file()
        self.current_token = 0

    def syntax_error(self, expected, found):
        token_info = found
    
        if self.current_token >= len(self.tokens):
            token_info = 'End of File (EOF)'
        elif isinstance(found, tuple):
             token_info = f"Type: {found[0]}, Value: {found[1]}"

        print(f"Syntax Error! Expected: ({expected}) but found: ({token_info}) at token index {self.current_token}")
        sys.exit()


    def match(self, *arg):
        if self.current_token >= len(self.tokens):
            return False
            
        token = self.tokens[self.current_token]
        if len(arg) == 1:
            if token[0] == arg[0]:
                self.current_token += 1
                return True
        elif len(arg) == 2:
            if token[0] == arg[0] and token[1] == arg[1]:
                self.current_token += 1
                return True
        return False

    def parse(self):
        if self.current_token >= len(self.tokens):
            return

        token = self.tokens[self.current_token]

        if token[0] == 'KEYWORD':
            if token[1] == 'int':
                if self.current_token + 1 < len(self.tokens) and self.tokens[self.current_token+1][1] == 'main':
                    self.parse_fun_declaration()
                else:
                    self.current_token += 1
                    self.parse_statment()
            
            elif token[1] == 'if':
                self.parse_if_statement()
            elif token[1] == 'return':
                self.parse_return_statement()
            
            elif token[1] == 'else':
                 return 
            
            elif token[1] in ('float', 'double', 'char'):
                self.current_token += 1 
                self.parse_statment()

        elif token[0] == 'IDENTIFIER':
            self.parse_assignment()

        elif token[0] == 'SPECIAL_CHARACTER' and token[1] == '}':
            return 
        
        else:
            self.syntax_error('KEYWORD, IDENTIFIER, or }', token)


    def parse_fun_declaration(self):
        if (self.match('KEYWORD', 'int') and 
            self.match('KEYWORD', 'main') and 
            self.match('SPECIAL_CHARACTER', '(') and 
            self.match('SPECIAL_CHARACTER', ')')):
            
            self.parse_code_block()
            return
        else:

            self.syntax_error('int main() declaration', self.tokens[self.current_token])

    def parse_statment(self):
        while True:
            if self.match('IDENTIFIER'):
                if self.match('OPERATOR', '='):
                    self.parse_expression()
                    if self.match('SPECIAL_CHARACTER', ';'):
                        return
                    else:
                        self.syntax_error(';', self.tokens[self.current_token])
                
                elif self.match('SPECIAL_CHARACTER', ','):
                    continue
                
                elif self.match('SPECIAL_CHARACTER', ';'):
                    return
                
                else:
                    self.syntax_error(', or ; or =', self.tokens[self.current_token])
            
            else:
                self.syntax_error('Identifier', self.tokens[self.current_token])


    def parse_assignment(self):
        if not self.match('IDENTIFIER'):
             self.syntax_error('Identifier', self.tokens[self.current_token])

        if self.match('OPERATOR', '='):
            self.parse_expression()
            if self.match('SPECIAL_CHARACTER', ';'):
                return
            else:
                self.syntax_error(';', self.tokens[self.current_token])
        else:
            self.syntax_error('=', self.tokens[self.current_token])

    def parse_expression(self):
        self.parse_term()

        relational_operators = ('==', '>', '<', '!=', '>=', '<=')
        
        if (self.current_token < len(self.tokens) and 
            self.tokens[self.current_token][0] == 'OPERATOR' and 
            self.tokens[self.current_token][1] in relational_operators):
            
            self.current_token += 1 
            self.parse_term() 
        
    def parse_term(self):
        if not self.parse_factor():
            self.syntax_error('Expression Factor (Number or Identifier)', self.tokens[self.current_token])
        
        while (self.current_token < len(self.tokens) and 
               self.tokens[self.current_token][0] == 'OPERATOR' and 
               (self.tokens[self.current_token][1] == '+' or self.tokens[self.current_token][1] == '-')):
            
            self.match('OPERATOR') 
            if not self.parse_factor(): 
                 self.syntax_error('Factor after operator', self.tokens[self.current_token])
    
    def parse_factor(self):
        if self.match('NUMERIC_CONSTANT'):
            return True
        elif self.match('IDENTIFIER'):
            return True
        return False

    def parse_if_statement(self):
        self.current_token += 1
        
        if self.match('SPECIAL_CHARACTER', '('):
            self.parse_expression()
            if self.match('SPECIAL_CHARACTER', ')'):
                
                self.parse_code_block() 
                
                if self.match('KEYWORD', 'else'):
                    self.parse_code_block()
                
                return
        
        self.syntax_error('if (...) structure', self.tokens[self.current_token])

    def parse_return_statement(self):
        self.current_token += 1
        
        if self.match('NUMERIC_CONSTANT') or self.match('IDENTIFIER'):
             if self.match('SPECIAL_CHARACTER', ';'):
                 return
        
        self.syntax_error('return value;', self.tokens[self.current_token])

    def parse_code_block(self):
        if self.match('SPECIAL_CHARACTER', '{'):
            while self.current_token < len(self.tokens) and self.tokens[self.current_token][1] != '}':
                self.parse()
            

            if not self.match('SPECIAL_CHARACTER', '}'):

                 found_token = None
                 if self.current_token < len(self.tokens):
                     found_token = self.tokens[self.current_token]
                 
                 self.syntax_error('}', found_token)
            
            return 
        else:
            self.syntax_error('{', self.tokens[self.current_token])

 

def main():
    parser = Cparser()
    try:
        parser.parse()
        if parser.current_token == len(parser.tokens):
            print("Parsing Completed Successfully. No Syntax Errors Found.")
        else:
             print(f"Warning: Parsing stopped early at token index {parser.current_token}. Check for unparsed tokens.")
    except SystemExit:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":

    main()
