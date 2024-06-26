# Quant-Functions

Quant-Functions is a Python project that uses Azure Functions to fetch historical candlestick data from Binance and OKX exchanges. The data is fetched at various intervals: 15 minutes, 1 hour, 2 hours, 4 hours, 6 hours, 12 hours, 1 day, 1 week, etc. The fetched data is then stored in MongoDB for further analysis.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.8 or higher
- Azure Functions Core Tools
- MongoDB

### Installing

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository
2. Install the dependencies using pip:

```shell
pip install -r requirements.txt
```

3. Set up your Azure Functions environment
```shell
# Create a resource group named AzureFunctionsQuickstart-rg in your chosen region.
az group create --name AzureQuantFunctions-rg --location southeastasia

# Create a general-purpose storage account in your resource group and region.
az storage account create --name QuantStorageAccount --location southeastasia --resource-group AzureQuantFunctions-rg --sku Standard_LRS

# Create the function app in Azure.
az functionapp create --resource-group AzureQuantFunctions-rg --consumption-plan-location southeastasia --runtime python --runtime-version 3.10 --functions-version 4 --name quant-jobs --os-type linux --storage-account quantstorage1
```

4. Set up your MongoDB database

## Running the tests

Explain how to run the automated tests for this system.

## Deployment

Add additional notes about how to deploy this on a live system.

## Built With

- [Python](https://www.python.org/) - The programming language used
- [Azure Functions](https://azure.microsoft.com/en-us/services/functions/) - The serverless compute service used
- [MongoDB](https://www.mongodb.com/) - The database used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Your Name** - _Initial work_ - [YourGithubUsername](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/your-repo/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
