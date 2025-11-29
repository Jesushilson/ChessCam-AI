# Deliverables

## Core System Requirements

- **Board Compatibility:** Works with most standard boards (goal: ~70%).
- **Move Detection Speed:** Detect moves in under **2 seconds**.
- **Move Accuracy Benchmark:** Achieve **90–95%** accuracy; include a **“That’s not my move”** correction button.
- **Move Confirmation Options:** Allow users to choose between instant detection or manual confirmation.
- **Piece Detection:** Automatically recognize most piece types, or include a calibration mode (e.g., “Show the knight to the camera”).
- **Portability:** System must be compact and easy to transport.
- **User-Friendly:** App must be simple, intuitive, and accessible.

---

## Testing Requirements

- **Lighting Robustness:** Test accuracy in bright, dim, and low-light environments.
- **Game Recording:** Successfully record **10 full games** from start to finish and document any issues.
- **Special Moves Support:** Fully support castling, en passant, promotions, and all capture types.
- **Real-Time Board Sync:** App must mirror the current board state with minimal desync.

---

## App & Interface Requirements

- **Camera Setup Wizard:** Provide a guided setup to help users connect to the camera.
- **Game Exports:** Allow exporting games as **PGN**, **JSON**, or **screenshots**.
- **Error Handling:** If the system is uncertain about a move, prompt the user for clarification.

---

## Documentation & Presentation

- **Architecture Diagram:** Include a visual overview of the system design.
- **Setup Guide:** Provide instructions for mounting the camera, configuring the Pi, and using the app.
- **Developer Documentation:** Document dependencies, Raspberry Pi setup, app setup, and API endpoints.
- **Demo Video:** Create a 2-minute demo showcasing core functionality.
- **Full GitHub Repository:** Maintain an organized repo with tasks, progress logs, and completed milestones.
