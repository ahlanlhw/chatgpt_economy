import random
import numpy as np

class Person:
    def __init__(self, name, budget, strategy, profitable=False):
        self.name = name
        self.budget = budget
        self.debt = 0
        self.interest_rate = 0.05
        self.strategy = strategy
        self.profitable = profitable

    def __repr__(self):
        return f"{self.name} (${self.budget}, debt: ${self.debt},profit: ${self.budget-1000})"

    def make_repayment(self, amount):
        if amount > self.budget:
            print(f"{self.name} does not have enough money to make a repayment of ${amount}.")
            return False

        self.budget -= amount
        self.debt = max(0, self.debt - amount)

        return True

class Middleman:
    def __init__(self, mean_spread, std_spread, interest_rate):
        self.mean_spread = mean_spread
        self.std_spread = std_spread
        self.interest_rate = interest_rate
        self.profit = 0

    def trade(self, buyer, seller, item, price):
        spread = max(0, np.random.normal(self.mean_spread, self.std_spread))

        if buyer.profitable:
            if seller.profitable:
                return False
            else:
                buyer, seller = seller, buyer

        elif seller.profitable:
            pass

        else:
            if buyer.strategy(price, spread):
                if buyer.budget + buyer.debt < price:
                    print(f"{buyer.name} cannot afford {item} at {price}.")
                    return False

                if seller.budget + seller.debt + price < spread:
                    print(f"{seller.name} cannot afford to sell {item} at {price+spread}.")
                    return False

                self.profit += spread

                buyer.debt += max(0, price - buyer.budget)
                buyer.budget = max(0, buyer.budget - price)

                interest = buyer.debt * self.interest_rate
                buyer.debt += interest
                self.profit += interest

                seller.debt += max(0, spread - seller.budget)
                seller.budget = max(0, seller.budget + price - spread)

                print(f"{buyer.name} bought {item} from {seller.name} for ${price}.")
                return True

            else:
                print(f"{buyer.name} did not buy {item} from {seller.name} at {price}.")
                return False

class Economy:
    def __init__(self, people, middleman):
        self.people = people
        self.middleman = middleman

    def simulate(self, items):
        random.shuffle(items)

        for item, price in items:
            buyer, seller = random.sample(self.people, 2)
            while buyer is seller:
                buyer, seller = random.sample(self.people, 2)

            success = self.middleman.trade(buyer, seller, item, price)

            if not success:
                continue

            # Random chance of each person making a repayment
            for person in self.people:
                if person.debt > 0 and random.random() < 0.1:
                    repayment_amount = min(person.debt, random.uniform(0, person.budget))
                    person.make_repayment(repayment_amount)

        print("Final budget:")
        for person in self.people:
            print(person)

        print(f"The middleman made a profit of ${self.middleman.profit}.")


# Define strategies for each person
def random_strategy(price, spread):
    return random.random() < 0.5

def profit_strategy(price, spread):
    return price - spread > 10


# Define a list of people with initial budgets and strategies
people = []
for i in range(10000):
    name = f"Person {i+1}"
    budget = 1000
    # budget = random.randint(50, 200)
    if i < 2500:
        strategy = random_strategy
    else:
        strategy = profit_strategy
    people.append(Person(name, budget, strategy, i < 2500))

# Define a list of items with prices
lb = 5
ub = 100
items = [("tshirt", random.randint(lb,ub)), ("sneakers", random.randint(lb,ub)), ("trousers", random.randint(lb,ub)),
         ("bagpack",random.randint(lb,ub)),("sandals",random.randint(lb,ub)),("slippers",random.randint(lb,ub)),
         ("coat",random.randint(lb,ub)),("jacket",random.randint(lb,ub)),("pullover",random.randint(lb,ub))] * 1000

# Create a middleman instance with a random spread
mean_spread = 10
std_spread = 2
interest_rate = 0.05
middleman = Middleman(mean_spread, std_spread,interest_rate)

# Create an instance of the economy and simulate the transactions
economy = Economy(people, middleman)
economy.simulate(items)
