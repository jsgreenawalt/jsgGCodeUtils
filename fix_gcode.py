from gcodeparser import GcodeParser
from decimal import Decimal

gcode = """
"""


def parse_gcode(gcode):
    lines = gcode.split("\n")
    new_lines = []
    for line in lines:
        toks = []
        accum = []
        if len(line) == 0:
            new_lines.append({"comment":line})
            continue
        if line[0] == "(":
            new_lines.append({"comment":line})
            continue
        for c in line:
            #print("c=",c)
            if c.isalpha():
                #print("is alpha")
                #print("accum=", accum)
                if len(accum) > 0:
                    toks.append("".join(accum))
                    accum = []
                toks.append(c)
            else:
                # accumulate non-alpha
                #print("is not alpha")
                accum.append(c)
            #print("per-character accum =", accum)

        # done with all characters in line,
        # do the final append
        if len(accum) > 0:
            #print("final accum=", accum)
            toks.append("".join(accum))
            accum = []
        #print("final toks for line:", toks)
        dictRep = {}
        i = 0
        while i < len(toks):
            t = toks[i]
            try: tn = toks[i+1]
            except:
                dictRep[t] = None
                i += 1
                continue
            if t.isalpha():
                dictRep[t] = tn
                i += 1
            i += 1
        #new_lines.append(toks)
        new_lines.append(dictRep)

    return new_lines

def modify_gcode(gcode):
    for line in gcode:
        try: line['X'] = Decimal(0.0) - Decimal(line['X'])
        except KeyError: pass
        try: line['Y'] = Decimal(0.0) - Decimal(line['Y'])
        except KeyError: pass
        try: line['Z'] = Decimal(line['Z']) - Decimal(20)
        except KeyError: pass
    return gcode

def modified_gcode_to_string(gcode):
    out_string = []
    for line in gcode:
        line_accum = []
        for k, v in line.items():
            if k == 'comment':
                out_string.append(v)
                continue
            if v == None:
                out_string.append(k)
            else:
                out_string.append(str(k))
                out_string.append(str(v))
        out_string.append("\n")
    out_string = "".join(out_string)
    return out_string


with open("/mnt/c/Users/joe/Documents/Set_4_Chain.gcode", "r") as in_file:
    gcode = in_file.read()

parsed_gcode = parse_gcode(gcode)
modified_gcode = modify_gcode(parsed_gcode)
for line in modified_gcode:
    print(line)
out_str = modified_gcode_to_string(modified_gcode)
print(out_str)

with open("/mnt/c/Users/joe/Documents/Set_4_Chain_processed.gcode", "w") as out_file:
    out_file.write(out_str)
print("Done!")
