from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import os, time

"""
- Parse matches for all > 90%
- Place cookie so don't login every time
"""

def login():
	
	# username = raw_input("username: ")
	username = 'jdliauw@gmail.com'
	os.system("stty -echo")
	password = raw_input("password: ")
	os.system("stty echo")

	driver = webdriver.Firefox()
	driver.get("http://www.okcupid.com")
	driver.find_element_by_id('open_sign_in_button').click()
	driver.find_element_by_id('login_username').send_keys(username)
	driver.find_element_by_id('login_password').send_keys(password)
	driver.find_element_by_id('sign_in_button').click()

	time.sleep(1)
	driver.get("https://www.okcupid.com/match")

	return driver

def sort_by_match(driver):
	
	# click dropdown
	css = "[class='match-filters-in-results'] div[class='chosen-container chosen-container-single']"
	driver.find_element_by_css_selector(css).click()

	# sort by match
	css = "[class='chosen-container chosen-container-single chosen-with-drop chosen-container-active'] ul li:nth-child(2)"
	driver.find_element_by_css_selector(css).click()

	driver.find_element_by_css_selector("span[class='order-by-label']").click()
	driver.get("https://www.okcupid.com/match")

def select_city(driver, zip):

	css = "span[class='filter-wrapper filter-location-locale']"
	driver.find_element_by_css_selector(css).click()
	
	css = "div[class='clear-location-search'] button"
	driver.find_element_by_css_selector(css).click()
 
	xpath = "//span[text()='More options']"
	driver.find_element_by_xpath(xpath).click()

	time.sleep(1)
	css = "div[class='okinput'] input"
	driver.find_element_by_css_selector(css).click()

	css = "input[name='lquery']"
	driver.find_element_by_css_selector(css).send_keys(zip)

	time.sleep(1)
	css = "span[class='filter-wrapper filter-location-locale']"

class Match:
	name = None
	url = None
	age = None
	image = None
	match = None
	enemy = None

	def __init__(self, name, url, age, image, match, enemy):
		self.name = name
		self.url = url
		self.image = image
		self.age = age
		self.match = match
		self.enemy = enemy

def store_matches(driver, match_list):

	time.sleep(1)

	users = driver.find_elements_by_css_selector("div[class='match_card_wrapper user-not-hidden matchcard-user']")

	for user in users:
		name = user.find_element_by_css_selector("div[class='username'] a").text
		if name not in match_list:
			url = 	'www.okcupid.com/profile/{0}'.format(name)
			age = 	user.find_element_by_css_selector("span[class='age']").text
			image = user.find_element_by_css_selector("span[class='fadein-image image_wrapper loaded'] img").get_attribute('src')
			match = int(user.find_element_by_css_selector("div[class='percentage_wrapper match'] span[class='percentage']").text.replace('%', ''))
			enemy = int(user.find_element_by_css_selector("div[class='percentage_wrapper enemy'] span[class='percentage']").text.replace('%', ''))
			match_list.append(Match(name, url, age, image, match, enemy))

	last_index = len(match_list)-1

	if match_list[last_index].match >= 90:
		print "you ain't done yet"
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		print 'last =', match_list[last_index].name
		store_matches(driver, match_list)
	else:
		print "-----\nFINAL\n-----" 
		for match in match_list:
			print match.name
			print match.url
			print match.age
			print match.image
			print match.match
			print match.enemy


def cycle_cities(driver):

	zips = ["28801", 	# asheville, nc
		"94701",		# berkeley, ca
		"80301", 		# boulder, co
		"02108", 		# boston, ma
		"95616",		# davis, ca
		"80123", 		# denver, co
		"32826",  		# orlando, fl
		"04101", 		# portland, me
		"97201", 		# portland, or
		"02901",		# providence, ri
		"94101",		# san francisco, ca
		"90401",		# santa monica, ca
		"98101", 		# seattle, wa
		"98401"			# tacoma, wa
	]

	for zip in zips:
		select_city(driver, zip)
		time.sleep(1)

if __name__ == "__main__":
	driver = login()
	sort_by_match(driver)
	print ''
	store_matches(driver, [])

def count_matches_old(driver, match_list):
	
	time.sleep(1)

	names = driver.find_elements_by_css_selector("div[class='username'] a")
	print 'len names:', len(names)

	for i, name in enumerate(names):
		if name.text not in match_list:
			match_list.append(Match(name.text))
			match_list[i].url = 'www.okcupid.com/profile/{0}'.format(name.text)

	images = driver.find_elements_by_css_selector("span[class='fadein-image image_wrapper loaded'] img")
	print 'len images:', len(images)

	for i, image in enumerate(images):
		match_list[i].image = image.get_attribute('src')
		# print image.get_attribute('src')

	ages = driver.find_elements_by_css_selector("span[class='age']")
	print 'len ages:', len(ages)

	for i, age in enumerate(ages):
		match_list[i].age = age.text
		# print age.text

	matches = driver.find_elements_by_css_selector("div[class='percentage_wrapper match'] span[class='percentage']")
	print 'len matches:', len(matches)

	for i, match in enumerate(matches):
		match_list[i].match = int(match.text.replace('%', ''))
		# print int(match.text.replace('%', ''))

	enemies = driver.find_elements_by_css_selector("div[class='percentage_wrapper enemy'] span[class='percentage']")
	print 'len enemies:', len(enemies)

	for i, enemy in enumerate(enemies):
		match_list[i].enemy = int(enemy.text.replace('%', ''))
		# print int(enemy.text.replace('%', ''))

	print '-----'

	for match in match_list:
		for property in (match.name, match.url, match.image, match.age, match.match, match.enemy):
			print property
		print '-----'