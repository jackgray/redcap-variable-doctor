import sys
import renameParts, reorderParts

# Attempts to reorder components of a field name separated by '_'
# in 2 ways. 

def fixVar(seperator='_', var, changemap, preChangemap, postChangemap): 
    fixvar0 = var   

    # find replace on entire var word  
    formname = var.split(separator)[0]
    try:
        # run explicit fixes that transcend '_' separation
        for change, to in preChangemap.items():
            var = var.replace(change, to)
            print(f'\n{fixvar0}\t-->\t{var}')
    except: pass
    
    #######################
    #    RENAMING
    #######################
    # rename each part of the variable according to changemap
    print(f'Running renameParts: {var}\t --> ')
    var = renameParts(var, changemap)
    print(var, '\n')

    #######################
    #    SORT PART ORDER
    #######################
    # sort order according to dict (function to use as sort key in sorted function)
    def positions(dict):
        return lambda x: dict[x]['position']
    
    try:
        ##########
        # SORT 1 #
        ##########
        # 1st try is lazy lambda prioritization using position designation from changemap of given survey. Requires all parts to be defined
        var = seperator.join(sorted(var.split(separator), key=positions(changemap)))
    except:
        # Only variables that have all their parts defined in changemaps will be re-ordered above \
            # (because lambda functions exit on error & there is no way to handle them inside). 
            # We want to let variables that fail through, too

        # If lambda function failed the changemap is incomplete and will attempt abstractly following
        # preferences based on available info
        #    loops through several times until all conditions are met because sometimes preferences compete
        print(f"\n\n\n\n\nTrying best-effort sort function on :", var)
        partindex=0
        try:
            ##########
            # SORT 2 #
            ##########
            print(f'{var}\t-->\t')
            var = reorderParts(var, changemap, partindex)
            print(f'{var}')
        except Exception as e:
            raise e
    
    # find & replace again on chunks of new variable because of some fringe cases where it's easier to make them after
    #   (transcends '_' separation)
    try:
        for change, to in postChangemap.items():
            var = var.replace(change, to)

    except: pass
    
    print("\nAdding survey prefix back to begining of field name: ", changemap['prefix'])
    varparts = var.split(separator)
    try:
        varparts.insert(0, changemap['prefix']) # Puts the correct prefix as the leading variable component
    except Exception as e:
        print(f"No defined prefix found; using {formname}")
        varparts.insert(0, formname)
    var = separator.join(varparts)
    print(f'\n{startvar}\t-->\t{var}')
    
    return var

sys.modules[__name__] = fixVar