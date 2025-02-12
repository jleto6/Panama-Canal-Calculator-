#!/usr/bin/env python3

cost_per_gallon = 0.0002 # approximate dollar cost per gallon of water
transits_per_year = 14000 # approximate amount of transits in the Panama canal per year

def main():

    # Data for each lock
    panamax_lock_data = {
        "lock_name": "Panamax",  
        "lock_volume": 50_000_000,  # Total lock volume in gallons
        "water_lost" : 100 # Percentage of water lost based on water saving mechanisms
    }
    neopanamax_lock_data = {
        "lock_name": "Neopanamax",  
        "lock_volume": 38_000_000,  # Total lock volume in gallons
        "water_lost" : 55 # Percentage of water lost based on water saving mechanisms

    }

    # Inputs
    ship_size = int(input("Ship Tonnage: "))
    lock_type = input("Lock Type (Panamax or Neopanamax): ").lower()
        
        
    print("")
    print("---------------------------------------------")
    print("")

    # If using Panamax lock
    if (lock_type == "panamax"):
        lock_calculation(panamax_lock_data, ship_size)
    # If using Neopanamax lock
    elif (lock_type == "neopanamax"):
        lock_calculation(neopanamax_lock_data, ship_size)
    # Compare all
    elif (lock_type == "all"):
        lock_calculation(panamax_lock_data, ship_size)
        lock_calculation(neopanamax_lock_data, ship_size)


def lock_calculation(lock_data, ship_size):

    print("")
    print(f"Data for {lock_data['lock_name']} lock with a {ship_size} ton ship:")
    print("")

    # Amount of water a ship will displace based on tonnage
    water_displaced = ship_size * 240 #one ton displaces approximately 240 gallons of water
    print(f"{format_number(water_displaced)} gallons of water displaced per lock")

    # Subtract ship displacement from lock volume to get water needed
    water_needed = lock_data['lock_volume'] - water_displaced
    print(f"{format_number(water_needed)} gallons of water needed per lock (since the ship displaces water, less additional water is required to fill the lock)")

    # Calculate percentage of water saved based on ship displacement
    percent_savings = (water_displaced / (lock_data['lock_volume'])) * 100

    # Calculate water lost based on water needed and water saving mechanisms
    water_lost = water_needed * (lock_data['water_lost'] / 100)
    print(f"{format_number(water_lost)} gallons of water lost per lock (water not recycled)")

    # Calculate cost based on water needed
    cost_per_lock = water_needed * cost_per_gallon
    print(f"{format_number(cost_per_lock)} dollars of water per lock")


    # Calculations for a full transit
    print("")
    print(f"{format_number(water_displaced * 6)} gallons of water displaced for 1 full transit")
    print(f"{format_number(water_needed * 6)} gallons of water needed for 1 full transit (since the ship displaces water, less additional water is required to fill the lock)")
    print(f"{format_number((water_lost * 6))} gallons of water lost for 1 full transit (water not recycled)")
    print(f"{percent_savings:.0f}% savings of water per lock because of water displaced (since the ship takes up space in the lock, it reduces the amount of additional water needed)")
    print(f"{format_number(cost_per_lock * 6)} dollars of water for 1 full transit")
    print("")

    # Annual calculations
    # for a {ship_size} ton ship in {lock_type} locks:
    #annual_savings = (water_displaced * 6) * transits_per_year 
    #print(f"{format_number(annual_savings)} gallons of water saved per year based on a {ship_size} ton ship")



def format_number(n):

    n = round(n)

    if n > 1_000_000_000_000:
        return (f"{n / 1_000_000_000_000} trillion")
    elif n > 1_000_000_000:
        return (f"{n / 1_000_000_000} billion")
    elif n > 1_000_000:
        return (f"{n / 1_000_000} million")
    elif n > 1_000:
        return (f"{n / 1_000} thousand")
    else: 
        return n

if __name__ == "__main__":
    main()