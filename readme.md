# Vast.ai XenBlocks Mining Assistant

Welcome to TreeCityWes.eth's Vast.ai XenBlocks Mining Assistant! This Python tool optimizes cryptocurrency mining on Vast.ai, helping you monitor instance stats, terminate non-profitable instances, and discover new lucrative offers.

## Features

- **Monitor Instance Stats:** Automatically fetch and display key metrics from your mining instances.
- **Kill Dead Instances:** Identify and terminate unprofitable instances, cutting unnecessary expenses.
- **Find New Offers:** Use advanced filtering to uncover the most cost-effective mining opportunities on Vast.ai.

## Getting Started

### Prerequisites

- Python 3.6 or later.
- A Vast.ai API key and wallet address configured via an .env file for secure access.

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/TreeCityWes/XenBlocks-Assistant.git
   cd XenBlocks-Assistant
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install --upgrade vastai;
   Login to Vast.ai API CLI: vastai set apikey (your API key)

![image](https://github.com/TreeCityWes/XenBlocks-Assistant/assets/93751858/baf6dee5-b940-4690-a7bc-360411f6e2e8)

   
   ```

3. **Configure .ENV File:**

   Create a `.env` file in the root directory of the project with your Vast.ai API key and wallet address. This file should contain the following lines:

   ```env
   API_KEY=your_vast_ai_api_key
   ADDR=your_wallet_address
   ```

   Replace `your_vast_ai_api_key` and `your_wallet_address` with the actual values you wish to use for mining.

### Usage

Run the script from the command line:

```bash
python vastmon.py
```

Follow the on-screen instructions to monitor your instances, terminate non-profitable ones, or find new offers.

### Support

For support, visit [HashHead.io](https://hashhead.io)

Or Buy Us A Coffee! 
- Smit: [buymeacoffee.com/smit1237](https://buymeacoffee.com/smit1237)
- Wes: [buymeacoffee.com/treecitywes](https://buymeacoffee.com/treecitywes)

This project is designed to work with Smit1237's XenBlocks Template on Vast.ai. 
For more details, refer to the template and Docker links provided.
