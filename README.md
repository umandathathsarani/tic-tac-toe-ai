# 🎮 Tic-Tac-Toe: Infinite Campaign

*A high-stakes, infinitely scaling tactical logic game featuring an advanced Minimax AI, procedural level generation, and a bespoke engine built from the ground up.*

---

# 🎓 Academic Context

* **Program:** Bachelor of Science Honours in Information Technology
* **Specialization:** Artificial Intelligence
* **Institutional Context:** Sri Lanka Institute of Information Technology (SLIIT)

This repository serves as a practical demonstration of advanced algorithm design, state-machine logic, and GUI event-driven programming.

---

# 🌟 Project Overview

**Tic-Tac-Toe: Infinite Campaign** evolves the classic 3x3 grid into a limitless, challenging tactical experience.

While traditional implementations rely on simple win-condition checks, this engine employs a **Minimax AI with Alpha-Beta Pruning**, significantly optimized via **Depth-Limiting** and **Local Search Heuristics** to ensure near-instantaneous decision-making on grids as large as **12x12**.

The architecture is built for sustainability; rather than hardcoding levels, a **procedural generation engine** uses deterministic random seeding to create unique, increasingly difficult board states.

The interface employs a **"Custom Chrome"** design methodology, using a borderless-window architecture to deliver a seamless, modern, and immersive user experience.

---

# 🚀 Key Features

## ♾️ Infinite Procedural Levels

Boards scale dynamically in size and complexity, ensuring an endless campaign.

## 🧠 Optimized AI Engine

A high-performance Minimax algorithm capable of solving complex board states without sacrificing system resources.

## 📱 Responsive UI Scaling

A fluid graphical interface that dynamically recalculates board and button geometry based on user window manipulation.

## 💾 Persistent Save-State System

Integrated JSON-based progress tracking that remembers the user's level across sessions.

## 🎨 Modern Aesthetic

A premium "Matcha/Earthy" color palette with 3D-raised interaction components.

## 🔊 Integrated Audio Mixer

A multi-layered sound effect system using Pygame to provide tactile feedback for moves, wins, and losses.

---

# 💻 Technical Stack

| Component           | Technology                              |
| ------------------- | --------------------------------------- |
| Backend Environment | Python 3.12                             |
| GUI Framework       | Tkinter (Custom event-driven engine)    |
| AI Logic            | Minimax Algorithm (Heuristic-optimized) |
| Audio Engine        | Pygame (Mixer module)                   |
| Data Persistence    | JSON (Progress tracking)                |
| Version Control     | Git & GitHub                            |

---

# 📂 System Architecture

```plaintext
tic-tac-toe-campaign/
├── audio/               # Game sound effects (WAV)
├── ai.py                # Minimax logic & local search heuristics
├── game.py              # Grid state & win-condition engine
├── main.py              # GUI engine & event-loop handler
├── save_data.json       # Persistent user progress
├── LICENSE              # Proprietary rights documentation
└── README.md            # Project documentation
```

---

# 🛠️ Installation & Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/umandathathsarani/tic-tac-toe-campaign.git
cd tic-tac-toe-campaign
```

## 2. Configure the Environment

Ensure you have **Python 3.x** installed.

Install the required sound library:

```bash
pip install pygame
```

## 3. Initialize the Engine

Launch the game application directly via the terminal:

```bash
python main.py
```

## 4. Create a Standalone Executable
To distribute the game as a professional .exe file without requiring Python installed on the target machine:

  * Install the packaging tool:
  ```
  pip install pyinstaller
  ```

  * Generate the executable:
  ```
  pyinstaller --onefile --windowed main.py
  ```

  * Deployment:
  After the build completes, find the main.exe in the dist/ folder. Ensure you copy your audio/ directory into the same location as main.exe to enable in-game sound effects.

  And if there is no save_data.json file inside that dist folder craate that file and inside that file include this line and save them: ``` {"level": 1} ``` 
  . Then again run that previous line: ``` pyinstaller --onefile --windowed main.py ```

---

# 🧠 AI Implementation Details

The AI system is built around the **Minimax Algorithm** enhanced with:

* Alpha-Beta Pruning
* Depth Limitation
* Localized Move Search
* Heuristic Evaluation Functions
* Dynamic Difficulty Scaling

These optimizations significantly reduce computational overhead while maintaining intelligent decision-making behavior on larger grids.

---

# 🔮 Future Enhancements

* Online multiplayer mode
* Leaderboard integration
* Achievement system
* Adaptive AI learning
* Campaign storyline progression
* Mobile deployment version

---

# 📄 License

Copyright (c) 2026 **Mummullage Binuri Umanda Thathsarani**.
All rights reserved.

This project is proprietary. Unauthorized copying, reproduction, distribution, or modification of this software, its source code, or its design assets is strictly prohibited.

This repository is published strictly for academic demonstration and professional portfolio purposes.

---

# 👩‍💻 Author

**Mummullage Binuri Umanda Thathsarani**
Undergraduate — BSc (Hons) Information Technology
Specialized in Artificial Intelligence
Sri Lanka Institute of Information Technology (SLIIT)

---
