from github import Github
from dateutil.parser import parse
g = Github()
repo = g.get_repo("dharlabwustl/EDEMA_MARKERS")
contents = repo.get_contents("module_NWU_CSFCompartment_Calculations.py")
dt = parse(contents.last_modified)

Version_Date="VersionDate-" + dt.strftime("%m_%d_%Y")
print(Version_Date)


