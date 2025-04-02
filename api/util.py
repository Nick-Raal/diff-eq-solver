from sympy import *
from sympy.abc import x, t
from sympy.parsing.mathematica import parse_mathematica

import matplotlib.pyplot as plt
import io
import base64

def plot_equation(eq, x_range=(-10, 10)):
    try:
        f = lambdify(x, eq, 'numpy')  # Converts SymPy expression to a numpy-compatible function

        # Generate x values for plotting
        import numpy as np
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        y_vals = f(x_vals)  # Get corresponding y values for the plot

        # Create the plot with matplotlib
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=str(eq))
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f"Plot of the particular solution")
        ax.set_axis_on()

        # Save the plot to a buffer in PNG format
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")  # Save plot to buffer (Matplotlib figure)
        buf.seek(0)

        # Convert buffer content to base64
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        # Return the base64 string for embedding in HTML
        return f"data:image/png;base64,{image_base64}"
    except Exception as e:
        print(f"Error: {e}")
        return "err"
    
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

