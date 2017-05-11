# DFA-Minimizer

Given a DFA G = (Q, sigma, delta, qo, F), with
+ Q: set of states
+ sigma: input set
+ delta: Q x sigma -> Q, state transitioning function
+ qo: starting state
+ F: set of final states

Steps:

1. Create all pairs of states
2. Mark all pairs where P in F and Q not in F (or vice versa)
3. If there are any unmarked pairs (P, Q)such that [delta(P,x), delta(Q,x)] is marked, then marked (P,Q).
Repeat (3) until no more markings can be made.
4. combine all the unmarked pairs and make them a single state in the minimized DFA


Input:
Stored as a file, with structure:
```
{
    'states': ['A', 'B', 'C', 'D', 'E', 'F'],
    'final_states': ['C', 'D', 'E'], 
    'sigma': ['0', '1'],
    'edges':[
        ('A', 'B', '0'),
        ('B', 'A', '0'),
        ('B', 'D', '1'),
        ('A', 'C', '1'),
        ('D', 'F', '1'),
        ('D', 'E', '0'),
        ('C', 'E', '0'),
        ('C', 'F', '1'),
        ('E', 'E', '0'),
        ('E', 'F', '1'),
        ('F', 'F', '0'), 
        ('F', 'F', '1')
    ]
}
```

Output:
```
{('E', 'C'), ('B', 'A'), ('E', 'D'), ('D', 'C')}
{'F'}
```

First set involves unmarked pairs
second set are remaining states.


Note: It is up to you to make sure that every state in the DFA has exactly k out-going transition edges, where k is len(sigma).

