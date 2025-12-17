# Success Metrics

## 1. Functionality

**Metric 1 - Move Detection Accuracy**

* **Description** - How well the system correctly detects moves sent by the camera.
* **Measurement Method** - Will test 10 games (long and short) with wierd moves and normal moves. Then compare what was detected vs whate was actually played.
* **Successful Metric** - If the system is able to correctly detect 90% of the moves.

**Metric 2 - Game PNG output**
* **Description** - How accurate the PNG produced from the game is.
* **Measurement Method** - Will test 10 games (long and short) with wierd moves and normal moves. Keeping track of the moves that is played.
* **Successful Metric** - If the system is able to correctly construct the PNG 95% of the time.

## 2. Performance

**Metric 3 - Response Speed**

* **Description** - How fast the system responds to each command or AI move.
* **Measurement Method** - Will time all kind of commands/moves.
* **Successful Metric** - If the system produces an average time of 3.5 sec.

**Metric 4 - Move detection Speed**

* **Description** - How fast the system reads the board and confirms a move was played.
* **Measurement Method** - Log timestamps from camera capture to board state update.
* **Successful Metric** - If the system responds in 2s on average.

## 3. Reliability and Robustness
 
**Metric 5 - Camera Obstruction Recognition**

* **Description** - During gameplay, hands and other things are bound to obstruct the camera. The camera must be able to detects any obstructions so it avoids misreading moves or updating the board state incorrectly.
* **Measurement Method** - Simulate common obstructions like hands, arms, or items over the board for varing durations. Will test about 20 different obsrtuctions under normal lighting.
* **Successful Metric** - If the system is able to detect these obstructions at a >95% correctness and also 0 board updates occur during these obstructions.

**Metric 6 - Lighting**

* **Description** - How well the system performs under different lighting.
* **Measurement Method** - Test 10 games under differnt lighting types: Bright, Normal, Semi Dim.
* **Successful Metric** - If the system is able to correctly detect 90% of the moves on all lighting types.

**Metric 7 – Uptime During a Game**

* **Description** - System can run a full game without crashing or needing a restart.
* **Measurement Method** - Run 10 full test games end-to-end.
* **Successful Metric** - 90% of games complete without a system restart.
