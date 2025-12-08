# Architecture

## Overview

This system automatically detects chess moves of an over the board chess game. It will be able to connect to any phone that has the application to serve a seemless connection. The app will provide AI interaction as well as game review. It will store full length games and provide the ability to export games via PNG. The system relies on real-time computer vision to track moves and must operate reliably under typical room lighting conditions.

## Major Features 

* **Camera Detection** - Camera will be set up over the board to capture every move that happens in the game and is sent to the phone
* **Move Validation** - Provide the ability to comfirm moves through the device, allowing for players time to make sure the made the right move.
* **Play VS AI** - Play aganist an AI bot that will have different levels of skill.
* **Annouce AI Moves** - The phone will anounce the AI's moves and will have some personality to each move that they make.
* **Move Recording** - Games will be recorded where useres can have the ability to go back an and watch any game they want.
* **Review Mode** - Users will be able to review games to see where they went wrong or struggled in any of their games. It will use Stockfish as a way of providing feedback on these moves.
* **Allow for Alternative Move Tree** - When looking back at old games, be able to try an alternative move to the one that was played in the actual game. Stockfish will provide feedback on whether that was a better move.
* **Player Vs Player Recording** - Games between 2 real players will also be recorded for fun reviews and learning.

## Major Components

* **Camera/Frame Capture**
  * Captures the board from a top down view.
  * Outputs continuous video frames of the board.
* **Computer Vision**
  * Reads the video frames.
  * Outputs detected move events or changes in board state.
* **Event System**
  * Based on the current board position, it will produce an event.
  * This event will trigger an outcome in game state manager.
  * Emits events (e.g., moveDetected, pieceCaptured, illegalMove) consumed by the Game State Manager.
* **Game State Manager**
  * This will manage the games states that we have had so far.
  * It will also talk to the game engine to update the current game state.
* **Chess Engine**
  * The game engine will provide moves based on the current state of the game.
  * Provides recommended moves, evaluations, and analysis when AI mode is enabled.
  * If the player isn't playing against AI, then this will be skipped.
* **UI/Voice Output**
  * This will take the move that the Chess engine produced and turn it into an AI voice to inform the player of the move.
  * It will also update the UI on the app's version of the current game state regardless if the player is playing agaisnt AI or another player.
* **Game Logging/Storage**
  * After the game is over, all the moves saved in the game state manager is sent for storage where the user on the app can review anytime.
  * Stores PGN or move history for export.

## Flowchart Diagram

<img width="1325" height="1132" alt="Screenshot 2025-12-07 173116" src="https://github.com/user-attachments/assets/227d20b2-d641-4452-bfa0-139a531ee918" />

## Communication Data Flow 

**1. Camera → Pi:**

   The camera is connected to the PI with a USB cable. The camera sends constant video frames to the PI when prompted (When a game has started). The camera will capture the game in a fairly low frame rate due to the slow pace of chess (Future advancement can improve this).
   
**3. Pi → Computer Vision:**

   The Pi communicates with an openCV program that will read the video frames as they come in. If the program detects any kind of change in the board state then an event is triggered. However, if the board state hasn't changed then the PI will disgard the video frame and move on.
   
**4. Computer Vision → Event System:**

   When the openCV program detects an event, it will send the imformation to the event system. This event system will execute the correct code depending on the type of event. If the move is legal then we can update the current game state.
   
**5. Event System → Game State Manager:**

   The Game State Manager recieves the command on what the board state should look like and updates accordingly. If the user has AI mode on then it will speak to the Chess Engine.

**6. Game State Manager ↔ Chess Engine:**

   The Chess Engine will recieve the current game state. If the player is playing against AI, then the engine will produce a move for it's turn. It will send that update back to manager. Alternatively, if the player just wants feedback then the engine will just read the current state and produce a score for the move the player just played.

**7. UI / App ↔ Game State Manager:**

   The Game State manager will then send updated game state to the UI app. If the user decides to terminate the game early or if the user wants to delete a previous move, then the app will notify the manager accordingly.

**8. Game State Manager → Storage:**

   After the game is over, the game state manager will store the game in the selected storage to be used again later.

