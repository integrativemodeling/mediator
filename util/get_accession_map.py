# Create the accession map used by test/mock/sitecustomize.py

import ihm.reference

codes = [ 'P38782', 'P38304', 'Q99278', 'P32569', 'P32585', 'P34162', 'P32570',
          'Q12343', 'Q08278', 'P33308', 'P38633', 'P47822', 'Q06213', 'Q12321',
          'P19263', 'P25046', 'Q12124', 'P40356', 'P53114', 'P19659', 'P32259']

def pp(s):
    indent = 8
    width = 66
    def get_lines(s):
        for i in range(0, len(s), width):
            yield ' ' * indent + "'" + s[i:i+width] + "'"
    return '\n'.join(l for l in get_lines(s))

for code in codes:
    u = ihm.reference.UniProtSequence.from_accession(code)
    print("    '%s': {'db_code':'%s', 'sequence':\n%s},"
          % (code, u.db_code, pp(u.sequence)))
