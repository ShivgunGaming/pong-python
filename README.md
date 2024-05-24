# Pong Game ReadMe

## Introduction
This is a simple implementation of the classic Pong game using Pygame, a popular library for creating video games in Python. The game features two paddles and a ball, where one paddle is controlled by the player using the mouse, and the other is controlled by a basic AI.

## Requirements
- Python 3.x
- Pygame library

## Installation
To install Pygame, run:
pip install pygame

## How to Run
Save the provided code to a file, `pong.py`. Then run the game using Python:
python pong.py


## Game Controls
- The player controls the left paddle using the mouse. Move the mouse up and down to move the paddle vertically.
- The AI controls the right paddle, which automatically follows the ball's movement.

## Game Elements
- **Screen Dimensions:** 800x600 pixels.
- **Colors:** White for the paddles and ball, black for the background.
- **Paddles:** 
  - Width: 10 pixels
  - Height: 100 pixels
  - Speed: 5 pixels per frame
- **Ball:**
  - Size: 20 pixels
  - Speed: 5 pixels per frame in both X and Y directions, with random initial direction.

## Scoring
- The game keeps track of the scores for both the player and the opponent.
- If the ball passes the left edge of the screen, the opponent scores a point.
- If the ball passes the right edge of the screen, the player scores a point.
- The scores are displayed at the top of the screen.

## Code Overview
### Initialization
- `pygame.init()`: Initializes the Pygame library.
- Screen is set up with dimensions 800x600.
- Paddles and ball are created using `pygame.Rect`.

### Game Loop
- The main loop continues running until the user closes the window.
- The player paddle follows the mouse's Y position.
- The AI paddle moves up or down to follow the ball's Y position.
- The ball moves according to its speed, bouncing off the top and bottom edges of the screen.
- Collision detection checks if the ball hits the paddles or goes out of bounds.
- Scores are updated and displayed accordingly.

### Drawing
- Paddles, ball, and scores are drawn on the screen in each frame.
- The display is updated with `pygame.display.flip()`.

### Ending the Game
- The game loop exits and Pygame is quit when the window is closed by the user.

## Future Enhancements
- Add sound effects for paddle and wall collisions.
- Implement different difficulty levels for the AI.
- Add a start menu and game over screen.

Enjoy playing Pong!
