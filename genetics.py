import random

def solar(x, y, z):

    cost = 650*x #Cost to install
    energy = 24*x*y*z #Energy generated per day (Watt hours)
    return (cost, energy)

def wind(x, y, z):

    cost = 4000000*x #Cost to install
    energy = 18.1 * (y**2) * (z**3) * x #Energy generated per day (Watt hours)
    return cost, energy
    
def hydro(x, y, z):
    z /= 100

    energy = 212 * x * y * z #Energy generated per day (Watt hours)
    cost = energy/12 #Cost to install
    return cost, energy
    
def coal(x):

    cost = 0.15*x #Cost of coal 
    emission = 2.11*x # CO2 emissions per day (kg)
    energy = 6000*x #Energy generated per day (Watt hours)
    return cost, energy, emission
    
def oil(x, y):

    if y == "crude":
        cost = 0.45*x #Cost of oil   
        energy = 10500*x #Energy generated per day (Watt hours)
    if y == "gasoline":
        cost = 1.1*x #Cost of oil 
        energy = 9300*x #Energy generated per day (Watt hours)

    emission = 2.7*x # CO2 emissions per day (kg)
    return cost, energy, emission

def gas(x):

    cost = 0.12*x #Cost of natural gas 
    emission = 1.8*x # CO2 emissions per day (kg)
    energy = 10700*x #Energy generated per day (watt hours)
    return cost, energy, emission


# User Inputted Values

ff = "coal"     # Fossil Fuel type: Can be "coal", "oil" or "gas"

# Booleans that determine whether or not it's possible to use those energy sources


# Placeholder parameters for calculation functions
solar_wattage = 300
sunlight = 6
turbine_length = 40
wind_speed = 10
flow_rate = 5
hydro_eff = 75
oil_type = "crude"

max_cost = 1000000#float(input("Input the max cost:"))
max_emit = 500#float(input("Input the max kg of CO2 emissions per day:"))
min_power = 1000#float(input("Input the minimum watt hours generated per day:"))


# Genes are: s w h f (Number of solar panels, Number of wind turbines, Length of hydrodam, Amount of Fossil Fuel)
class Chromosome:
    def __init__ (self, genes: list):
        self.genes = genes
    
    def mutate (self):
        for i in range(4):
            f = random.choice(50*[0]+[0.01, 0.02, 0.03, 0.04, 0.05, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.5, 1])
            d = random.choice([-1, 1])
            self.genes[i] += self.genes[i]*f*d
            if self.genes[i] == 0:
                self.genes[i] = random.choice(50*[0] + [1])
            if i <= 1:
                self.genes[i] = int(self.genes[i])




# Fitness functions to determine least amount of emissions, smallest cost and most power
def fitness_emissions(c: Chromosome):
    s = solar(c.genes[0], solar_wattage, sunlight)
    w = wind(c.genes[1], turbine_length, wind_speed)
    h = hydro(flow_rate, c.genes[2], hydro_eff)
    if ff == "coal":
        f = coal(c.genes[3])
    elif ff == "oil":
        f = oil(c.genes[3], oil_type)
    elif ff == "gas":
        f = gas(c.genes[3])
    else:
        raise "Fossil Fuel Type is Invalid"
    cost = s[0] + w[0] + h[0] + f[0]
    power = s[1] + w[1] + h[1] + f[1]
    emissions = f[2]
    if cost > max_cost or power < min_power:
        emissions = float("inf")
    return ((emissions, cost, power))

def fitness_cost(c: Chromosome):
    s = solar(c.genes[0], solar_wattage, sunlight)
    w = wind(c.genes[1], turbine_length, wind_speed)
    h = hydro(flow_rate, c.genes[2], hydro_eff)
    if ff == "coal":
        f = coal(c.genes[3])
    elif ff == "oil":
        f = oil(c.genes[3], oil_type)
    elif ff == "gas":
        f = gas(c.genes[3])
    else:
        raise "Fossil Fuel Type is Invalid"
    cost = s[0] + w[0] + h[0] + f[0]
    power = s[1] + w[1] + h[1] + f[1]
    emissions = f[2]
    if emissions > max_emit or power < min_power:
        cost = float("inf")
    return ((cost, power, emissions))

def fitness_power(c: Chromosome):
    s = solar(c.genes[0], solar_wattage, sunlight)
    w = wind(c.genes[1], turbine_length, wind_speed)
    h = hydro(flow_rate, c.genes[2], hydro_eff)
    if ff == "coal":
        f = coal(c.genes[3])
    elif ff == "oil":
        f = oil(c.genes[3], oil_type)
    elif ff == "gas":
        f = gas(c.genes[3])
    else:
        raise "Fossil Fuel Type is Invalid"
    cost = s[0] + w[0] + h[0] + f[0]
    power = s[1] + w[1] + h[1] + f[1]
    emissions = f[2]
    if emissions > max_emit or cost > max_cost:
        power = -1
    return ((power, cost, emissions))


class Population:
    def __init__ (self, cost, emissions, power):   # n is the amount of chromosomes in a population, more is usually more efficient but more computing is needed
        self.population = [0] * 50
        self.cost = cost
        self.emissions = emissions
        self.power = power
        for i in range(50):
            s = random.randrange(0, 1000)
            w = random.randrange(0, 1000)
            h = random.randrange(0, 1000)
            f = random.randrange(0, 1000)
            self.population[i] = Chromosome([s, w, h, f])
        self.gen = 0
    
    def do_emissions (self):
        self.gen += 1
        self.population = sorted(self.population, key=fitness_emissions)
        self.b = fitness_emissions(self.population[0])

        # Printing used for testing
        #print(f"Generation {self.gen}: best is {self.population[0].genes} "
        #      f"with an emission of {self.b[0]}, a cost of {self.b[1]} and generating {self.b[2]} watt hours each day!")
        
        self.population = self.population[:25]
        out = self.population.copy()

        for i in range(5):
            random.shuffle(self.population)
            cop = self.population.copy()
            for j in range(5):
                a = cop.pop()
                b = cop.pop()
                baby = []
                for gene in range(4):
                    whichParent = random.choice([0, 1])
                    if whichParent == 0:
                        baby.append(a.genes[gene])
                    if whichParent == 1:
                        baby.append(b.genes[gene])

                c = Chromosome(baby)
                c.mutate()
                out.append(c)
        
        self.population = out
    
    def do_cost (self):
        self.gen += 1
        self.population = sorted(self.population, key=fitness_cost)
        self.b = fitness_cost(self.population[0])

        # Printing used for testing
        #print(f"Generation {self.gen}: best is {self.population[0].genes} "
        #      f"with an emission of {self.b[2]}, a cost of {self.b[0]} and generating {self.b[1]} watt hours each day!")
        
        self.population = self.population[:25]
        out = self.population.copy()

        for i in range(5):
            random.shuffle(self.population)
            cop = self.population.copy()
            for j in range(5):
                a = cop.pop()
                b = cop.pop()
                baby = []
                for gene in range(4):
                    whichParent = random.choice([0, 1])
                    if whichParent == 0:
                        baby.append(a.genes[gene])
                    if whichParent == 1:
                        baby.append(b.genes[gene])

                c = Chromosome(baby)
                c.mutate()
                out.append(c)
        
        self.population = out
    
    def do_power (self):
        self.gen += 1
        self.population = sorted(self.population, key=fitness_power, reverse = True)
        self.b = fitness_power(self.population[0])

        # Printing used for testing
        #print(f"Generation {self.gen}: best is {self.population[0].genes} "
        #      f"with an emission of {self.b[2]}, a cost of {self.b[1]} and generating {self.b[0]} watt hours each day!")
        
        self.population = self.population[:25]
        out = self.population.copy()

        for i in range(5):
            random.shuffle(self.population)
            cop = self.population.copy()
            for j in range(5):
                a = cop.pop()
                b = cop.pop()
                baby = []
                for gene in range(4):
                    whichParent = random.choice([0, 1])
                    if whichParent == 0:
                        baby.append(a.genes[gene])
                    if whichParent == 1:
                        baby.append(b.genes[gene])

                c = Chromosome(baby)
                c.mutate()
                out.append(c)
        
        self.population = out


cur = 0 # Current Best
count = 0
p = Population(max_cost, max_emit, min_power)
while True:
    p.do_power()
    if p.b == cur:  # Comparing new best to current best
        count += 1
    else:
        count = 0
        cur = p.b
    if count >= 3000:
        break




# JANKY WORK FUNCTION
def workFn (i):  # i for iterable
    if i == 0:   # Least amount of emissions
        p = Population(max_cost, max_emit, min_power)
        cur = 0 # Current Best
        count = 0
        while True:
            p.do_emissions()
            if p.b == cur:  # Comparing new best to current best
                count += 1
            else:
                count = 0
                cur = p.b
            if count >= 5000:
                print("Optimal Emissions")
                if p.b[0] > max_emit: 
                    print("Impossible with these params")
                    break
                print(f"Emissions:{p.b[0]}, Cost:{p.b[1]}, Energy:{p.b[2]}")
                print(f"Solar panels used: {p.population[0].genes[0]}")
                print(f"Wind Turbines used: {p.population[0].genes[1]}")
                print(f"Length of Hydrodam: {p.population[0].genes[2]}")
                print(f"Amount of Fossil fuel used: {p.population[0].genes[3]}")
                print()
                break
    elif i == 1:    # Least amount of cost
        p = Population(max_cost, max_emit, min_power)
        cur = 0 # Current Best
        count = 0
        while True:
            p.do_cost()
            if p.b == cur:  # Comparing new best to current best
                count += 1
            else:
                count = 0
                cur = p.b
            if count >= 5000:
                if p.b[0] > max_cost:
                    print("Impossible with these params")
                    break
                print("Optimal Cost")
                print(f"Emissions:{p.b[2]}, Cost:{p.b[0]}, Energy:{p.b[1]}")
                print(f"Solar panels used: {p.population[0].genes[0]}")
                print(f"Wind Turbines used: {p.population[0].genes[1]}")
                print(f"Length of Hydrodam: {p.population[0].genes[2]}")
                print(f"Amount of Fossil fuel used: {p.population[0].genes[3]}")
                print()
                break
    elif i == 2:
        p = Population(max_cost, max_emit, min_power)
        cur = 0 # Current Best
        count = 0
        while True:
            p.do_power()   # Most amount of energy
            if p.b == cur:  # Comparing new best to current best
                count += 1
            else:
                count = 0
                cur = p.b
            if count >= 5000:
                if p.b[0] < min_power:
                    print("Impossible with these params")
                    break
                print("Optimal Power")
                print(f"Emissions:{p.b[2]}, Cost:{p.b[1]}, Energy:{p.b[0]}")
                print(f"Solar panels used: {p.population[0].genes[0]}")
                print(f"Wind Turbines used: {p.population[0].genes[1]}")
                print(f"Length of Hydrodam: {p.population[0].genes[2]}")
                print(f"Amount of Fossil fuel used: {p.population[0].genes[3]}")
                print()
                break


for i in range(3):
    workFn(i)