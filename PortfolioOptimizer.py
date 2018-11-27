import quandl
import numpy as np

class PortfolioOptimizer:
	def __init__(self, api_key, stock_list):
		self.stock_list = stock_list
		self.mean_daily_returns = None
		self.cov_matrix = None
		
		quandl.ApiConfig.api_key = api_key
		
		data = quandl.get_table(
			"WIKI/PRICES",
			ticker = stock_list,
			qopts = {"columns":['date', 'ticker', 'adj_close']},
			date = {"gte":"2017-1-1", "lte":"2018-1-1"}, paginate=True
		)

		df = data.set_index("date")
		df = df.pivot(columns='ticker')

		df.fillna(method='ffill', inplace=True)
		df.fillna(method='backfill', inplace=True)
  
		daily_returns = df.pct_change()
		daily_returns = daily_returns[1:]

		self.mean_daily_returns = daily_returns.mean()
		self.cov_matrix = daily_returns.cov()
			
		
	def annual_performance(self, mean_daily_returns, allocs, cov_matrix):
	  returns = np.sum(mean_daily_returns * allocs) * 252
	  std = np.sqrt(np.dot(np.array(allocs).T, np.dot(cov_matrix, allocs))) * np.sqrt(252)
	  return returns, std
	  
	def sharpe_ratio(self, portfolio_returns, portfolio_std, risk_free_rate):
		return (portfolio_returns - risk_free_rate) / (portfolio_std)
		
	def optimize_sharpe_ratio(self, risk_free_rate, num_portfolios=1000):
		weights_list = []
		sharpe_list = []

		for i in range(num_portfolios):
			weights = np.random.random(len(self.mean_daily_returns))
			weights /= np.sum(weights)
			
			returns, std = self.annual_performance(self.mean_daily_returns, weights, self.cov_matrix)
			sharpe = self.sharpe_ratio(returns, std, risk_free_rate)
			
			weights_list.append(weights)
			sharpe_list.append(sharpe)
			
		best_sharpe_index = sharpe_list.index(max(sharpe_list))
		best_sharpe_weights = weights_list[best_sharpe_index]
	
		print("-" * 60)
		print("  OPTIMIZED SHARPE RATIO")
		print("\n")
		for i in range(len(self.stock_list)):
			print("\t{} \t-\t {}%".format(self.stock_list[i], round(best_sharpe_weights[i] * 100)))
			
		print("\n")
		print("  Sharpe Ratio: \t{}".format(sharpe_list[best_sharpe_index]))	
		print("  Annual Return: \t{}%".format(round(self.annual_performance(self.mean_daily_returns, weights_list[best_sharpe_index], self.cov_matrix)[0] * 100)))
		print("  Volatility: \t\t{}".format(self.annual_performance(self.mean_daily_returns, weights_list[best_sharpe_index], self.cov_matrix)[1]))
		print("-" * 60)
					
	def optimize_returns(self, risk_free_rate, num_portfolios=1000):
		weights_list = []
		returns_list = []

		for i in range(num_portfolios):
			weights = np.random.random(len(self.mean_daily_returns))
			weights /= np.sum(weights)
			
			returns, std = self.annual_performance(self.mean_daily_returns, weights, self.cov_matrix)
			
			weights_list.append(weights)
			returns_list.append(returns)
			
		best_returns_index = returns_list.index(max(returns_list))
		best_returns_weights = weights_list[best_returns_index]
	
		print("-" * 60)
		print("  OPTIMIZED SHARPE RATIO")
		print("\n")
		for i in range(len(self.stock_list)):
			print("\t{} \t-\t {}%".format(self.stock_list[i], round(best_returns_weights[i] * 100)))
			
		print("\n")
		print("  Sharpe Ratio: \t{}".format(returns_list[best_returns_index]))	
		print("  Annual Return: \t{}%".format(round(self.annual_performance(self.mean_daily_returns, weights_list[best_returns_index], self.cov_matrix)[0] * 100)))
		print("  Volatility: \t\t{}".format(self.annual_performance(self.mean_daily_returns, weights_list[best_returns_index], self.cov_matrix)[1]))
		print("-" * 60)
		

	def optimize_risk(self, risk_free_rate, num_portfolios=1000):
		weights_list = []
		std_list = []

		for i in range(num_portfolios):
			weights = np.random.random(len(self.mean_daily_returns))
			weights /= np.sum(weights)
			
			returns, std = self.annual_performance(self.mean_daily_returns, weights, self.cov_matrix)
			
			weights_list.append(weights)
			std_list.append(std)
			
		best_std_index = std_list.index(min(std_list))
		best_std_weights = weights_list[best_std_index]
	
		print("-" * 60)
		print("  OPTIMIZED SHARPE RATIO")
		print("\n")
		for i in range(len(self.stock_list)):
			print("\t{} \t-\t {}%".format(self.stock_list[i], round(best_std_weights[i] * 100)))
			
		print("\n")
		print("  Sharpe Ratio: \t{}".format(std_list[best_std_index]))	
		print("  Annual Return: \t{}%".format(round(self.annual_performance(self.mean_daily_returns, weights_list[best_std_index], self.cov_matrix)[0] * 100)))
		print("  Volatility: \t\t{}".format(self.annual_performance(self.mean_daily_returns, weights_list[best_std_index], self.cov_matrix)[1]))
		print("-" * 60)
		
if __name__ == "__main__":
	p = PortfolioOptimizer("1sof-3kR9pZ25SpEjN55", ["AAPL", "FB"])
	p.optimize_sharpe_ratio(0.017)
	p.optimize_returns(0.017)
	p.optimize_risk(0.017)

