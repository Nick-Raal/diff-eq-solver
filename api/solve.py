from http.server import BaseHTTPRequestHandler
import json
from sympy import *
from sympy.abc import x
from sympy.parsing.mathematica import parse_mathematica
from util import parse, plot_equation
import traceback

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            equation_str = data.get('equation', '')

            if not equation_str or '=' not in equation_str or 'y' not in equation_str:
                raise ValueError("Invalid equation format")

            equation = parse(equation_str)
            if isinstance(equation, str):
                raise ValueError(equation)

            y = Function('y')(x)

            data["inputs"] = [x for x in data.get("inputs", []) if x]
            data["inputs1"] = [x for x in data.get("inputs1", []) if x]

            init = [sympify(num) for num in data["inputs"]]
            init1 = [sympify(num) for num in data["inputs1"]]

            eqsol = dsolve(equation, y)
            solution = eqsol.rhs

            sys = [Eq(solution.diff(x, i).subs(x, init[i]), init1[i]) for i in range(len(init))]
            sys1 = [symbols(f"C{i+1}") for i in range(len(init))]

            constants = solve(sys, sys1)
            particular_solution = solution.subs(constants)

            graph_image = plot_equation(particular_solution)

            response = {
                'solution': str(particular_solution),
                'image': graph_image if graph_image else "No valid plot generated"
            }
            self.send_response(200)
        except Exception as e:
            traceback.print_exc()
            response = {'error': str(e)}
            self.send_response(400)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())