# Intellihub SDK (Python)

[![](https://intellihub.ai/static/img/logo-high.png)](https://intellihub.ai)
Intellihub renders a comprehensive spectrum of solutions that can be accessed by users on-demand from our pool of transformational technologies.

### Installation

Intellihub SDK requires Python 3.5 + . Go to https://intellihub.ai and create an app. On creation of an app, you will get an API Key.

```sh
import intellihub
c = intellihub.IntellihubClient('API Key')
response = c.sentiment_analysis('I am feeling good.')
print(response)
```

For more details, visit https://intellihub.ai
