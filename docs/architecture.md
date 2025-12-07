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
* **Computer Vision**
* **Game State Manager**
* **Chess Engine**
* **Event System**
* **UI/Voice Output**
* **Game Logging/Storage**

## Flowchart Diagram

<img width="766" height="646" alt="Overboard Chess AI Flowchart drawio" src="https://github.com/user-attachments/assets/0b9e5f0c-c5d4-446d-afe8-1defd9ed3a51" />
