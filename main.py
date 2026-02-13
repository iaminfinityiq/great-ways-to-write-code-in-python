# tyler's typescript series

from enum import Enum, auto
from typing import Self

class Position:
	def __init__(
		self,
		idx: int,
		col: int,
		line: int
	) -> None:
		self.idx = idx
		self.col = col
		self.line = line
	
	def advance(
		self,
		current_char: str
	) -> Self:
		self.idx += 1
		if current_char == "\n":
			self.line += 1
			self.col = 1
		else:
			self.col += 1
	
	def copy(self) -> Self:
		return Position(
			self.idx,
			self.col,
			self.line
		)

class Context:
	def __init__(
		self,
		fn: str,
		lines: list[str],
		parent: Self | None,
		pos_start: Position,
		pos_end: Position
	) -> None:
		self.fn = fn
		self.lines = lines
		self.parent = parent
		self.pos_start = pos_start
		self.pos_end = pos_end
	
	def __repr__(self) -> str:
		if self.parent:
			start = f"{self.parent}\n\nAt line {self.pos_start.line} in {self.fn}:\n\n"
		else:
			start = f"Traceback (most recent called last):\n\nAt line {self.pos_start.line} in {self.fn}:\n\n"
		
		if self.pos_start.line == self.pos_end.line:
			start += f"{self.pos_start.line} || {self.lines[self.pos_start.line-1]}\n"
			for i in range(1, self.pos_start.col+len(str(self.pos_start.line)) + 4):
				start += " "
			
			for i in range(self.pos_start.col, self.pos_end.col):
				start += "^"
		else:
			max_digits = len(str(self.pos_end.line))
			for i in range(self.pos_start.line, self.pos_end.line+1):
				digits = len(str(i))
				for j in range(digits, max_digits):
					start += " "
				
				start += f"{i} || {self.lines[i-1]}\n"
				for j in range(max_digits+4):
					start += " "
				
				if i == self.pos_start.line:
					for j in range(1, self.pos_start.col):
						start += " "
					
					for j in range(self.pos_start.col, len(self.lines[i-1])+1):
						start += "^"
					
					start += "\n"
				elif i == self.pos_end.line:
					for j in range(self.pos_end.col):
						start += "^"
					
					break
				else:
					for j in range(len(self.lines[i-1])):
						start += "^"
					
					start += "\n"
		
		return start	

class Error:
	def __init__(
		self,
		error_type: str,
		details: str,
		context: Context
	) -> None:
		self.error_type = error_type
		self.details = details
		self.context = context
	
	def __repr__(self) -> str:
		return f"{self.context}\n\n{self.error_type}: {self.details}"

class Syntax(Error):
	def __init__(
		self,
		details: str,
		context: Context
	) -> None:
		super().__init__(
			"Syntax Error",
			details,
			context
		)

class Operator(Error):
	def __init__(
		self,
		details: str,
		context: Context
	) -> None:
		super().__init__(
			"Operator Error",
			details,
			context
		)

class UnfinishedInterpreter(Error):
	def __init__(
		self,
		details: str,
		context: Context
	) -> None:
		super().__init__(
			"Unfinished Interpreter Error",
			details,
			context
		)

class Math(Error):
	def __init__(
		self,
		details: str,
		context: Context
	) -> None:
		super().__init__(
			"Math Error",
			details,
			context
		)

class Variable(Error):
	def __init__(
		self,
		details: str,
		context: Context
	) -> None:
		super().__init__(
			"Variable Error",
			details,
			context
		)

class TokenType(Enum):
	EOF = auto()
	SEMICOLON = auto()
	PLUS = auto()
	MINUS = auto()
	MULTIPLY = auto()
	DIVIDE = auto()
	LPAREN = auto()
	RPAREN = auto()
	EQUALS = auto()
	INT = auto()
	FLOAT = auto()
	IDENTIFIER = auto()
	LET = auto()
	CONST = auto()

class Token:
	def __init__(
		self,
		type: TokenType,
		value: str,
		context: Context
	) -> None:
		self.type = type
		self.value = value
		self.context = context
	
	def __repr__(self) -> str:
		return f"({self.type} {self.value})"
	
	def copy(self) -> Self:
		return Token(
			self.type,
			self.value,
			self.context
		)

class LexerResult:
	def __init__(
		self,
		result: list[Token],
		error: Error | None
	) -> None:
		self.result = result
		self.error = error

class Lexer:
	def __init__(
		self,
		fn: str,
		src: str
	) -> None:
		self.fn = fn
		self.src = src
		self.lines = []
		line = ""
		for char in self.src:
			if char == "\n":
				self.lines += [line]
				line = ""
			else:
				line += char
		
		if line != "":
			self.lines += [line]
			
		self.pos = Position(
			-1,
			0,
			1
		)
		self.current_char = None
		self.advance()
	
	def advance(self) -> None:
		self.pos.advance(self.current_char)
		self.current_char = self.src[self.pos.idx] if 0 <= self.pos.idx < len(self.src) else None
	
	def make_context(
		self,
		pos_start: Position,
		pos_end: Position
	) -> Context:
		return Context(
			self.fn,
			self.lines,
			None,
			pos_start,
			pos_end
		)
	
	def tokenize(self) -> LexerResult:
		tokens = []
		KEYWORDS = {
			"let": TokenType.LET,
			"const": TokenType.CONST
		}
		while self.current_char != None:
			if self.current_char in " \t\n":
				self.advance()
				continue
			
			if self.current_char == ";":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.SEMICOLON,
					";",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
						
			if self.current_char == "+":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.PLUS,
					"+",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char == "-":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.MINUS,
					"-",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char == "*":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.MULTIPLY,
					"*",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char == "/":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.DIVIDE,
					"/",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char == "(":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.LPAREN,
					"(",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char == ")":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.RPAREN,
					")",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char == "=":
				pos_start = self.pos.copy()
				self.advance()
				
				tokens += [Token(
					TokenType.EQUALS,
					")",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				
				continue
			
			if self.current_char in "0123456789.":
				number = ""
				dot = False
				pos_start = self.pos.copy()
				while self.current_char != None and self.current_char in "0123456789.":
					if self.current_char == ".":
						if dot:
							break
						
						dot = True
					
					number += self.current_char
					self.advance()
				
				if dot:
					if number == ".":
						return LexerResult(
							[],
							Syntax(
								"standalone decimal point",
								self.make_context(
									pos_start,
									self.pos.copy()
								)
							)
						)
					
					tokens += [Token(
						TokenType.FLOAT,
						number,
						self.make_context(
							pos_start,
							self.pos.copy()
						)
					)]
				else:
					tokens += [Token(
						TokenType.INT,
						number,
						self.make_context(
							pos_start,
							self.pos.copy()
						)
					)]
				
				continue
			
			if self.current_char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_":
				identifier = ""
				pos_start = self.pos.copy()
				while self.current_char != None and self.current_char in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_":
					identifier += self.current_char
					self.advance()
				
				if identifier in KEYWORDS:
					tokens += [Token(
						KEYWORDS[identifier],
						identifier,
						self.make_context(
							pos_start,
							self.pos.copy()
						)
					)]
					continue
				
				tokens += [Token(
					TokenType.IDENTIFIER,
					identifier,
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)]
				continue
						
			pos_start = self.pos.copy()
			char = self.current_char
			self.advance()
			return LexerResult(
				[],
				Syntax(
					f"invalid character: '{char}'",
					self.make_context(
						pos_start,
						self.pos.copy()
					)
				)
			)
		
		return LexerResult(
			tokens + [Token(
				TokenType.EOF,
				"EOF",
				self.make_context(
					self.pos.copy(),
					self.pos.copy()
				)
			)],
			None
		)

class NodeType(Enum):
	PROGRAM = auto()
	VARIABLE_DECLARATION = auto()
	BINARY = auto()
	UNARY = auto()
	INT = auto()
	FLOAT = auto()
	IDENTIFIER = auto()
	PAREN = auto()

class Statement:
	def __init__(
		self,
		type: NodeType,
		context: Context
	) -> None:
		self.type = type
		self.context = context

class Expression(Statement):
	def __init__(
		self,
		type: NodeType,
		context: Context
	) -> None:
		super().__init__(
			type,
			context
		)

class Program(Statement):
	def __init__(
		self,
		fn: str,
		lines: list[str],
		start_token: Token,
		end_token: Token,
		body: list[Statement]
	) -> None:
		super().__init__(
			NodeType.PROGRAM,
			Context(
				fn,
				lines,
				None,
				start_token.context.pos_start,
				end_token.context.pos_end
			)
		)
		self.body = body
	
	def __repr__(self) -> str:
		repr = "{\n"
		for i, stmt in enumerate(self.body):
			repr += f"{i+1} || {stmt}\n"
		
		return repr + "}"

class VariableDeclaration(Statement):
	def __init__(
		self,
		start_token: Token,
		variable_name: str,
		value: Expression
	) -> None:
		super().__init__(
			NodeType.VARIABLE_DECLARATION,
			Context(
				start_token.context.fn,
				start_token.context.lines,
				None,
				start_token.context.pos_start,
				value.context.pos_end
			)
		)
		self.constant = start_token.type == TokenType.CONST
		self.variable_name = variable_name
		self.value = value
	
	def __repr__(self) -> str:
		return f"{'const' if self.constant else 'let'} {self.variable_name} = {self.value}"

class Binary(Expression):
	def __init__(
		self,
		lhs: Expression,
		op: Token,
		rhs: Expression
	) -> None:
		super().__init__(
			NodeType.BINARY,
			Context(
				lhs.context.fn,
				lhs.context.lines,
				None,
				lhs.context.pos_start,
				rhs.context.pos_end
			)
		)
		self.lhs = lhs
		self.op = op.value
		self.rhs = rhs
	
	def __repr__(self) -> str:
		return f"({self.lhs} {self.op} {self.rhs})"

class Unary(Expression):
	def __init__(
		self,
		op: Token,
		value: Expression
	) -> None:
		super().__init__(
			NodeType.UNARY,
			Context(
				op.context.fn,
				op.context.lines,
				None,
				op.context.pos_start,
				value.context.pos_end
			)
		)
		self.op = op.value
		self.value = value
		
	def __repr__(self) -> str:
		return f"({self.op}{self.value})"

class IntLiteral(Expression):
	def __init__(
		self,
		value: Token
	) -> None:
		super().__init__(
			NodeType.INT,
			value.context
		)
		self.value = int(value.value)
	
	def __repr__(self) -> str:
		return str(self.value)

class FloatLiteral(Expression):
	def __init__(
		self,
		value: Token
	) -> None:
		super().__init__(
			NodeType.FLOAT,
			value.context
		)
		self.value = float(value.value)
	
	def __repr__(self) -> str:
		return str(self.value)

class Identifier(Expression):
	def __init__(
		self,
		symbol: Token
	) -> None:
		super().__init__(
			NodeType.IDENTIFIER,
			symbol.context
		)
		self.symbol = symbol.value
	
	def __repr__(self) -> str:
		return self.symbol

class Paren(Expression):
	def __init__(
		self,
		lparen: Token,
		expr: Expression,
		rparen: Token
	) -> None:
		super().__init__(
			NodeType.PAREN,
			Context(
				lparen.context.fn,
				lparen.context.lines,
				None,
				lparen.context.pos_start,
				rparen.context.pos_end
			)
		)
		self.expr = expr
	
	def __repr__(self) -> str:
		return f"{self.expr}"

class ParserResult:
	def __init__(
		self,
		result: Statement | None,
		error: Error | None
	) -> None:
		self.result = result
		self.error = error

class Parser:
	def __init__(
		self,
		tokens: list[Token]
	) -> None:
		self.tokens = tokens
		self.idx = -1
		self.advance()
	
	def advance(self) -> None:
		self.idx += 1
		self.current_token = self.tokens[self.idx] if 0 <= self.idx < len(self.tokens) else None
	
	def parse(self) -> ParserResult:
		body = []
		while self.current_token.type not in (TokenType.EOF, None):
			stmt = self.statement()
			if stmt.error:
				return stmt
			
			body += [stmt.result]
		
		return ParserResult(
			Program(
				self.tokens[0].context.fn,
				self.tokens[0].context.lines,
				self.tokens[0],
				self.tokens[-1],
				body
			),
			None
		)
	
	def statement(self) -> ParserResult:
		if self.current_token.type in (TokenType.LET, TokenType.CONST):
			return self.variable_declaration()
		
		return self.expression()
	
	def variable_declaration(self) -> ParserResult:
		start_token = self.current_token.copy()
		self.advance()
		
		if self.current_token.type != TokenType.IDENTIFIER:
			return ParserResult(
				None,
				Syntax(
					"expected variable name in variable declarations",
					self.current_token.context
				)
			)
		
		variable_name = self.current_token.value
		self.advance()
		
		if self.current_token.type == TokenType.SEMICOLON:
			semicolon_context = self.current_token.context
			self.advance()
			return ParserResult(
				VariableDeclaration(
					start_token,
					variable_name,
					Identifier(
						"null",
						semicolon_context
					)
				),
				None
			)
		
		if self.current_token.type != TokenType.EQUALS:
			return ParserResult(
				None,
				Syntax(
					"expected '=' in variable declaration",
					self.current_token.context
				)
			)
		
		self.advance()
		
		value = self.expression()
		if value.error:
			return value
		
		if self.current_token.type != TokenType.SEMICOLON:
			return ParserResult(
				None,
				Syntax(
					"expected ';'",
					self.current_token.context
				)
			)
		
		self.advance()
		return ParserResult(
			VariableDeclaration(
				start_token,
				variable_name,
				value.result
			),
			None
		)
	
	def expression(self) -> ParserResult:
		return self.additive()
	
	def additive(self) -> ParserResult:
		lhs = self.multiplicative()
		if lhs.error:
			return lhs
		
		while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
			op = self.current_token.copy()
			self.advance()
			
			rhs = self.multiplicative()
			if rhs.error:
				return rhs
			
			lhs.result = Binary(
				lhs.result,
				op,
				rhs.result
			)
		
		return lhs
	
	def multiplicative(self) -> ParserResult:
		lhs = self.unary()
		if lhs.error:
			return lhs
		
		while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
			op = self.current_token.copy()
			self.advance()
			
			rhs = self.unary()
			if rhs.error:
				return rhs
			
			lhs.result = Binary(
				lhs.result,
				op,
				rhs.result
			)
		
		return lhs
	
	def unary(self) -> ParserResult:
		if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
			op = self.current_token.copy()
			self.advance()
			
			value = self.unary()
			if value.error:
				return value
			
			return ParserResult(
				Unary(
					op,
					value.result
				),
				None
			)
		
		return self.primary()
	
	def primary(self) -> ParserResult:
		if self.current_token.type == TokenType.INT:
			token = self.current_token.copy()
			self.advance()
			
			return ParserResult(
				IntLiteral(
					token
				),
				None
			)
		
		if self.current_token.type == TokenType.FLOAT:
			token = self.current_token.copy()
			self.advance()
			
			return ParserResult(
				FloatLiteral(
					token
				),
				None
			)
		
		if self.current_token.type == TokenType.IDENTIFIER:
			token = self.current_token.copy()
			self.advance()
			
			return ParserResult(
				Identifier(
					token
				),
				None
			)
		
		if self.current_token.type == TokenType.LPAREN:
			lparen = self.current_token.copy()
			self.advance()
			
			expr = self.expression()
			if expr.error:
				return expr
			
			if self.current_token.type != TokenType.RPAREN:
				return ParserResult(
					None,
					Syntax(
						"expected ')' after '('",
						self.current_token.context
					)
				)
			
			rparen = self.current_token.copy()
			self.advance()
			
			return ParserResult(
				Paren(
					lparen,
					expr.result,
					rparen
				),
				None
			)
		
		if self.current_token.type == TokenType.RPAREN:
			return ParserResult(
				None,
				Syntax(
					"unmatched ')'",
					self.current_token.context
				)
			)
		
		return ParserResult(
			None,
			Syntax(
				"invalid syntax!",
				self.current_token.context
			)
		)

class InterpreterResult:
	pass

class RuntimeValue:
	def __init__(
		self,
		data_type: str,
		context: Context
	) -> None:
		self.data_type = data_type
		self.context = context
	
	def add(
		self,
		other: Self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '+' on '{self.data_type}' and '{other.data_type}'",
				context
			)
		)
	
	def sub(
		self,
		other: Self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '-' on '{self.data_type}' and '{other.data_type}'",
				context
			)
		)
	
	def mul(
		self,
		other: Self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '*' on '{self.data_type}' and '{other.data_type}'",
				context
			)
		)
	
	def div(
		self,
		other: Self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '/' on '{self.data_type}' and '{other.data_type}'",
				context
			)
		)
	
	def unary_plus(
		self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform 'unary +' on '{self.data_type}'",
				context
			)
		)
		
	def unary_minus(
		self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform 'unary -' on '{self.data_type}'",
				context
			)
		)

class Scope:
	def __init__(
		self,
		parent: Self
	) -> None:
		self.parent = parent
		self.variables = {}
		self.constants = set()
	
	def resolve(
		self,
		variable_name: str
	) -> Self | None:
		if variable_name in self.variables:
			return self
		
		if self.parent:
			return self.parent.resolve(
				variable_name
			)
		
		return None
	
	def declare(
		self,
		variable_name: str,
		value: RuntimeValue,
		constant: bool,
		context: Context
	) -> InterpreterResult:
		if variable_name in self.variables:
			return InterpreterResult(
				None,
				Variable(
					f"variable '{variable_name}' is already declared, thus can't be declared again",
					context
				)
			)
		
		self.variables[variable_name] = value
		if constant:
			self.constants.add(variable_name)
		
		return InterpreterResult(
			None,
			None
		)
	
	def assign(
		self,
		variable_name: str,
		value: RuntimeValue,
		context: Context
	) -> None:
		scope = self.resolve(
			variable_name
		)
		if not scope:
			return InterpreterResult(
				None,
				Variable(
					f"variable '{variable_name}' is not declared, thus can't be assigned",
					context
				)
			)
		
		if variable_name in scope.constants:
			return InterpreterResult(
				None,
				Variable(
					f"variable '{variable_name}' is a constant, thus can't be assigned",
					context
				)
			)
		
		scope.variables[variable_name] = value
		value.context = context
		return InterpreterResult(
			value,
			None
		)
	
	def get(
		self,
		variable_name: str,
		context: Context
	) -> InterpreterResult:
		scope = self.resolve(
			variable_name
		)
		if not scope:
			return InterpreterResult(
				None,
				Variable(
					f"variable '{variable_name}' does not exist",
					context
				)
			)
		
		result = scope.variables[variable_name]
		result.context = context
		
		return InterpreterResult(
			result,
			None
		)

class Int(RuntimeValue):
	def __init__(
		self,
		value: int,
		context: Context
	) -> None:
		super().__init__("int", context)
		self.value = value
	
	def __repr__(self) -> str:
		return str(self.value)
	
	def add(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type == "int":
			return InterpreterResult(
				Int(
					self.value + other.value,
					context
				),
				None
			)
		
		if other.data_type == "float":
			return InterpreterResult(
				Float(
					self.value + other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '+' on 'int' and '{other.data_type}'",
				context
			)
		)

	def sub(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type == "int":
			return InterpreterResult(
				Int(
					self.value - other.value,
					context
				),
				None
			)
		
		if other.data_type == "float":
			return InterpreterResult(
				Float(
					self.value - other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '-' on 'int' and '{other.data_type}'",
				context
			)
		)

	def mul(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type == "int":
			return InterpreterResult(
				Int(
					self.value * other.value,
					context
				),
				None
			)
		
		if other.data_type == "float":
			return InterpreterResult(
				Float(
					self.value * other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '*' on 'int' and '{other.data_type}'",
				context
			)
		)

	def div(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type == "int":
			if other.value == 0:
				return InterpreterResult(
					None,
					Math(
						"someone here does not know that they can't divide by 0",
						Context(
							self.context.fn,
							self.context.lines,
							self.context.parent,
							self.context.pos_start,
							other.context.pos_end
						)
					)
				)
			
			return InterpreterResult(
				Int(
					self.value // other.value,
					context
				),
				None
			)
		
		if other.data_type == "float":
			if other.value == 0:
				return InterpreterResult(
					None,
					Math(
						"someone here does not know that they can't divide by 0",
						context
					)
				)
			
			return InterpreterResult(
				Float(
					self.value / other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '/' on 'int' and '{other.data_type}'",
				context
			)
		)
	
	def unary_plus(
		self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			Int(
				self.value,
				context
			),
			None
		)
	
	def unary_minus(
		self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			Int(
				-self.value,
				context
			),
			None
		)

class Float(RuntimeValue):
	def __init__(
		self,
		value: float,
		context: Context
	) -> None:
		super().__init__("float", context)
		self.value = value
	
	def __repr__(self) -> str:
		return str(self.value)
	
	def add(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type in ("int", "float"):
			return InterpreterResult(
				Float(
					self.value + other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '+' on 'float' and '{other.data_type}'",
				context
			)
		)
	
	def sub(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type in ("int", "float"):
			return InterpreterResult(
				Float(
					self.value - other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '-' on 'float' and '{other.data_type}'",
				context
			)
		)
	
	def mul(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type in ("int", "float"):
			return InterpreterResult(
				Float(
					self.value * other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '*' on 'float' and '{other.data_type}'",
				context
			)
		)
	
	def div(
		self,
		other: RuntimeValue,
		context: Context
	) -> InterpreterResult:
		if other.data_type in ("int", "float"):
			if other.value == 0:
				return InterpreterResult(
					None,
					Math(
						"someone here does not know that they can't divide by 0",
						context
					)
				)
			
			return InterpreterResult(
				Float(
					self.value / other.value,
					context
				),
				None
			)
		
		return InterpreterResult(
			None,
			Operator(
				f"cannot perform '/' on 'float' and '{other.data_type}'",
				context
			)
		)
	
	def unary_plus(
		self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			Float(
				self.value,
				context
			),
			None
		)
	
	def unary_minus(
		self,
		context: Context
	) -> InterpreterResult:
		return InterpreterResult(
			Float(
				-self.value,
				context
			),
			None
		)

class Null(RuntimeValue):
	def __init__(
		self,
		context: Context
	) -> None:
		super().__init__("null_type", context)
	
	def __repr__(self) -> str:
		return "NULL"

class Boolean(RuntimeValue):
	def __init__(
		self,
		value: bool,
		context: Context
	) -> None:
		super().__init__("boolean", context)
		self.value = value
	
	def __repr__(self) -> str:
		return "TRUE" if self.value else "FALSE"

class InterpreterResult:
	def __init__(
		self,
		result: RuntimeValue | None,
		error: Error | None
	) -> None:
		self.result = result
		self.error = error

class Interpreter:
	def __init__(
		self,
		ast: Program,
		global_scope: Scope
	) -> None:
		self.ast = ast
		self.global_scope = global_scope
	
	def run(self) -> InterpreterResult:
		return self.evaluate(
			self.ast,
			self.global_scope
		)
	
	def evaluate(
		self,
		node: Statement,
		scope: Scope
	) -> InterpreterResult:
		if node.type == NodeType.PROGRAM:
			for stmt in node.body:
				result = self.evaluate(
					stmt,
					scope
				)
				
				if result.error:
					return result
				
				if result.result:
					print(result.result)
			
			return InterpreterResult(
				None,
				None
			)
		
		if node.type == NodeType.VARIABLE_DECLARATION:
			value = self.evaluate(
				node.value,
				scope
			)
			if value.error:
				return value
			
			return scope.declare(
				node.variable_name,
				value.result,
				node.constant,
				node.context
			)
		
		if node.type == NodeType.BINARY:
			lhs = self.evaluate(
				node.lhs,
				scope
			)
			
			if lhs.error:
				return lhs
			
			rhs = self.evaluate(
				node.rhs,
				scope
			)
			
			if rhs.error:
				return rhs
				
			if node.op == "+":
				return lhs.result.add(rhs.result, node.context)
			
			if node.op == "-":
				return lhs.result.sub(rhs.result, node.context)
			
			if node.op == "*":
				return lhs.result.mul(rhs.result, node.context)
			
			if node.op == "/":
				return lhs.result.div(rhs.result, node.context)
			
			return InterpreterResult(
				None,
				Operator(
					f"unexpected operator: '{node.op}'",
					node.context
				)	
			)
		
		if node.type == NodeType.INT:
			return InterpreterResult(
				Int(
					node.value,
					node.context
				),
				None
			)
		
		if node.type == NodeType.FLOAT:
			return InterpreterResult(
				Float(
					node.value,
					node.context
				),
				None
			)
		
		if node.type == NodeType.PAREN:
			result = self.evaluate(
				node.expr,
				scope
			)
			
			if result.error:
				return result
			
			result.result.context = node.context
			return result
		
		if node.type == NodeType.UNARY:
			value = self.evaluate(
				node.value,
				scope
			)
			
			if value.error:
				return value
			
			if node.op == "+":
				return value.result.unary_plus(node.context)
			
			if node.op == "-":
				return value.result.unary_minus(node.context)
			
			return InterpreterResult(
				None,
				Operator(
					f"unexpected operator: 'unary {node.op}'",
					node.context
				)	
			)
		
		if node.type == NodeType.IDENTIFIER:
			return scope.get(
				node.symbol,
				node.context
			)
		
		return InterpreterResult(
			None,
			UnfinishedInterpreter(
				f"unexpected node type: {node.type}",
				node.context
			)
		)

print("""----------------------------
| tyler's language, a REPL |
----------------------------
""")

dummy_context = Context(
	"",
	[],
	None,
	0,
	0
)
global_scope = Scope(
	None
)
global_scope.declare(
	"true",
	Boolean(
		True,
		dummy_context
	),
	True,
	dummy_context
)
global_scope.declare(
	"false",
	Boolean(
		False,
		dummy_context
	),
	True,
	dummy_context
)
global_scope.declare(
	"null",
	Null(
		dummy_context
	),
	True,
	dummy_context
)
while True:
	code = input("repl > ")
	
	lexer = Lexer("<stdin>", code)
	lr = lexer.tokenize()
	
	if lr.error:
		print(lr.error)
		continue
	
	print("\nTOKENS:")
	for i, token in enumerate(lr.result):
		print(f"{i+1} || {token}")
	
	parser = Parser(lr.result)
	pr = parser.parse()
	
	if pr.error:
		print(pr.error)
		continue
	
	print(f"\nAST:\n{pr.result}\n\nINTERPRETER:")
	
	interpreter = Interpreter(pr.result, global_scope)
	ir = interpreter.run()
	if ir.error:
		print(ir.error)
		continue
