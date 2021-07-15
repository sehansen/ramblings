#!/usr/bin/env python3

import random

Jobs = ["wage_labour", "farming"]
wage_labour = Jobs[0]
farming = Jobs[1]

Resources = ["gold", "food"]
gold = Resources[0]
food = Resources[1]

Rewards = {wage_labour: {gold: 1.0}, farming: {food: 5}}


class InvalidJobException(Exception):
    pass


class OnlyWorkStrategy:
    def select_work_strategy(self):
        return wage_labour

    def select_trading_strategy(self):
        if self.gold == 0:
            return (None, None)
        strategy_table = {0: [(self.gold / x, 1) for x in range(1, 11)],
                          1: [(self.gold / (x + 1), 1) for x in range(1, 10)],
                          2: [(self.gold / (x + 2), 1) for x in range(1, 9)],
                          3: [(self.gold / (x + 3), 1) for x in range(1, 8)],
                          4: [(self.gold / (x + 4), 1) for x in range(1, 7)],
                          5: [(1/6, 1), (0.2, 1), (1/4, 1), (1/3, 1), (0.5, 1)],
                          6: [(1/6, 1), (0.2, 1), (1/4, 1), (1/3, 1)],
                          7: [(1/6, 1), (0.2, 1), (1/4, 1)],
                          8: [(1/6, 1), (0.2, 1)],
                          9: [(1/6, 1)]}

        bid_structure = strategy_table[self.food]
        # This guy just goes to work and buys his food on auction
        ask_structure = None

        return (bid_structure, ask_structure)

    def update(self, gold, food, clearing_price, amount_cleared):
        self.gold = gold
        self.food = food


class OnlyFarmStrategy:
    def select_work_strategy(self):
        if self.food < 10:
            return farming
        else:
            return wage_labour

    def select_trading_strategy(self):
        if self.food > 9:
            free_food = self.food - 9
        else:
            free_food = 0

        strategy_table = [(0.2, 1), (0.25, 1), (0.4, 1), (0.5, 1),
                          (0.8, 1), (1, 1), (1.6, 1), (2, 1)]

        bid_structure = None
        ask_structure = [(0, 1)] * free_food + [(x, y + free_food)
                                                for x, y in strategy_table
                                                if y < self.food]

        return (bid_structure, ask_structure)

    def update(self, gold, food, clearing_price, amount_cleared):
        self.gold = gold
        self.food = food


class YesterdayTenPercentStrategy:
    def __init__(self):
        self.sell_price = 0.5
        self.buy_price = 0.2

    def select_work_strategy(self):
        if self.food == 1:
            return farming
        else:
            return wage_labour

    def select_trading_strategy(self):

        bid_structure = [(self.buy_price, 10 - self.food)]
        ask_structure = [(self.sell_price, self.food - 1)]

        return (bid_structure, ask_structure)

    def update(self, gold, food, clearing_price, amount_cleared):
        self.gold = gold
        self.food = food
        if clearing_price is not None:
            self.sell_price = clearing_price * 1.1
            self.buy_price = clearing_price * 0.9



class TwodayTenPercentStrategy:
    def __init__(self):
        self.sell_price = 0.5
        self.buy_price = 0.2
        self.old_clearing_price = 0.2

    def select_work_strategy(self):
        if self.food == 1:
            return farming
        else:
            return wage_labour

    def select_trading_strategy(self):

        bid_structure = [(self.buy_price, 10 - self.food)]
        ask_structure = [(self.sell_price, self.food - 1)]

        return (bid_structure, ask_structure)

    def update(self, gold, food, clearing_price, amount_cleared):
        self.gold = gold
        self.food = food
        if clearing_price is not None:
            self.sell_price = self.old_clearing_price * 1.1
            self.buy_price = self.old_clearing_price * 0.9
            self.old_clearing_price = clearing_price


class Market:
    def __init__(self, market_participants):
        self.market_participants = market_participants
        self.states = []
        for participant in self.market_participants:
            self.states.append((0.0, 1))
            participant.update(0.0, 1, None, None)

    def end_day(self):
        job_rewards = []
        for work in self.jobs:
            if work == wage_labour:
                job_rewards.append((1, 0))
            elif work == farming:
                job_rewards.append((0, 5))
            else:
                raise InvalidJobException

        self.states = [(x + a, y - 1 + b)
                       for (x, y), (a, b) in zip(self.states, job_rewards)]

    def start_day(self):
        self.jobs = [participant.select_work_strategy()
                     for participant in self.market_participants]

    def run_auction(self):
        bids = []
        asks = []

        for pid, participant in enumerate(self.market_participants):
            bid_structure, ask_structure = (participant
                                            .select_trading_strategy())
            if bid_structure is not None:
                for price, amount in bid_structure:
                    if price <= 0:
                        print(f"Bid of price {price} <= 0 from {participant}:{pid}"
                              " not allowed")
                    elif amount <= 0:
                        print(f"Bid of amount {amount} <= 0 from {participant}:{pid}"
                              " not allowed")
                    elif self.states[pid][1] + amount > 10:
                        print(f"Bid of amount {amount} > {10 - self.states[pid][1]}"
                              f" from {participant}:{pid} not allowed")
                    else:
                        bids.append((price, amount, pid))
            if ask_structure is not None:
                for price, amount in ask_structure:
                    if amount <= 0:
                        print(f"Ask of amount {amount} <= 0 from {participant}:{pid}"
                              " not allowed")
                    else:
                        asks.append((price, amount, pid))

        if bids == []:
            print("No buyers - no auction")
            return (0, None)
        if asks == []:
            print("No sellers - no auction")
            return (float('inf'), None)

        bids.sort()
        print(f"Bids: {bids}")
        asks.sort()
        print(f"Asks: {asks}")

        bid_progression = [bids[0][0]]
        for price, _, _ in bids:
            if price > bid_progression[-1]:
                bid_progression.append(price)

        ask_progression = [asks[0][0]]
        for price, _, _ in asks:
            if price > ask_progression[-1]:
                ask_progression.append(price)

        if ask_progression[-1] == 0:
            final_price = bid_progression[0]
        else:
            if ask_progression[0] == 0:
                marginal_bid = 0
                marginal_ask = 1
            else:
                marginal_bid = 0
                marginal_ask = 0

            if bid_progression[marginal_bid] < ask_progression[marginal_ask]:
                current_price = bid_progression[marginal_bid]
                marginal_bid += 1
            else:
                current_price = ask_progression[marginal_ask]
                marginal_ask += 1

            bid_amount = sum(x for p, x, _ in bids if p >= current_price)
            ask_amount = sum(x for p, x, _ in asks if p <= current_price)
            cleared_amount = min((bid_amount, ask_amount))

            print(f"Starting price: {current_price}")
            print(f"Starting amount: {cleared_amount}")
            previous_price = current_price
            previous_cleared = cleared_amount

            while cleared_amount >= previous_cleared:
                previous_cleared = cleared_amount
                previous_price = current_price
                if marginal_bid < len(bid_progression):
                    if marginal_ask < len(ask_progression):
                        if (
                                bid_progression[marginal_bid]
                                < ask_progression[marginal_ask]):
                            current_price = bid_progression[marginal_bid]
                            marginal_bid += 1
                        else:
                            current_price = ask_progression[marginal_ask]
                            marginal_ask += 1
                    else:
                        current_price = bid_progression[marginal_bid]
                        marginal_bid += 1
                elif marginal_ask < len(ask_progression):
                    current_price = ask_progression[marginal_ask]
                    marginal_ask += 1
                else:
                    break

                bid_amount = sum(x for p, x, _ in bids if p >= current_price)
                ask_amount = sum(x for p, x, _ in asks if p <= current_price)
                cleared_amount = min((bid_amount, ask_amount))

            final_price = previous_price

        print(f"Final price: {final_price}")

        bids_in_range = [x for x in bids if x[0] >= final_price]
        asks_in_range = [x for x in asks if x[0] <= final_price]
        print(f"Bids in range: {bids_in_range}")
        print(f"Asks in range: {asks_in_range}")

        ask_deficit = (sum(x for _, x, _ in bids_in_range)
                       - sum(x for _, x, _ in asks_in_range))
        print(f"Ask deficit: {ask_deficit}")

        while ask_deficit != 0:
            if ask_deficit < 0:
                tentative_matches = [x for x in asks_in_range
                                     if x[0] == asks_in_range[-1][0]]
                safe_matches = [x for x in asks_in_range
                                if x[0] < asks_in_range[-1][0]]
                print(f"Tentative matches: {tentative_matches}")

                match_population = []
                for price, amount, participant in tentative_matches:
                    for _ in range(amount):
                        match_population.append((price, 1, participant))

                lucky_picks = max((len(match_population)
                                  - abs(ask_deficit),
                                  0))
                lucky_matches = random.sample(match_population,
                                              lucky_picks)
                asks_in_range = safe_matches + lucky_matches
            elif ask_deficit > 0:
                tentative_matches = [x for x in bids_in_range
                                     if x[0] == bids_in_range[0][0]]
                safe_matches = [x for x in bids_in_range
                                if x[0] > bids_in_range[0][0]]
                print(f"Tentative matches: {tentative_matches}")

                match_population = []
                for price, amount, participant in tentative_matches:
                    for _ in range(amount):
                        match_population.append((price, 1, participant))

                lucky_picks = max((len(match_population)
                                   - abs(ask_deficit),
                                   0))
                lucky_matches = random.sample(match_population,
                                              lucky_picks)
                bids_in_range = safe_matches + lucky_matches
            ask_deficit = (sum(x for _, x, _ in bids_in_range)
                           - sum(x for _, x, _ in asks_in_range))
            print(f"Ask deficit: {ask_deficit}")

        assert(ask_deficit == 0)

        for _, amount, participant in bids_in_range:
            self.states[participant] = (self.states[participant][0]
                                        - final_price * amount,
                                        self.states[participant][1]
                                        + amount)
        for _, amount, participant in asks_in_range:
            self.states[participant] = (self.states[participant][0]
                                        + final_price * amount,
                                        self.states[participant][1]
                                        - amount)

        return (final_price, sum(x for _, x, _ in bids_in_range))

    def run_day(self):
        self.start_day()
        (todays_price, todays_amount) = self.run_auction()
        self.end_day()
        for participant, (gold, food) in zip(self.market_participants,
                                             self.states):
            participant.update(gold, food, todays_price, todays_amount)


if __name__ == "__main__":
    auction_house = Market([OnlyWorkStrategy(),
                            OnlyWorkStrategy(),
                            OnlyWorkStrategy(),
                            OnlyWorkStrategy(),
                            OnlyWorkStrategy(),
                            OnlyWorkStrategy(),
                            OnlyFarmStrategy(),
                            OnlyFarmStrategy(),
                            YesterdayTenPercentStrategy(),
                            TwodayTenPercentStrategy()])

    for _ in range(90):
        auction_house.run_day()
        print(auction_house.states)
