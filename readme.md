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
   pip install --upgrade vastai
   vastai set apikey (your API key)
   ```

   ![image](https://github.com/TreeCityWes/XenBlocks-Assistant/assets/93751858/bdfb2499-0cd7-405a-a552-a0330c6690cc)

3. **Configure .ENV File:**
   Create a `.env` file in the root directory of the project with your Vast.ai API key and wallet address.

   This file should contain the following lines:
   ```
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

### Running Image On Local Machine 
```bash
# First, install some required libraries by following the first two steps at:
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

# Install Docker
sudo apt install docker.io

# After installation, add your user to the Docker group
sudo usermod -aG docker your_username

# Reboot the machine (safest way)
sudo reboot

# Execute the Docker command with your Xenblocks address. Make sure to replace 'your_username' with your actual username
# and 'your_xenblocks_address' with your actual Xenblocks address.
docker run -it -d --restart unless-stopped -p 2222:22 -p 8080:8080 -p 8000:8000 --gpus=all -e ADDR=your_xenblocks_address smit1237/xengpuminer:vast

# This command downloads an image (3.7 gigabytes in size) with all you need to mine. 
# After it's done, it will start mining. You can observe a nice and simple web UI on http://your_mining_machine_ip:8080.
# You can safely reboot the machine; mining will start automatically unless you stop it.
```

### Support

For support, visit [HashHead.io](https://hashhead.io)

Or Buy Us A Coffee! 
- Smit: [buymeacoffee.com/smit1237](https://buymeacoffee.com/smit1237)
- Wes: [buymeacoffee.com/treecitywes](https://buymeacoffee.com/treecitywes)

This project is designed to work with Smit1237's XenBlocks Template on Vast.ai. 
For more details, refer to the template and Docker links provided.
