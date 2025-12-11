import sys

class Scanner:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.source = f.read()
        self.tokens = []
        self.pos = 0

    def scan(self):
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            
            # Skip spaces & tabs
            if ch in ' \t\n':
                self.pos += 1
                continue
            
            # Comments
            if ch == '/' and self.pos + 1 < len(self.source):
                nxt = self.source[self.pos + 1]
                # Single-line comment
                if nxt == '/':
                    comment = '//'
                    self.pos += 2
                    while self.pos < len(self.source) and self.source[self.pos] != '\n':
                        comment += self.source[self.pos]
                        self.pos += 1
                    self.tokens.append(('COMMENT', comment))
                    continue
                # Multi-line comment
                elif nxt == '*':
                    comment = '/*'
                    self.pos += 2
                    while self.pos < len(self.source) - 1:
                        comment += self.source[self.pos]
                        if self.source[self.pos] == '*' and self.source[self.pos + 1] == '/':
                            comment += '/'
                            self.pos += 2
                            break
                        self.pos += 1
                    self.tokens.append(('COMMENT', comment))
                    continue
            
            # Numbers
            if ch.isdigit() or (ch == '.' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
                num = ch
                self.pos += 1
                while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] in '.eE+-'):
                    num += self.source[self.pos]
                    self.pos += 1
                self.tokens.append(('NUMERIC_CONSTANT', num))
                continue
            
            # Identifiers & Keywords
            if ch.isalpha() or ch == '_':
                word = ch
                self.pos += 1
                while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                    word += self.source[self.pos]
                    self.pos += 1
                token_type = 'KEYWORD' if word in {'int', 'return', 'if', 'else', 'while', 'for', 'void', 'float', 'main'} else 'IDENTIFIER'
                self.tokens.append((token_type, word))
                continue
            
            # Operators
            operators = {'==', '!=', '<=', '>=', '++', '--', '+=', '-=', '*=', '/='}
            if self.pos + 1 < len(self.source):
                two_char = ch + self.source[self.pos + 1]
                if two_char in operators:
                    self.tokens.append(('OPERATOR', two_char))
                    self.pos += 2
                    continue
            
            if ch in '+-*/=<>!&|':
                self.tokens.append(('OPERATOR', ch))
                self.pos += 1
                continue
            
            # Special Characters
            if ch in '(){}[];,':
                self.tokens.append(('SPECIAL_CHARACTER', ch))
                self.pos += 1
                continue
            
            self.pos += 1  # skip unknown characters
        
        return self.tokens

    def print_to_file(self, output_file):
        with open(output_file, 'w') as f:
            f.write(f"{'#':<4} {'TYPE':<20} {'VALUE'}\n")
            f.write("=" * 50 + "\n")
            
            for idx, (t, v) in enumerate(self.tokens, 1):
                f.write(f"{idx:<4} {t:<20} {v}\n")
            
            f.write("=" * 50 + "\n")
            f.write(f"Total tokens: {len(self.tokens)}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <file.c>")
        return
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.c', '_tokens.txt')
    
    scanner = Scanner(input_file)
    scanner.scan()
    scanner.print_to_file(output_file)
    print(f"Tokens saved to: {output_file}")

if __name__ == "__main__":
    main()
