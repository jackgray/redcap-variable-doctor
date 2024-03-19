import sys

# Changes the name of a matched field component to the preferred value defined in changemap input file ('changeto' field)

def renameParts(var, changemap):
    partindex=0
    varparts = var.split('_')    
    print("\nInspecting variable: ", var)
    # iterate over field name components (part), but partindex is dynamic. watch out for infinite loops
    while partindex < len(varparts):
        part = varparts[partindex]  # current part
        print("\nInspecting component : ", part)
        print("at position: ", partindex)
        try:
            # look for the current field part in the changemap
            if part in changemap.keys():
                print("\nVariable component matched in changemap: ", var)
                # survey name designators are flagged with -9 index because they belong first
                # save it and pop it from the list so the rest of the fields can be ordered by their index priority values
                # (remove survey label for component reordering it will be added later)
                if changemap[part]['position']==-9:
                    varparts.pop(partindex)
                    # reset part index to start over (important for when survey name isn't already the first part of the field name)
                    partindex=0
                else:
                    print(f"Changing {part}\t-->\t{changemap[part]['changeto']}\n")
                    varparts[partindex]=changemap[part]['changeto'] # change  field component in-place, then move to next component in the list
                    partindex+=1
            else:
                # print('failed for ', varparts[partindex])
                partindex+=1
        except Exception as e:
            # print(f'Error: {e} in {part} from {varparts}')
            # if there is no match move to next component
            partindex+=1
            pass
    # print("--> ", "_".join(varparts))
    return "_".join(varparts)

sys.modules[__name__] = renameParts