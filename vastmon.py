import requests
import threading
from tabulate import tabulate
import logging
import subprocess
import json
from prettytable import PrettyTable
import os
from dotenv import load_dotenv
import platform

logging.basicConfig(level=logging.INFO)
load_dotenv()  

API_KEY = os.getenv('API_KEY')
ADDR = os.getenv('ADDR')

def get_instances_with_stats(api_key):
    instances = get_instances(api_key)  
    instance_stats = {}  
    threads = []  
    for instance in instances:
        thread = threading.Thread(target=scrape_data_into_instance, args=(instance, instance_stats))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()  

    for instance in instances:
        instance_id = instance['id']
        if instance_id in instance_stats:
            instance.update(instance_stats[instance_id])
        else:
            instance['Status'] = "Loaded"
    return instances

def display_splash_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    splash_screen = """
\033[92m,.  ,.         ,-,---. .                 
` \/   ,-. ,-.  '|___/ |  ,-. ,-. . , ,-.
  /\   |-' | |  ,|   \\ |  | | |   |/  `-.
`'  `' `-' ' ' `-^---' `' `-' `-' |\\  `-'                                                                                       
                                  ' `    

    ,.                 .          .      
   / |   ,-. ,-. . ,-. |- ,-. ,-. |-     
  /~~|-. `-. `-. | `-. |  ,-| | | |      
,'   `-' `-' `-' ' `-' `' `-^ ' ' `-'     



Welcome to TreeCityWes.eth's Vast.ai XenBlocks Mining Assistant 

    - Remember to create .ENV file with Wallet Address and API variables

    - Open-source with No Fee collection - https://github.com/TreeCityWes/XenBlocks-Assistant 

    - Visit https://HashHead.io or https://buymeacoffee.com/treecitywes for more info



This script is designed to work with Smit1237's XenBlocks Template on Vast.ai

    - Template: https://cloud.vast.ai/?ref_id=88736&t...

    - Docker: https://hub.docker.com/r/smit1237/xen...

    - Vast.ai Sign-Up: https://cloud.vast.ai/?ref_id=88736


\033[0m"""
    print(splash_screen)
    input("\033[92mHit Enter to continue...\033[0m")

display_splash_screen()

def get_instances(api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://console.vast.ai/api/v0/instances"
    instances = []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        for instance in data.get('instances', []):
            instance_id = instance.get('id')
            public_ipaddr = instance.get('public_ipaddr', '').strip()
            external_port = instance.get('ports', {}).get('8080/tcp', [{}])[0].get('HostPort', 'N/A')
            cost_per_hour = instance.get('dph_total', 0)
            gpu_name = instance.get('gpu_name', 'N/A')

            instances.append({
                'id': instance_id,
                'public_ipaddr': public_ipaddr,
                'external_port': external_port,
                'cost_per_hour': cost_per_hour,
                'gpu_name': gpu_name
            })
    except requests.RequestException as e:
        logging.error(f"Error fetching instances: {e}")
    return instances

def scrape_data_into_instance(instance, instance_stats):
    instance_id = instance['id']
    if instance['external_port'] == 'N/A':
        logging.info(f"Data scraping skipped for instance {instance_id} due to unavailable external port.")
        instance_stats[instance_id] = {"Status": "Data scraping skipped"}
        return
    instance_url = f"http://{instance['public_ipaddr']}:{instance['external_port']}"
    ajax_url = f"{instance_url}/data"
    try:
        response = requests.get(ajax_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            instance_stats[instance_id] = {
                "Data": data,
                "Status": "Loaded",
                "Hashrate_per_Dollar": data.get('hashrate_count', 0) / instance['cost_per_hour'] if instance['cost_per_hour'] > 0 else 0
            }
        else:
            instance_stats[instance_id] = {"Status": "Failed to scrape data"}
            logging.info(f"Failed to scrape data from {ajax_url} for instance {instance_id}: Status code {response.status_code}")
    except Exception as e:
        instance_stats[instance_id] = {"Status": "Error scraping data"}
        logging.error(f"Error scraping data from {ajax_url} for instance {instance_id}: {e}")

def display_instances_and_stats(instances):
    headers = ["Instance ID", "GPU Type", "Cost", "Hashrate", "Hashrate/$", "XNM", "X.BLK", "XUNI", "Link"]
    table = PrettyTable()
    table.field_names = headers
    table.align = "l"
    table.float_format = ".2"

    total_hashrate = 0
    total_cost = 0
    total_xnm = 0
    total_xblk = 0
    total_xuni = 0

    sorted_instances = sorted(instances, key=lambda x: -x.get('Hashrate_per_Dollar', 0))

    for instance in sorted_instances:
        stats = instance.get('Data', {})
        status = instance.get('Status', 'Error')
        gpu_type = instance.get('gpu_name', 'N/A')
        link = f"http://{instance.get('public_ipaddr')}:{instance.get('external_port')}" if instance.get('external_port') != 'N/A' else 'N/A'

        if status == "Loaded":
            hashrate_count = stats.get('hashrate_count', 0)
            hash_per_dollar = instance.get('Hashrate_per_Dollar', 0)
            xnm = stats.get('regularblock_count', 0)
            xblk = stats.get('superblock_count', 0)
            xuni = stats.get('xuniblock_count', 0)
            cost = instance.get('cost_per_hour', 0)

            total_hashrate += hashrate_count
            total_cost += cost
            total_xnm += xnm
            total_xblk += xblk
            total_xuni += xuni

            color_code = get_color_for_hashrate_per_dollar(hash_per_dollar)
            row = [
                color_code + str(instance.get('id')) + "\033[0m",
                color_code + str(gpu_type) + "\033[0m",
                color_code + f"${cost:.3f}" + "\033[0m",
                color_code + str(hashrate_count) + "\033[0m",
                color_code + f"{hash_per_dollar:.2f}" + "\033[0m",
                color_code + str(xnm) + "\033[0m",
                color_code + str(xblk) + "\033[0m",
                color_code + str(xuni) + "\033[0m",
                color_code + link + "\033[0m"
            ]
        else:
            color_code = "\033[91m"
            row = [
                color_code + str(instance.get('id')) + "\033[0m",
                color_code + str(gpu_type) + "\033[0m",
                color_code + f"${instance.get('cost_per_hour', 0):.3f}" + "\033[0m",
                color_code + "-" + "\033[0m",
                color_code + "-" + "\033[0m",
                color_code + "-" + "\033[0m",
                color_code + "-" + "\033[0m",
                color_code + "-" + "\033[0m",
                color_code + link + "\033[0m"
            ]
        
        table.add_row(row)

    total_hashrate_per_dollar = total_hashrate / total_cost if total_cost > 0 else 0

    table.add_row(["-"*len(header) for header in headers])

    totals_row = [
        "\033[92mTotals\033[0m",
        "-",
        f"\033[92m${total_cost:.3f}\033[0m",
        f"\033[92m{total_hashrate}\033[0m",
        f"\033[92m{total_hashrate_per_dollar:.2f}\033[0m",
        f"\033[92m{total_xnm}\033[0m",
        f"\033[92m{total_xblk}\033[0m",
        f"\033[92m{total_xuni}\033[0m",
        "-"
    ]
    table.add_row(totals_row)

    print(table)



def run_vastai_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.stderr:
            print("Error:", result.stderr.strip())
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"success": False, "error": "Loading...", "stdout": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"Command execution failed: {e}"}


def display_instances_for_termination(instances):
    sorted_instances = sorted(instances, key=lambda x: -x.get('Hashrate_per_Dollar', 0))

    headers = ["Number", "Instance ID", "GPU Type", "Cost", "Hashrate", "Hashrate/$", "XNM", "X.BLK", "XUNI", "Link"]
    table = PrettyTable()
    table.field_names = headers
    table.align = "l"
    table.float_format = ".2"

    for idx, instance in enumerate(sorted_instances, start=1):
        stats = instance.get('Data', {})
        hashrate = stats.get('hashrate_count', 'N/A')
        hash_per_dollar = instance.get('Hashrate_per_Dollar', 'N/A')
        xnm = stats.get('regularblock_count', 'N/A')
        xblk = stats.get('superblock_count', 'N/A')
        xuni = stats.get('xuniblock_count', 'N/A')
        cost = instance.get('cost_per_hour', 'N/A')

        color_code = get_color_for_hashrate_per_dollar(hash_per_dollar) if hashrate != 'N/A' else "\033[91m"

        row = [
            f"\033[0m{idx}\033[0m",
            color_code + str(instance['id']) + "\033[0m",
            color_code + str(instance.get('gpu_name', 'N/A')) + "\033[0m",
            color_code + (f"${float(cost):.2f}" if cost != 'N/A' else "N/A") + "\033[0m",
            color_code + str(hashrate) + "\033[0m",
            color_code + (f"{hash_per_dollar}" if hash_per_dollar != 'N/A' else "N/A") + "\033[0m",
            color_code + str(xnm) + "\033[0m",
            color_code + str(xblk) + "\033[0m",
            color_code + str(xuni) + "\033[0m",
            color_code + (f"http://{instance.get('public_ipaddr')}:{instance.get('external_port')}" if instance.get('external_port') != 'N/A' else "N/A") + "\033[0m"
        ]
        table.add_row(row)

    print("\nInstances Available for Termination:")
    print(table)

def handle_instance_termination(api_key, instances):
    display_instances_for_termination(instances)
    
    while True:
        user_choice = input("Choose 'K' to kill dead instances, 'I' to select instances, or 'X' to exit: ").upper()

        if user_choice == 'K':
            kill_dead_instances(api_key, instances)
            break
        elif user_choice == 'I':
            kill_selected_instances(api_key, instances)
            break
        elif user_choice == 'X':
            print("Returning to main menu.")
            break
        else:
            print("Invalid option, please try again.")

def kill_dead_instances(api_key, instances):
    dead_instance_ids = []
    for instance in instances:
        hashrate = instance.get('Data', {}).get('hashrate_count', 0)
        status = instance.get('Status', 'N/A')
        if hashrate == 0 or status not in ['Loaded', 'Running']:
            dead_instance_ids.append(instance['id'])
    
    if dead_instance_ids:
        print("\nIdentified dead instances for termination:")
        for instance_id in dead_instance_ids:
            print(f"Instance ID: {instance_id}")
        confirm = input("\nConfirm termination of all identified dead instances? (y/n): ").lower()
        
        if confirm.startswith('y'):
            kill_instances(api_key, dead_instance_ids)
        else:
            print("Operation cancelled.")
    else:
        print("No dead instances identified for termination.")

def kill_selected_instances(api_key, instances):
    display_instances_for_termination(instances)
    
    sorted_instances = sorted(instances, key=lambda x: -x.get('Hashrate_per_Dollar', 0))

    instance_numbers_str = input("Enter the numbers of the instances to kill, or a range (e.g., '1, 2, 4' or '7-10'): ")
    instance_numbers = []
    for part in instance_numbers_str.split(","):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            instance_numbers.extend(range(start, end + 1))  
        elif part.isdigit():
            instance_numbers.append(int(part))

    instance_numbers = [num for num in sorted(set(instance_numbers)) if 1 <= num <= len(sorted_instances)]

    selected_instance_ids = [sorted_instances[num-1]['id'] for num in instance_numbers]

    if selected_instance_ids:
        print("\nSelected Instances for Termination:")
        for instance_id in selected_instance_ids:
            print(f"Instance ID: {instance_id}")
        
        confirm = input("\nConfirm termination of all selected instances? (y/n): ").lower()
        
        if confirm.startswith('y'):
            kill_instances(api_key, selected_instance_ids)
        else:
            print("Operation cancelled.")
    else:
        print("No valid instances selected for termination.")

def kill_instances(api_key, instance_ids):
    for instance_id in instance_ids:
        print(f"Attempting to terminate instance {instance_id}...")
        command = ["vastai", "destroy", "instance", str(instance_id), "--api-key", api_key]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if result.returncode == 0:
                print(f"Instance {instance_id} terminated successfully.")
            else:
                print(f"Failed to terminate instance {instance_id}.")
        except subprocess.CalledProcessError as e:
            print(f"Error terminating instance {instance_id}: {e}")

def create_instance(offer_id, price):
    command = [
        "vastai", "create", "instance", str(offer_id),
        "--price", str(price),
        "--image", "smit1237/xengpuminer:vast",
        "--env", f"-e ADDR={ADDR}",
        "--args", "--args ...",
        "--api-key", API_KEY,
        "--raw"
    ]

    result = run_vastai_command(command)
    table = PrettyTable()
    table.field_names = ["Offer ID", "Response from Vast.ai", "State"]

    if result:
        response_from_vast = "Started"
        state = "Success: True" if result.get('success') else "Success: False"
        table.add_row([
            f"\033[92m{offer_id}\033[0m",
            f"\033[92m{response_from_vast}\033[0m",
            f"\033[92m{state}\033[0m"
        ])
    else:
        table.add_row([
            f"\033[92m{offer_id}\033[0m",
            "\033[92mFailed to receive proper response\033[0m",
            "\033[92mN/A\033[0m"
        ])

    print(table)

def search_top_offers(criterion='dph_total'):
    query = "verified=false rented=false"
    command = ["vastai", "search", "offers", query, "--interruptible", "--raw"]
    offers = run_vastai_command(command)
    if offers:
        if criterion == 'dph_total':
            sorted_offers = sorted(offers, key=lambda x: x.get(criterion, float('inf')))
        else:
            sorted_offers = sorted(offers, key=lambda x: x.get(criterion, float('-inf')), reverse=True)
        return sorted_offers[:10]
    return []

def print_offers(offers):
    if not offers:
        print("No offers to display.")
        return
    table = PrettyTable()
    table.field_names = ["Number", "ID", "GPU", "Price/hr", "Total TFLOPS", "TFLOPS/$", "Location"]
    table.align = "l"
    for idx, offer in enumerate(offers, start=1):
        table.add_row([
            f"\033[92m{idx}\033[0m",
            f"\033[92m{offer['id']}\033[0m",
            f"\033[92m{offer['gpu_name'].replace('_', ' ')}\033[0m",
            f"\033[92m${offer['dph_total']:.3f}\033[0m",
            f"\033[92m{offer['total_flops']:.2f}\033[0m",
            f"\033[92m{offer['flops_per_dphtotal']:.2f}\033[0m",
            f"\033[92m{offer.get('geolocation', 'Unknown')}\033[0m"
        ])
    print(table)

def parse_selection(input_str):
    """
    Parses a string input like '1-3,5' into a list of numbers [1, 2, 3, 5].
    """
    selection = set()
    for part in input_str.split(","):
        if '-' in part:
            start, end = map(int, part.split('-'))
            selection.update(range(start, end + 1))
        else:
            selection.add(int(part))
    return sorted(selection)

def get_color_for_hashrate_per_dollar(hashrate_per_dollar):
    if hashrate_per_dollar == 0 or hashrate_per_dollar == 'Error':
        return "\033[91m"  
    elif 1 <= hashrate_per_dollar < 20000:
        return "\033[93m" 
    elif hashrate_per_dollar >= 20000:
        return "\033[92m"  
    else:
        return "\033[0m"  

def main():
    while True:
        print("\nMain Menu:")
        print("1. View Running Instances and Their Stats")
        print("2. Kill an Instance(s)")
        print("3. Buy an Instance")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            instances = get_instances_with_stats(API_KEY)
            display_instances_and_stats(instances)
        elif choice == "2":
            instances = get_instances_with_stats(API_KEY)
            handle_instance_termination(API_KEY, instances)
        elif choice == "3":
            while True:  
                print("\nSelect the type of top 10 GPU offers to view:")
                print("1. Lowest Price/hr")
                print("2. Highest Total TFLOPS")
                print("3. Highest TFLOPS/$")
                print("4. Exit to previous menu")
                offer_type = input("Enter your choice: ").upper()  

                if offer_type == '4':
                    break  

                criterion_map = {'1': 'dph_total', '2': 'total_flops', '3': 'flops_per_dphtotal'}
                criterion = criterion_map.get(offer_type)
                
                if criterion:
                    print(f"\nFetching the top 10 GPU offers based on {criterion}...")
                    top_offers = search_top_offers(criterion)
                    if top_offers:
                        print_offers(top_offers)
                        offer_selection = input("\nEnter the numbers of the offers to purchase, 'R' to refresh prices, or 'X' to exit to the previous menu: ").upper()

                        if offer_selection == 'X':
                            break  
                        elif offer_selection == 'R':
                            continue
                        else:
                            selected_indices = parse_selection(offer_selection)
                            selected_offers = [top_offers[idx - 1] for idx in selected_indices if 1 <= idx <= len(top_offers)]
                            
                            for selected_offer in selected_offers:
                                print(f"Purchasing offer ID {selected_offer['id']}...")
                                print()
                                print()
                                create_instance(selected_offer['id'], selected_offer['dph_total'])
                                print()
                                print()
                                
                else:
                    print("Invalid option, please try again.")

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
