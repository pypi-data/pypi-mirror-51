# Chaintrail API Wrapper

Installation

```bash
pip3 install chaintrailapi
```

Import and use the package as demonstrated in `example.py` below:

```python
from chaintrailapi import ChainTrail, Accounts, Dataset
import matplotlib.pyplot as plt

api = ChainTrail("localhost:3000", Dataset.JAN_2019)

account_data = api.get_accounts(['acct_address'])
account_scaled = api.get_accounts(['tx_count','avg_tx_in','avg_tx_out','std_tx_in','std_tx_out']).get_scaled()

print(account_scaled.shape)

pcadata = ChainTrail.calculate_pca(account_scaled, components=2)
inliers, outliers, xx, yy, z_train = ChainTrail.predict_outliers(pcadata)

# plot the training points
plt.contour(xx,yy,z_train, levels=[0], linewidths=2, colors='darkred')
plt.scatter(pcadata[inliers,0], pcadata[inliers,1], color='blue', alpha=0.2)
plt.scatter(pcadata[outliers,0], pcadata[outliers,1], color='red', alpha=0.4)
plt.show()
```
