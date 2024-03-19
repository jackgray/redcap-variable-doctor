1. fixSurveyVars -- read field names, and determine what the correct field name should be according to rules ('changemap.json')

2. makePlan - Generate find and replace map of original field names and their new ones

3. applyPlan
 
applyChangemap(var, changemap) -- first method to reposition
3. makePlan
    fixVar(var, changemap, preChangemap, postChangemap)
        preChangemap(var, changemap)

4. applyPlan('/input/plan.json', 'redcap-project.zip')