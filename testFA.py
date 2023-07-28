class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.final_states = set()

    def input_fa(self):
        self.input_states()
        self.input_alphabet()
        self.input_transitions()
        self.input_initial_state()
        self.input_final_states()
        self.display_transition_table()

    def input_states(self):
        num_states = int(input("Enter the number of states: "))
        self.states = {'q' + str(i) for i in range(num_states)}

    def input_alphabet(self):
        alphabet_input = input("Enter the symbols in the alphabet separated by commas: ")
        self.alphabet = {symbol.strip() for symbol in alphabet_input.split(",")}

    def input_transitions(self):
        epsilon = "$"
        for state in sorted(self.states):
            for symbol in sorted(self.alphabet, key=lambda x: int(x) if x.isdigit() else x):
                next_states_input = input("Enter the next states for transition ({} -{}-> ?) "
                                          "separated by commas (leave empty if none): ".format(state, symbol))
                next_states = [state.strip() for state in next_states_input.split(",")]
                if next_states:
                    self.transitions.setdefault(state, {}).setdefault(symbol, set(next_states))
                else:
                    # If next_states is empty, remove the entry for the transition
                    self.transitions.get(state, {}).pop(symbol, None)

        has_epsilon = input("Are there any epsilon transitions? (y/n): ")
        if has_epsilon.lower() == 'y':
            for state in sorted(self.states):
                next_states_epsilon_input = input("Enter the next states for epsilon transition ({} -{}-> ?) "
                                                  "separated by commas (leave empty if none): ".format(state, epsilon))
                next_states_epsilon = [state.strip() for state in next_states_epsilon_input.split(",")]
                if next_states_epsilon:
                    self.transitions.setdefault(state, {}).setdefault(epsilon, set(next_states_epsilon))
                else:
                    # If next_states_epsilon is empty, remove the entry for the epsilon transition
                    self.transitions.get(state, {}).pop(epsilon, None)


    def input_initial_state(self):
        self.initial_state = input("Enter the initial state: ")

    def input_final_states(self):
        final_states = input("Enter the final states (comma-separated): ")
        self.final_states = set(final_states.split(","))

    def display_transition_table(self):
        epsilon = "$"
        print("Transition Table:")
        header = [epsilon] + sorted(self.alphabet)
        max_state_length = max(len(state) for state in self.states)
        max_symbol_length = max(len(symbol) for symbol in header)
        row_format = "{:<{}} |".format("", max_state_length)
        for symbol in header:
            row_format += " {:<{}} |".format(symbol, max_symbol_length)
        print(row_format)
        print("-" * ((max_state_length + max_symbol_length + 3) * (len(header) + 1)))
        for state in sorted(self.states):
            row = "{:<{}} |".format(state, max_state_length)
            for symbol in header:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states = sorted(self.transitions[state][symbol])
                    row += " {:<{}} |".format(','.join(next_states), max_symbol_length)
                else:
                    row += " {:<{}} |".format("", max_symbol_length)
            print(row)

    def is_nfa(self):
        for state, transitions in self.transitions.items():
            for symbol in self.alphabet:
                if symbol in transitions and len(transitions[symbol]) > 1:
                    return True

        # Check for epsilon transitions (NFA condition)
        epsilon = "$"
        for state, transitions in self.transitions.items():
            if epsilon in transitions and len(transitions[epsilon]) > 0:
                return True

        return False

    def test_string(self, string):
        current_states = {self.initial_state}
        for symbol in string:
            next_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])
            current_states = next_states
        return any(state in self.final_states for state in current_states)

    def convert_to_dfa(self):
            dfa = FiniteAutomaton()
            dfa.states = {frozenset(self.epsilon_closure({self.initial_state}))}
            dfa.alphabet = self.alphabet
            dfa.initial_state = frozenset(self.epsilon_closure({self.initial_state}))
            queue = [dfa.initial_state]
            visited = set()

            while queue:
                current_state = queue.pop(0)
                visited.add(current_state)
                for symbol in dfa.alphabet:
                    next_state = frozenset(self.epsilon_closure(self.move(current_state, symbol)))
                    if next_state not in visited:
                        queue.append(next_state)
                    dfa.transitions.setdefault(current_state, {})[symbol] = next_state
                    if next_state not in dfa.states:
                        dfa.states.add(next_state)
                        if any(state in self.final_states for state in next_state):
                            dfa.final_states.add(next_state)

            return dfa

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if state in self.transitions and symbol in self.transitions[state]:
                next_states.update(self.transitions[state][symbol])
        return next_states

    def epsilon_closure(self, states):
        closure = set(states)
        current_states = set(states)
        while True:
            next_states = set()
            for state in current_states:
                if state in self.transitions and '$' in self.transitions[state]:
                    next_states.update(self.transitions[state]['$'])
            if not next_states:
                break
            closure.update(next_states)
            current_states = next_states
        return closure

    def minimize_dfa(self):
        # Code to minimize the DFA
        pass

    def save_data(self, file_name):
        with open(file_name, 'w') as file:
            file.write("States: {}\n".format(','.join(self.states)))
            file.write("Alphabet: {}\n".format(','.join(self.alphabet)))
            file.write("Transitions:\n")
            for state, transitions in self.transitions.items():
                for symbol, next_states in transitions.items():
                    for next_state in next_states:
                        file.write("{} -{}-> {}\n".format(state, symbol, next_state))
            file.write("Initial State: {}\n".format(self.initial_state))
            file.write("Final States: {}\n".format(','.join(self.final_states)))


def main():
    fa = FiniteAutomaton()
    fa_input = False

    while True:
        print("Finite Automaton Menu")
        print("1. Input FA")
        print("2. Test string")
        print("3. Convert to DFA")
        print("4. Minimize")
        print("5. Save to file")
        print("6. Check if NFA or DFA")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            fa.input_fa()
            fa_input = True
        elif choice == "2":
            if not fa_input:
                print("Please input the Finite Automaton first.")
                continue

            string = input("Enter the string to test: ")
            if fa.is_nfa():
                if fa.test_string(string):
                    print("Accepted")
                else:
                    print("Rejected")
            else:
                if fa.test_string(string):
                    print("Accepted")
                else:
                    print("Rejected")
        elif choice == "3":
            dfa = fa.convert_to_dfa()
            dfa.display_transition_table()
            fa_input = True
        elif choice == "4":
            if not fa_input:
                print("Please input the Finite Automaton first.")
                continue
            fa.minimize_dfa()
        elif choice == "5":
            if not fa_input:
                print("Please input the Finite Automaton first.")
                continue
            file_name = input("Enter the file name to save: ")
            fa.save_data(file_name)
        elif choice == "6":
            if not fa_input:
                print("Please input the Finite Automaton first.")
                continue
            if fa.is_nfa():
                print("The automaton is an NFA.")
            else:
                print("The automaton is a DFA.")
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
