###################################################################################
# This example will connect to ResInsight, retrieve a list of cases and print info
# 
###################################################################################

# Import the ResInsight Processing Server Module
import rips

# Connect to ResInsight
resInsight  = rips.Instance.find()
if resInsight is not None:
    # Get a list of all cases
    cases = resInsight.project.cases()

    print ("Got " + str(len(cases)) + " cases: ")
    for case in cases:
        print("Case name: " + case.name)
        print("Case grid path: " + case.gridPath())
        
        timesteps = case.timeSteps()
        for t in timesteps:
            print("Year: " + str(t.year))
            print("Month: " + str(t.month))
        
    

