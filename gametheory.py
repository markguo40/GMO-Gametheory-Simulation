from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import random

class Company(object):

	CAP_WEIGHT = 10
	QUALITY_MULTI = 25
	BIAS_EFFECT = 25
	market_size = 0 #this variable change overtime
	survive = 0

	def __init__(self, grp_threshold, capital, cog_bias, drug_quality):
		"""Input

		grp_threshold: int, how many other companies out there who are selling GMO
		capital: int, how many capital it has (in million), it associates with risk
		cog_biase: scale from 1 - 5, 1 means risk averse, 5 means risk seeking. 
		drug_quality: scale from 1 - 5, 1 means lowest, 5 means highest
		"""
		self.threshold = grp_threshold
		self.capital = capital
		self.cog_bias = cog_bias
		self.drug_quality = drug_quality
		self.survive = True # True means survive
		Company.survive += 1
		self.wealthdelta = 0 # use to evaluate the change in cog_bias and drug_quality
		Company.market_size += capital

	def get_quality(self):
		return self.drug_quality

	def get_cog_bias(self):
		return self.cog_bias

	def decision_index(self):
		return self.threshold - self.capital / self.CAP_WEIGHT \
				- (self.cog_bias - 3) * self.BIAS_EFFECT \
				 - (self.drug_quality - 3) * self.QUALITY_MULTI
				
	def _luck(self, win, lose):
		if random.random() > 0.5: #check whether it is lucky
			self.capital += win
			self.wealthdelta += win
			Company.market_size += win
		else:
			self.capital -= lose
			self.wealthdelta -= lose
			Company.market_size -= lose

	def capital_gain(self):
		"""capital gain heavily depend on the market_share, and somewhat depends on luck

		income can be a negative number, in that case, it will be captical loss"""
		shares = self.capital / self.market_size
		if shares > 0.01:
			self._luck(20, 18)
		elif shares > 0.005:
			self._luck(10, 8)		
		elif shares > 0.002:
			self._luck(5, 5)
		else:
			self._luck(3, 3)

		#check whether the bias change
		if self.wealthdelta > 100:
			self.drug_quality += 1
			self.wealthdelta = 0 # startover
			self.capital -= 100
		elif self.wealthdelta > 50 and self.cog_bias < 5:
			self.cog_bias += 1
			self.wealthdelta = 0 # startover

		#check to lower the bias and wealth
		if self.wealthdelta < -100 and self.drug_quality > 1:
			self.drug_quality -= 1
			self.wealthdelta = 0 # startover
		elif self.wealthdelta < -50 and self.cog_bias > 1:
			self.cog_bias -= 1
			self.wealthdelta = 0 # startover
	
	def get_capital(self):
		return self.capital

	def __lt__(self, other):
		if self.survive:	
			self.capital_gain() #capital gain from last period
			if self.capital < 1: #Check after capitcal gain, whether the company survive
				self.survive = False
				Company.survive -= 1
				return False
			return other > self.decision_index()
		return False

def sort_capital(company):
	return company.get_capital()

def pop_complex():
	"""Building companies through class"""
	cap = pop("exponential") #create capitals for companies, exponential is reality
	thres = pop("reverse exponential") #reverse exponential is close to reality
	cog = pop("uniform for cog bias and drug quality")
	drug = pop("uniform for cog bias and drug quality")
	companies = [Company(thres[i], cap[i], cog[i], drug[i]) for i in xrange(500)]
	print "Initial market size is", Company.market_size, 'million dollars with',\
			Company.survive, 'companies remaining.'
	return companies

def top(dist, start, stop, print_stat=False):
	count = start + 1
	total = 0
	for i in dist[start:stop]:
		if print_stat:
			print "Top {0}: has {1} million dollar. Drug Quality Level is {2}".format(
				count, i.get_capital(), i.get_quality()),\
				'Has cognitive bias level:', i.get_cog_bias()

		total += i.get_capital()
		count += 1
	return total

def pie_chart(dist, ax, title):
	arr = sorted(dist, key=sort_capital, reverse=True)
	top10 = top(arr, 0, 10, True)
	top20 = top(arr, 10, 20)
	top30 = top(arr, 20, 30)
	labels = 'Top 10', 'Top 10 to 20', 'Top 20 to 30', 'Rest'
	explode = 0, 0, 0, 0.05
	fracs = [top10, top20, top30, Company.market_size - top10 - top20 - top30]
	ax.pie(fracs, explode=explode, labels=labels,autopct='%1.1f%%', 
				shadow=True, startangle=90)
	ax.set_title(title)

def main_complex(init=300, period=50):
	arr = np.array(pop_complex())
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(223)
	ax3 = plt.subplot(122)
	pie_chart(arr, ax1, 'Start Point Market share layout\n{0} millions with {1} companies'.format(
			Company.market_size, Company.survive
		))

	visual(threshold(arr, init, period), ax3, \
		'Numbers of Businesses Who Sell GMO Food Over Time', \
		'The number of business period (seasons)', \
		'The number of companies sell GMO food', h=1.03)
	print '\n\nAfter all the period\n\n'

	pie_chart(arr, ax2, 'Market share layout After {0} Period\n{1} millions with {2} companies'.format(
		period, Company.market_size, Company.survive
		))

	print "Current market size is", Company.market_size, 'million dollars with',\
			Company.survive, 'companies remaining.'	

def _setboundary(x):
	"""Fixed the data overflow problem: 
	data point higer than 499 or lower than 1 does not make sense"""
	if x < 1:
		return 1
	elif x > 499:
		return 499
	else:
		return x

def pop(dist=None, fixed=None):
	"""Create the population GMO companies threshold
	return a np array. Default is uniform distribution."""
	if dist == 'normal':
		return np.array(map(_setboundary, np.random.normal(250, 100, 500).astype(int)))
	elif dist == 'exponential':
		return np.array(map(_setboundary, np.random.exponential(100, size=500).astype(int)))
	elif dist == 'reverse exponential': # use 500 minus each number in exponential
		return np.array(map(_setboundary, 500 - np.random.exponential(100, size=500).astype(int)))
	elif dist == 'uniform for cog bias and drug quality': #only use in the complex case
		return np.random.random_integers(1, 5, 500)
	elif dist == 'set':
		return np.array([fixed] * 500)
	else:
		return np.random.random_integers(1, 499, 500) #start at 0 don't make sense

def threshold(dist, init, weeks):
	result = [init]
	for i in xrange(weeks):
		result.append(len(dist[result[i] > dist]))
	return result

def visual(result, ax, title, x, y, h=1):
	ax.plot(xrange(len(result)), result)	
	ax.set_title(title, y=h)
	ax.set_xlabel(x)
	ax.set_ylabel(y)

def main_simple(init=300, weeks=50, dist_name='uniform'):
	value = None
	if dist_name == 'set':
		value = int(raw_input('Please enter a fixed value'))
	dist = pop(dist_name, value)
	print dist, len(dist), type(dist)
	ax1 = plt.subplot(121)
	ax2 = plt.subplot(122)
	visual(threshold(dist, init, weeks), ax1, \
		'Number of Businesses in GMO markets Over time \nSingle case under {0} distribution.\n {1} initial company'.format(
			dist_name, init), 'The number of business period (seasons)', \
		'The number of companies sell GMO food', 1.02)
	multi_init = []
	# Assumption: All the function will reach equalibrium in 50th weeks.
	for i in xrange(0, 501):
		#Against stomastic model, place 10 times and get average
		multi_init.append(np.mean([threshold(dist, i, 50)[-1] for _ in xrange(10)]))
	visual(multi_init, ax2, 'Equalibriums for All Inital Values (From 1 to 499)',\
		'Number of Businesses in the market initially',\
		'Equalibrium business', 1.03)
	plt.subplots_adjust(left=0.08, right=0.96)

def run():
	print 'Welcome to GMO Simulation. You have two versions to choose from:',\
		'\n1. Simple version: The threshold function only based on how many other companies involve',\
		'\n2. Complex version: The threshold function depends on\n\ta.How many other companies involve'+\
		'(reverse exponential distribution)\n\tb.How much capital a company have '+\
		'(exponential distribution)\n\tc.Cognitive Bias a company\'s managers has (Either '+\
		'risk adverse or risk seeking (uniformly scale from 1 - 5))\n\td.Drug Quality. The GMO quality ' +\
		'uniformly scale from 1 - 5.\n\te.The company each run will make or lose money depends on their size'+\
		' and their luck\nComplex version consider the dynamic for the individuals company'+\
		' especially the top 10 company. We will focus on the market change as a whole\n'+\
		'\nEnter 0 if you want to try only simple version, 1 for only complex, other numbers for both'
	choice = int(raw_input())
	init = int(raw_input('What initial value (businesses sell GMO last week) your like?'))
	period = int(raw_input('How long (in weeks, but the complex one will be in seasons)?'))
	if choice == 0 or choice != 1:
		distribution = raw_input('What type of population distribution your like?' + \
		'Please enter uniform, normal, exponential, reverse exponential\n' +\
		'Please enter set if you want to set a fixed value. fail to do so will trigger the default which is uniform:')
		plt.figure()
		main_simple(init, period, distribution)
	if choice == 1 or choice != 0:
		plt.figure()
		main_complex(init, period)
	plt.show()

run()
#################
# Ignore the function below
#################
def test(init, weeks):
	"""To test whether the data in main matches with the data in the sample program"""
	with open("data.txt") as f:
		new = f.read().split(',')
		new = np.array(map(lambda x: int(x), new))
	print new, len(new[init > new])
	visual(threshold(new, init, weeks))
