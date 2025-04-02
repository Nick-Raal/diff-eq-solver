from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS for frontend requests

import traceback

from sympy import *
from sympy.abc import x, t
from sympy.parsing.mathematica import parse_mathematica

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

equation = None
@app.route('/degrees', methods=['POST'])  # Ensure POST method is allowed
def degrees():
    y = Function('y')(x)
    data = request.json
    equation_str = data.get('equation', '')

    if not equation_str:
        return jsonify({'error': 'No equation provided'}), 400  # Handle missing data
    if '=' not in equation_str:
        return jsonify({'error': 'Provided equation lacks an equality'}), 400  # Handle missing data
    if 'y' not in equation_str:
        return jsonify({'error': 'Equation must be in terms of y'}), 400
    try:
        equation = parse(equation_str) # Convert strings to SymPy equation
        deg = int(ode_order(equation.lhs, y))  # Get the degree of the left-hand side
        return jsonify({'solution': deg})  # Return JSON response
    except Exception as e:
        print(e)
        return jsonify({'error': f'Invalid equation format: {str(e)}'}), 400
    
def parse(expr):
    lhs, rhs = expr.split('=', 1)
    y = Function('y')(x)
    # Ensure correct parsing and differentiation
    lhs_expr = parse_mathematica(lhs)
    rhs_expr = parse_mathematica(rhs)
    lhs_expr = deriv_conv(lhs_expr)
    rhs_expr = deriv_conv(rhs_expr)
    return Eq(lhs_expr, rhs_expr)

def deriv_conv(expr):
    y = Function('y')(x)
    expr = str(expr) + " "
    index = expr.find("Derivative(")

    # print(expr)
    
    while index != -1:
        s = expr[index: expr.find(") ", index + 1) + 1]

        
        s1 = "1"
        if s[s.rfind("(") +1] != 'y':
            s1 = s[s.rfind("(") + 1:s.rfind("y")]
            
            s1 = parse_mathematica(s1)


        n1 = s.count(")")

        

        n = s.count("Derivative")
        
        s = "Derivative(" + str(s1) + f" * y, x, {n}"
    
        
        expr = expr[:index] + s  + expr[expr.find(")", index + 1) + n - 1:]
        
        index = expr.find("Derivative(", index + len(s))
    print(f"expr : {expr}")
    return sympify(expr).subs(symbols('y'), y)

@app.route('/solve', methods=['POST'])
def initial_condition_solver():
    data = request.json
    equation_str = data.get('equation', '')
    

    if not equation_str:
        return jsonify({'error': 'No equation provided'}), 400  # Handle missing data
    if '=' not in equation_str:
        return jsonify({'error': 'Provided equation lacks an equality'}), 400  # Handle missing data
    if 'y' not in equation_str:
        return jsonify({'error': 'Equation must be in terms of y'}), 400
    
    y = Function('y')(x)
    try:
        equation = parse(equation_str) # Create a valid SymPy equation
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {'error': f'Invalid equation format: {str(e)}'}, 422
    
    try:
        data["inputs"] = [x for x in data["inputs"] if x]  # Remove empty strings
        data["inputs1"] = [x for x in data["inputs1"] if x]  # Remove empty strings

        init = [sympify(num) for num in data["inputs"]]
        init1 = [sympify(num) for num in data["inputs1"]]
    except Exception as e:
        traceback.print_exc()
        return {'error': f'Invalid initial conditions: {str(e)}'}, 422

    
    
    print(equation)

    try:
        eqsol = dsolve(equation, y)
        solution = eqsol.rhs
    except Exception as e:
        return {'error': f'Unable to solve: {str(e)}'}, 400

    
    sys = []
    sys1 = []
    for i in range(len(init)):
        deriv = solution.diff(x, i)
        condition_eq = Eq(deriv.subs(x, init[i]), init1[i])
        sys.append(condition_eq)
        sys1.append(Symbol(f"C{i+1}"))
    constants = solve(sys, sys1)
    particular_solution = solution.subs(constants)
    return jsonify({'solution': latex(particular_solution)}) 

if __name__ == '__main__':
    app.run(debug=True, port=5328)  # Ensure port is 5328