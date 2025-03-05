import numpy as np
import matplotlib.pyplot as plt

class Option:
    def __init__(self):
        # Now store multiple legs for each type in a list
        self.long_call = []
        self.short_call = []
        self.long_put = []
        self.short_put = []

    # Evaluate the strategy by passing stock price s
    def evaluate(self, s):
        result = 0
        # Sum all long_call payoffs
        result += sum([lc(s) for lc in self.long_call])
        # Sum all short_call payoffs
        result += sum([sc(s) for sc in self.short_call])
        # Sum all long_put payoffs
        result += sum([lp(s) for lp in self.long_put])
        # Sum all short_put payoffs
        result += sum([sp(s) for sp in self.short_put])
        return result

    # Plot the strategy payoff over a range of stock prices
    def plot(self, stock_price_range, strategy_name=None):
        # Create an array of stock prices in the range (min, max)
        stock_prices = np.linspace(stock_price_range[0], stock_price_range[1], 100)
        
        # Evaluate the strategy for each stock price
        payoffs = [self.evaluate(s) for s in stock_prices]

        if strategy_name is None:
            strategy_name = "Option Strategy"

        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.plot(stock_prices, payoffs, label=f"{strategy_name} Payoff")
        plt.xlabel('Stock Price (S)')
        plt.ylabel('Payoff')
        plt.title(f'{strategy_name} Payoff vs. Stock Price')
        plt.axhline(0, color='black',linewidth=0.5)  # Add a line at y=0 for reference
        plt.grid(True)
        plt.legend()
        plt.show()


class OptionBuilder:
    def __init__(self):
        self.option = Option()

    def build_long_call(self, k, p):
        # Append a new long call leg to the list
        self.option.long_call.append(lambda s: max((s - k), 0) - p)
        return self

    def build_short_call(self, k, p):
        # Append a new short call leg to the list
        self.option.short_call.append(lambda s: p - max((s - k), 0))
        return self

    def build_long_put(self, k, p):
        # Append a new long put leg to the list
        self.option.long_put.append(lambda s: max((k - s), 0) - p)
        return self

    def build_short_put(self, k, p):
        # Append a new short put leg to the list
        self.option.short_put.append(lambda s: p - max((k - s), 0))
        return self

    def build(self):
        return self.option


# Example: Building a butterfly spread strategy with puts
if __name__ == '__main__':
    builder = OptionBuilder()

    # Define the strikes and premiums
    k_long_put = 50  # Strike price for long put
    p_long_put = 5   # Premium for long put

    k_short_put = 55  # Strike price for short put
    p_short_put = 3   # Premium for short put
    
    k_long_put_2 = 60  # Strike price for another long put
    p_long_put_2 = 3   # Premium for the second long put

    # Build the option strategy (butterfly spread using puts)
    option_strategy = (
        builder.build_long_put(k_long_put, p_long_put)
               .build_short_put(k_short_put, p_short_put)
               .build_short_put(k_short_put, p_short_put)
               .build_long_put(k_long_put_2, p_long_put_2)
               .build()
    )

    # Evaluate the strategy at a given stock price
    stock_price = 0 
    result = option_strategy.evaluate(stock_price)
    print(f"Option strategy result at stock price {stock_price}: {result}")
    
    # Plot the strategy over a range of stock prices
    option_strategy.plot(stock_price_range=(0, 80), strategy_name="Butterfly_Puts")
