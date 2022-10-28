## Installation / Local Setup
1) Clone the repository ``git clone https://github.com/MujyKun/basic2dengine.git``
2) Go to the repo directory ``cd basic2dengine``
3) Running with Python ^3.9 is recommended. 
4) Install requirements with either 
   1) ``pip install -r requirements.txt`` 
      1) If you do not have pip, you can install it with ``python get-pip.py`` or ``python -m ensurepip --upgrade``
   2) If you have poetry you can use ``poetry install``. 
5) Start the program with `python run.py`

## Example Game
The game can be found in [brickbreaker.py](brickbreaker.py). 
Here are a few things to note:
* The floor will kill the ball.
* Use the spacebar key to spawn new balls.
* The amount of bricks/tiles are decided based on the screen resolution.
* You can use the Left or Right keyboard arrow key to move the platform respectively.


Here is a gif of an example run:
![Brick Breaker](example_gifs/brick_breaker.gif)
This example run may appear a bit slow because of the recording software, but also the game was rendered at 1080p.
It is a lot smoother at 720p which is now the default on run..

## Collision Tests
There are tests for collisions in [test.py](test.py) that could be run. Canceling out of one screen will open another.  
Here is a gif of an example run:
![Collision Tests](example_gifs/test_collisions.gif)
