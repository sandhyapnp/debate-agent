#!/usr/bin/env python3

import sys
from debate_system import DebateSystem


def main():
    print("="*60)
    print("           WELCOME TO THE DEBATE AGENT SYSTEM")
    print("="*60)
    print("This system will help you practice debate skills through")
    print("interactive discussions on topics of your choice.")
    print("\nType 'exit' at any time to quit the program.")
    print("="*60)
    print()
    
    debate_system = DebateSystem()
    
    print("Let's start! What topic would you like to debate about?")
    print("(Or just tell me about your interests and I'll suggest topics)")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                print("Please enter something or type 'exit' to quit.")
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("\nThank you for using the Debate Agent System!")
                print("Keep practicing your debate skills! Goodbye!")
                break
                
            if user_input.lower() == "restart" and debate_system.get_state() == "evaluation":
                response = debate_system.restart()
                print(f"\n{response}")
                continue
            
            response = debate_system.process_input(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Thanks for using the Debate Agent System!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again or type 'exit' to quit.")


if __name__ == "__main__":
    main()