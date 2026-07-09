# Wasserstein-AAPL.py adapted by Gemini / Reporting:  RWU/05-07-2026
import numpy as np
import scipy.stats as stats

# 1. Simulate AAPL deviation data sets (Pre- and Post-Shock)
np.random.seed(42)
# Pre-shock period: Clean Gaussian trading noise
dev_pre = np.random.normal(loc=0.0, scale=8.0, size=200) 
# Post-shock period: Slightly wider spread due to short-term nervosity
dev_post = np.random.normal(loc=0.5, scale=9.5, size=105) 

# 2. Compute the Empirical Wasserstein Distance (W1)
# This calculates the exact integrated area between the 2 sample CDFs
w1_observed = stats.wasserstein_distance(dev_pre, dev_post)
print(f"Observed Kantorovich-Wasserstein Distance:\n"+
       f"(W1):{w1_observed:.4f}EUR")

# 3. Parametric Bootstrap: Is the distance due to pure random chance?
# Pool data to find baseline parameters under the Null Hypothesis
pooled_data = np.concatenate([dev_pre, dev_post])
mu_hat, sigma_hat = stats.norm.fit(pooled_data)

bootstrap_w1s = []
n_pre, n_post = len(dev_pre), len(dev_post)

# Simulate 2,000 baseline scenarios with no structural change
for _ in range(2000):
    sim_pre = np.random.normal(mu_hat, sigma_hat, size=n_pre)
    sim_post = np.random.normal(mu_hat, sigma_hat, size=n_post)
    bootstrap_w1s.append(stats.wasserstein_distance(sim_pre, sim_post))

# 4. Calculate empirical p-value
p_value = np.mean(np.array(bootstrap_w1s) >= w1_observed)
print(f"Bootstrap p-value: {p_value:.4f}")

# 5. And here is the famous Wasserstein-Test:

if p_value < 0.05:
    print("Decision: REJECT the null hypothesis.\n" +
          "The market's geometry shifted significantly.")
else:
    print("Decision: ACCEPT the null hypothesis.\n" +
          "Barycenter change is within random sampling noise.")
