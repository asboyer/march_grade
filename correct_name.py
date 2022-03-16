def correct_name(name):
	name = name.lower().replace(' st', '-state').replace(' ', '-').replace('(', '').replace(')', '').lower().replace('.', '').replace("'", "")
	if name == "saint-marys":
		name = "saint-marys-ca"
	if name == 'loyola-chicago':
		name = 'loyola-il'
	if name == 'uconn':
		name = 'connecticut'
	if name == 'tcu':
		name = 'texas-christian'
	if name == 'uab':
		name = 'alabama-birmingham'
	if name == 'lsu':
		name = 'louisiana-state'
	if name == 'usc':
		name = 'southern-california'
	return name