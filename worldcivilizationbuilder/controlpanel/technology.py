from controlpanel.models import Technology, CivTec
import random

def unlock_another_technology(civilization):
	# Some how determin teh era of tech civ is on.
	# Possible tech
	possible_tech_names = Technology.PALEO_TECH_NAMES
	# remove tech they already have
	for tech_name in Technology.PALEO_TECH_NAMES:
		if civilization.has_technology_knowledge(tech_name):
			possible_tech_names.remove(tech_name)

	# remove tech you don't have prerequisite for
	possible_tech = []
	for tech_name in possible_tech_names:
		tech = Technology.objects.get(name=tech_name)
		if not (tech.prerequisite and 
			not civilization.has_technology_knowledge(tech.prerequisite.name)):
			possible_tech.append(tech)

	# todo what to do when all tech has been unlocked for this level
	if len(possible_tech) == 0:
		return

	choosen_index = random.randrange(0,len(possible_tech)-1)
	tech = possible_tech[choosen_index]

	CivTec.objects.create(
		civilization=civilization,
		technology=tech,
		active=True,
		)



