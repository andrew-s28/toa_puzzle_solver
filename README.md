
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

Simply download the executable in the dist folder found [here](dist) and run on your machine. The source code used for the compiling of this exectuable (compiled through [PyInstaller](https://pyinstaller.org/en/stable/index.html)) is available [here](source/toa_solver.py) and the build output from PyInstaller is available [here](build), so that you can have a little more trust running a .exe from some random person on the internet :D.

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

The puzzle in this game is adapted from a similar game called ["Lights Out"](https://en.wikipedia.org/wiki/Lights_Out_(game)), although the middle square in this case has been removed. In either case, the math remains the same. I solve this puzzle by using a solving a linear system of equations which is based on a great [WolframAlpha article by Margherita Barile](https://mathworld.wolfram.com/LightsOutPuzzle.html). The basics of how and why this works are laid out over there, so I will not be re-explaining that here. 

However, some adapting was needed. First and foremost, the lack of a center tile meant that the coefficient matrix (called _A_) had to be updated. Each 3x3 coefficient matrix (that is, how clicking each tile causes other tiles to react) was laid end-to-end and stacked on top of on another. See an example of this in the first row of _A_, where clicking the first tile changes itself, the second tile and the fourth tile (first tile in second row). Constructing this 9x9 matrix was relatively easy so I did it by hand. The other two matrices, _x_, the variable matrix, and _L_, the tile matrix, were easy to adapt by simply shortening their length by one. _L_ is defined by the initial tiles where, counting from the top left across then down, a one corresponds to an "on" tile and a zero to an "off" tile. These matrices are shown below, with _L_ using the tiles from the previous section as an example.

<p align="center">
    <img src=imgs/CodeCogsEqn1.png>
</p>

The system of equations we are interested in solving is given by _Ax=L_, which can be solved easily in the real number space with some basic numpy functionality. Each entry in the 8x1 matrix solution is the number of times needed to press each button to solve the puzzle. Unfortunately, in the real number space we get weird things like 0.33 button presses. This is because the linear algebra solution is designed to work in (0,1) integer space (see the WolframAlpha article for more details), and integer linear algebra is quite a bit harder than in the reals. 

I solved this problem by first solving the system of equations in real space before making use of some side-steps to get back to a (0,1) matrix solution which tells which buttons need to be pressed. To do this, I first turned the decimal results from the real space solution into fractions before getting their denominators. Then I brought the fractions to a common factor and multiplied through to get integer solutions. This solution will return some buttons which need to be pressed twice, that is returned to their original state. So the final step is to take mod 2 on this matrix (while also rounding to get rid of some floating-point weirdness) to get only those buttons that need to be pressed an odd number of times. 

The returned matrix will be a length 8 matrix corresponding to the buttons that need to be pressed, counting across then down from the top left first.
