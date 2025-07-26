# Debate Agent System

An educational agentic system designed to help students practice debate skills through interactive discussions.

## Features

### 🎯 Topic Selector Agent
- Interactive topic discovery through questions
- Suggests debate topics based on user interests
- Allows users to choose their stance (for/against)
- Exit functionality at any time

### 🗣️ Debator Agent
- Builds comprehensive arguments based on selected topic and stance
- Analyzes user arguments and provides thoughtful counterpoints
- Maintains topic focus throughout the debate
- Adapts responses based on argument quality

### 📊 Critique Agent
- Scores arguments on multiple criteria:
  - Evidence use (20 points)
  - Logical structure (25 points)
  - Relevance (20 points)
  - Persuasiveness (20 points)
  - Clarity (15 points)
- Provides constructive feedback after each round
- Tracks overall debate performance
- Generates final evaluation with grades and improvement suggestions

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python main.py
```

### Example Flow:
1. **Topic Selection**: Share your interests or choose from suggested topics
2. **Stance Selection**: Choose to argue FOR or AGAINST the topic
3. **Debate**: Make arguments and respond to counterpoints
4. **Evaluation**: Receive scores, feedback, and final grade

### Commands:
- `exit` or `quit` - Exit the program at any time
- `restart` - Start a new debate after evaluation
- `end debate` - End current debate and see evaluation

## System Architecture

```
DebateSystem (main orchestrator)
├── TopicSelectorAgent (topic discovery & selection)
├── DebatorAgent (argument generation & analysis)
└── CritiqueAgent (scoring & feedback)
```

Each agent inherits from `BaseAgent` and follows a modular design for easy extension.

## Educational Benefits

- **Critical Thinking**: Practice analyzing and constructing arguments
- **Communication Skills**: Improve clarity and persuasiveness
- **Evidence-Based Reasoning**: Learn to support claims with evidence
- **Perspective Taking**: Understand different viewpoints on complex issues
- **Real-time Feedback**: Immediate scoring and improvement suggestions

## Future Enhancements

- AI model integration for more sophisticated responses
- Resume/portfolio analysis for personalized topic suggestions
- Multiple debate formats (formal, casual, Socratic)
- Persistent user progress tracking
- Group debate capabilities