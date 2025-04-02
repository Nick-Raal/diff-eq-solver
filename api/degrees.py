from http.server import BaseHTTPRequestHandler
import json
from sympy import Function, Eq, symbols, ode_order
from sympy.abc import x
from util import parse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            equation_str = data.get('equation', '')
            
            if not equation_str or '=' not in equation_str or 'y' not in equation_str:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid equation'}).encode())
                return

            equation = parse(equation_str)
            if isinstance(equation, str):  # If parsing failed, return the error
                raise ValueError(equation)

            y = Function('y')(x)
            degree = int(ode_order(equation.lhs, y))

            response = {'solution': degree}
            self.send_response(200)
        except Exception as e:
            response = {'error': f'Invalid equation format: {str(e)}'}
            self.send_response(400)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())