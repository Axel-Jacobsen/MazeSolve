# Maze Solver

This is my attempt at a maze solving program, heavily inspired by [this video](https://www.youtube.com/watch?v=rop0W4QDOUI&t=24s). I will be working on and improving this at my leisure. If you have questions or comments, go right ahead!

Mazes are fetched from [here](http://hereandabove.com/maze/mazeorig.form.html), but any maze that follows these parameters should work:
  1. The maze should be a PNG that is only black and white (RGB 0,0,0 or 255,255,255 respectively)
  2. The walls of the maze are black, the path is white
  3. Both the walls and paths of the maze are 1 pixel wide
  4. The maze is surrounded by a black wall with 2 pixels of it white, signifying the start and end of the maze
  5. You may have a 1 pixel wide border around the black wall of the maze. The program assumes this and automatically crops the image. If your maze does not need to be cropped, use `python solveMaze -c False`

  ---

To get the performance of the program: `python -m cProfile solveMaze.py`
