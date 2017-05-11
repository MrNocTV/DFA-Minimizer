from collections import defaultdict

class DFAMinimizer:
    def load_dfa(self, path):
        try:
            with open(path) as f:
                content = f.read().strip()
                self.dfa = eval(content)
                self.F = self.dfa['final_states']
        except FileNotFoundError:
            print('Find not found')
        except SyntaxError:
            print('Cannot parse DFA. Something wrong with file structure')
        except Exception:
            print('Sorry, cannot load DFA')

    def create_pairs_state_table(self):
        n = len(self.dfa['states'])
        arr1 = self.dfa['states'][1:]
        arr2 = self.dfa['states'][:-1]
        
        self.pairs = []
        for i in range(1, n):
            for j in range(i):
                pair = (arr1[i-1], arr2[j])
                self.pairs.append(pair)

    def create_states_dict(self):
        edges = self.dfa['edges']
        self.states = defaultdict(dict)
        for P, Q, label in edges:
            self.states[P][label] = Q

    def minimize_dfa(self, path):
        self.load_dfa(path)
        
        # step 1: create pairs of states
        self.create_pairs_state_table()
        self.create_states_dict()
        self.print_transition_table()

        # step 2: mark all pairs where either P or Q in F 
        unmarked_pairs, marked_pairs = self.mark_all_pairs_first()

        # step 3: 
        # If there are any unmarked pairs (P, Q)
        # such that [delta(P, x), delta(Q, x)] is marked,
        # then marked [P, Q]
        # repeat until no more markings can be made 
        while True:
            new_unmarked = set()
            for P, Q in unmarked_pairs:
                labels = self.dfa['sigma']
                for i, label in enumerate(labels):
                    u = self.delta(P, label)
                    v = self.delta(Q, label)
                    
                    if u == v and i == len(labels) - 1:
                        new_unmarked.add((P, Q))
                        break
                    else:
                        if (u, v) in marked_pairs or (v, u) in marked_pairs:
                            marked_pairs.add((P, Q))
                            break
                        else:
                            if i == len(labels) - 1:
                                new_unmarked.add((P, Q))

            if set(new_unmarked) == set(unmarked_pairs):
                break
            unmarked_pairs = new_unmarked
        print(unmarked_pairs)

        # step 4: combine all the unmarked pairs and make them 
        # a single state in the minimized DFA 
        self.combine_unmarked_pairs(unmarked_pairs)


    def mark_all_pairs_first(self):
        unmarked_pairs = set()
        marked_pairs = set()

        for P, Q in self.pairs:
            if P in self.F and Q in self.F:
                unmarked_pairs.add((P, Q))
            elif P in self.F:
                marked_pairs.add((P, Q)) 
            elif Q in self.F:
                marked_pairs.add((P, Q))
            else:
                unmarked_pairs.add((P, Q))
        return unmarked_pairs, marked_pairs

    def delta(self, state, x):
        return self.states[state][x]

    def print_transition_table(self):
        labels = self.dfa['sigma']
        header = ''.join(['{:>8s}'.format(x) for x in labels])
        print('     ' + header)
        for state in self.states:
            print('{:>5s}'.format(state), end='')
            for label in labels:
                print('{:>8s}'.format(self.states[state][label]),end='')
            print()
    
    def combine_unmarked_pairs(self, unmarked_pairs):
        states = set(self.states.keys())
        for P, Q in unmarked_pairs:
            states = states - set((P,Q))
        print(states)

if __name__ == '__main__':
    minimizer = DFAMinimizer()
    minimizer.minimize_dfa('../Examples/example3')