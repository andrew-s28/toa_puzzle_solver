
<h1 align="center"><img src="imgs/Kephri_icon.ico" width="40" height="40" >&emsp;Tombs of Amascut Puzzle Solver&emsp;<img src="imgs/Kephri_icon.ico" width="40" height="40" ></h1>
<p align="center">A solver for the modified LightOut puzzle found in the Path of Scabaras within the raid.</p>

<p align="center">
    <img src=imgs/lightoutpuzzleroom.PNG>
</p>

## Disclaimer

This is a personal project used for personal needs. It is not thoroughly error tested nor is it guarenteed to work on your operating system (my personal OS is Windows 10, so this is the best bet). Use at your own risk, or make it better! 

Created using intellectual property belonging to Jagex Limited under the terms of Jagex's Fan Content Policy. This content is not endorsed by or affiliated with Jagex.

## Usage

### Installation

Simply download the executable above and run on your machine. The source code used for the compiling of this exectuable (compiled through [Auto PY to EXE](https://github.com/brentvollebregt/auto-py-to-exe)) is available [here](source/toa_solver.py)

### Solving the Puzzle

<p align="center">
    <img src=imgs/demo1.PNG>
</p>

1. Highlight the tiles that are in the tomb. Orientation does not matter, highlight however makes sense to you!
2. When the red tiles match the highlighted tiles from the raid, click solve.
3. The solution will now be highlighted in red the tiles below the solve button you need to step on to solve the puzzle. 
    - It does not matter what order you enter the solution, as the solution is commutative.  
    <p align="center">
        <img src=imgs/demo2.PNG>
    </p>
4. You can verify this by entering it in the above grid, as the top puzzle will now behave like the in-game puzzle.
5. To restart the process, simply click reset and re-do the process from above.

## The Math Behind It

<p align="center">
    <img src=imgs/lightsoutillustration.png>
</p>

The puzzle in this game is adapted from a similar game called ["Lights Out"](https://en.wikipedia.org/wiki/Lights_Out_(game)), although the middle square in this case has been removed. In either case, the math remains the same. I solve this puzzle by using a solving a linear system of equations which is based on a great [WolframAlpha article by Margherita Barile](https://mathworld.wolfram.com/LightsOutPuzzle.html). The basics of how and why this works are laid out in this work, so I will not be re-explaining that here. 

However, some adapting was needed. First and foremost, the lack of a center tile meant that the coefficient matrix had to be updated. This was relatively easy for a 9x9 matrix and I did it by hand. The resulting matrix is: 

<p align="center">
    <img src=imgs/CodeCogsEqn.png>
</p>

Then the system of equations was solved using numpy.linalg.solve. However, this function works in real space while the matrix is supposed to be a (0,1) matrix with integer only coefficients. However, integer only matrix solutions are not easy computationally. Thus, I solved the system of equations in real space before making use of some side-steps to get back to a (0,1) matrix solution which tells which buttons need to be pressed. To do this, I first turned the decimal results from the real space solution into fractions before getting their denominators. Then I brought the fractions to a common factor and multiplied through to get integer solutions. This solution will return some buttons which need to be pressed twice, that is returned to their original state. So the final step is to take mod 2 on this matrix (while also rounding to get rid of some floating-point weirdness) to get only those buttons that need to be pressed an odd number of times. 

The returned matrix will be a length 8 matrix corresponding to the buttons that need to be pressed, counting across then down from the top left first.

