from sys import modules
import fixVar

def makePlan(separator='_', varnames, formnames, survey, preChangemaps,changemaps, postChangemaps):
    
    # load changemaps for a given survey
    changemap = changemaps[survey]
    try: preChangemap = preChangemaps[survey]
    except: preChangemap = {}
    try: postChangemap = postChangemaps[survey]
    except: postChangemap = {}
    plan = {}    
    
    print(f"\nNormalizing survey: {survey}\n")
    varindex=0
    
    # rename each variable, adding a new item to plan.json (find & replace keyfile)
    for var in varnames:
        origvar = var   # keep track of last variable

        # check if survey name defined in changemap is in list of surveys from redcap file
        if survey in formnames[varindex]:
            
            print('\nUsing form: ', formnames[varindex])        
            
             # # # # # # # # # # # # # #
            # APPLY RULES TO VARIABLE  #
             # # # # # # # # # # # # # #
            var = fixVar(var, changemap, preChangemap, postChangemap)
            
            # add proper survey name back to beginning of variable as defined by changemap
            newvar = separator.join(newvar.split(separator).insert(0, changemap['prefix']))
            
            print(f"{origvar}\t-->\t{newvar}")

            # makes key:value pair list of originalname:newname
            plan[origvar] = newvar
            plan[formnames[varindex]] = separator.join([changemap['prefix'], formnames[varindex]])
        varindex+=1
    return plan

modules[__name__] = makePlan

