# Architecture

## Overview

This system automatically detects chess moves of an over the board chess game. It will be able to connect to any phone that has the application to serve a seemless connection. The app will provide AI interaction as well as game review. It will store full length games and provide the ability to export games via PNG. The system relies on real-time computer vision to track moves and must operate reliably under typical room lighting conditions.

## Major Features 

* **Camera Detection** - Camera will be set up over the board to capture every move that happens in the game and is sent to the phone
* **Move Validation** - Provide the ability to comfirm moves through the device, allowing for players time to make sure they made the right move.
* **Play VS AI** - Play aganist an AI bot that will have different options for level of skill.
* **Annouce AI Moves** - The phone will anounce the AI's moves and will have some personality to each move that they make.
* **Move Recording** - Games will be recorded where users can have the ability to go back and watch any game they want.
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
  * If the player isn't playing against AI, then this will be skipped.
  * Provides recommended moves, evaluations, and analysis when AI mode is enabled.
* **UI/Voice Output**
  * This will take the move that the Chess engine produced and turn it into an AI voice to inform the player of the move.
  * It will also update the UI on the app's version of the current game state regardless if the player is playing agaisnt AI or another player.
* **Game Logging/Storage**
  * After the game is over, all the moves saved in the game state manager is sent for storage where the user on the app can review anytime.
  * Stores PGN or move history for export.

## Flowchart Diagram

<img width="1122" height="978" alt="Screenshot 2025-12-09 212115" src="https://github.com/user-attachments/assets/5b8cb9b5-6e1b-4f6b-8187-b17c500990fb" />

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

## State Machine Design

### States:

* **Idle State** - The program is waiting for some command to indicate what type of game is to be played.
* **Game Setup** - The camera is calibrating the board set up to ensure that the game is ready to start (An illegal board doesn't start).
* **Player VS Player** - The State Manager expects moves from openCV program. Updates board according to the event.
* **Player VS AI** - The State Manager expects moves from both openCV and Chess Engine. Updates board according to the event.
* **AI Thinking** - The Chess engine is thinking of a move based on the current board state.
* **Player Thinking** - Whether playing against AI or another player, here the system waits for the player to make a move.
* **Error** - If the board is currenty in an illegal state then the system will wait for it to be fixed before going on.
* **Paused** - Game is paused and the state is saved to be played at a different time.

### Events:

#### Camera/OpenCV Events:

* move_detected - Anytype of move is detected.
* board_moved - Board moved and messed the calibration of the camera.
* illegal_moved - A move was played that is not allowed/possible.
* no_change - User indicated that they played a movee but there was no change in board state.

#### User Initiated Events:

* start_game_mode - User selects the type of game mode to play and starts it.
* undo_move - User has the ability to undo the last move, incase the system read the move incorrectly.
* review_game - User selects a game to review and sends a request to the PI to retrieve that said game.
* end_game - If the user wants to end the game early and has no future plans then this option will be give.
* pause_game - User can pause the game at anystate. This state will be saved for re-use later.

#### Chess Engine Events:

* ai_move_ready - AI's move is sent to the state manager.
* evaluation_ready - AI's game evaluation is ready.

#### System Events: 

* game_finished - Game has ended and the system does the appropriate actions.
* connection_failed - Failed to connect to the raspberry pi. 

## Multithreading

### Types:

**Main/Coordinator Thread**
* Coordinates all the other threads by managing the information that comes in.
* It will handle any errors, updates, or resets.
* It will also relay updates to the phone.
* It executes all Game State Manager operations.
* This is the only thread that will modify the game state.

**Camera Thread** 
* Constantly check every few seconds to see if there is any large changes on the board.
* The camera records at a slow frame rate and the main thread will decide when further analysis is needed.
* Can still run even if the system is proccessing a different move or waiting for an AI move.

**Cmaera Vision Proccessing Thread**
* Proccesses the video frames as they come in.
* These frames will be proccessed in a queue.
* Pushes the events that proccesed into the Event Bus queue.
* Runs without having to freeze the UI, or engine.

**Event Bus Thread**
* This will control what certain events will do.
* It will queue events as they come in.
* Dispatches events to the main thread where the Game State manager is run.
* This keeps the events in the correct order.

**Chess Engine Thread**
* Fetches a move or evaluates a move based on the current board state.
* Communicates with Main Thread via a response queue.
* Must run independently to not hinder other proccesses like CV or State Manager.

**Phone Connection Thread**
* Handles any updates from the phone.
* Sends commands to Main Thread via command queue.
* Sends UI updates to the phone.

### Concurrency Diagram:
<img width="1550" height="1101" alt="image" src="https://github.com/user-attachments/assets/b43fe15d-96b7-4b60-9da6-bd28a1afdd58" />

### Deadlock/Livelock Avoidance

#### Deadlock - Deadlock is the stalling of two different threads waiting for eachother to release a rescource that the other is using, causing an endless idle.

**How This Design Avoids Deadlock:**
- None of the Threads lock any shared data.
- Only the Main Thread is allowd to make updates to the board, relieving the need for multiple board accesses.
- The Threads have Unidirectional Communication which allows for smooth flow of information. It also ensures that no thread depends on receiving a message back from another thread before it continues.
- Queues act as a buffer make sure there is no issues with relaying information.
  
#### Livelock - Livelock happens when 2 threads are not stalled but are constantly reacting to eachother causeing a loop of interation and making no progress.

**How This Design Avoids Livelock:**
- No 2 threads react directly to each other.
- Only the Main Thread is allowed to make state trasfermations.
- Since engine and CV can't trigger each other, it aviods any issues that may arise.



