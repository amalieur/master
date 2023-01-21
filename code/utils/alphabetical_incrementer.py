# Utils - alphabetical incrementer in python

# Helper functions for giving names to the trajectories. Alphabetical incremental counter

def __increment_chr(c: str) -> str:
    return chr(ord(c)+1) if c != 'Z' else 'A'

def increment_alphabetical(s: str) -> str:
    lpart = s.rstrip('Z')
    number_replacements = len(s) - len(lpart)
    new_s = lpart[:-1] + __increment_chr(lpart[-1]) if lpart else "A"
    new_s += "A" * number_replacements
    return new_s

