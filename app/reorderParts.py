import sys


# Asserts position according to priority value defined in changemap


def reorderParts(var, changemap, partindex):

    # variable field names contain key info like the survey name, or sub-labels for a category of questions in a survey. 
    # they have been created without a standard schema, and are not ordered consistently.
    # to assert the same set of rules across all of them, this function will read a set of rules (changemap), split the variables by underscores, and attempt to reorder them
    
    varparts = var.split('_') 
    origvar=var
    maxcount=0
    stop_condition = False
    while not stop_condition:
        prevar = var

        if partindex >= len(varparts):    # reminder: n=0
            break

        part = varparts[partindex]
        print(f"\n\nInspecting {part} at position {partindex}")
        
        try:
            # Check if current position of part reflects its assignment in changemap (is it in the right place)
            if partindex != changemap[part]['position']:
                # and varparts[changemap[part]['position']] != changemap[part]['changeto']: 
                
                # remove part and insert at designated position
                try:
                    varparts.pop(partindex)
                    print(f"Popped {part} from position {partindex}")
                    # print(varparts, len(varparts))
                    try:
                        varparts.insert(changemap[part]['position'], part)      # insert as defined index for the variable element found
                        print(f"Inserted {part} to position {changemap[part]['position']}")
                        print(f"{origvar}-->{'_'.join(varparts)}")
                        # print("resetting index")
                        partindex=0
                        
                    except Exception as e:
                        # print(f"Can't insert {part} into {varparts} at current index {partindex}: \n{e}")
                        exit()
                except Exception as e:
                    # print(f"Exception for {e}: Couldn't pop {varparts} at current index {partindex}")
                    exit(1)
            
                var = "_".join(varparts)
                print(f'{prevar} --> {var}')
                partindex=0 

                # Run this function until part index makes all the way through all parts without being reset
                # return fixVar2(var, partindex)
            else:
                print(f'Final variable name: {var}\n')  # This should be the correct variable and where the loop stops
                stop_condition = True
                
        except Exception as e:
            # The variable wasnt' found in the needs fixing list. Move to next component of variable
            # print(f'Exception for {e}')
            # print(var)
            partindex+=1
            pass # finish loop
        maxcount+=1
        if maxcount == 30:
            stop_condition = True   # Max tries: Protect against infinite loop
    
    else:
        partindex = 0  # Reset index and return variable
        return var
    

sys.modules[__name__] = reorderParts