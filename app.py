from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "dev"  # Required for session to work

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Check if 'ship_size' is in the form (user submitted the main form)
    if 'ship_size' in request.form:
        ship_size = (request.form.get('ship_size', 0).replace(',', ''))
        ship_size = int(ship_size) if ship_size.isdigit() else 0
        session['ship_size'] = ship_size  # Store it in session
    else:
        # If no ship_size is submitted, use the last saved value
        ship_size = session.get('ship_size', 50000)  # Default to 50,000 if missing

    amount_type = (request.form.get('amount', 'per_lock')) # Transit amount to be displayed

    panamax_lock_data = {
        "lock_name": "Panamax",  
        "lock_volume": 50_000_000,  # Total lock volume in gallons
        "water_lost": 100  # Percentage of water lost
    }
    neopanamax_lock_data = {
        "lock_name": "Neopanamax",  
        "lock_volume": 38_000_000,  # Total lock volume in gallons
        "water_lost": 55  # Percentage of water lost
    }

    # Calculate BOTH Per Lock and Per Transit values in one request
    result = {
        "Panamax": {
            "per_lock": lock_calculation(panamax_lock_data, ship_size, 'per_lock'),
            "per_transit": lock_calculation(panamax_lock_data, ship_size, 'per_transit')
        },
        "Neopanamax": {
            "per_lock": lock_calculation(neopanamax_lock_data, ship_size, 'per_lock'),
            "per_transit": lock_calculation(neopanamax_lock_data, ship_size, 'per_transit')
        }
    }

    return render_template('index.html', result=result, amount_type='per_lock')

def lock_calculation(lock_data, ship_size, amount_type):

    # Lock data
    cost_per_gallon = 0.0002 # approximate dollar cost per gallon of water
    transits_per_year = 14000 # approximate amount of transits in the Panama canal per year

    # Ship displacement calculation
    water_displaced = ship_size * 240  # One ton displaces ~240 gallons
    water_needed = lock_data['lock_volume'] - water_displaced
    water_lost = water_needed * (lock_data['water_lost'] / 100)
    cost_per_lock = water_needed * cost_per_gallon

     

    if amount_type == 'per_lock':
        # Full transit calculations (6 locks)
        results = {
            #"Ship Size": ship_size,
            "Water Displaced Per Lock": {
                "value": format_number(water_displaced),
                "tooltip": "Total water displaced by the ship as it enters the lock. Larger ships displace more water, reducing the additional water needed to fill the lock."
            },

            "Water Needed Per Lock": {
                "value" : format_number(water_needed),
                "tooltip" : "Additional water needed to raise the ship to the next level after accounting for displacement."
            },

            "Water Lost Per Lock": {
                "value": format_number(water_lost),
                "tooltip": "Water that drains out of the system and isn't recycled. Some locks use water-saving basins, but not all water can be recovered."
            },

            "Cost Per Lock": {
                "value" : format_number(cost_per_lock) + " dollars",
                "tooltip" : "Estimated cost of the water used for this lock cycle. Costs depend on water lost and the local price per gallon"
            }
        }
    elif amount_type == 'per_transit':
        # Full transit calculations (6 locks)
        results = {
            #"Ship Size": ship_size,
            "Water Displaced Per Transit ": {
                "value": format_number(water_displaced * 6),
                "tooltip": "Total water displaced by the ship during a full canal transit, passing through all 6 locks."
            },

            "Water Needed Per Transit": {
                "value" : format_number(water_needed * 6),
                "tooltip" : "Total additional water needed to raise the ship through all locks in a complete transit."
            },

            "Water Lost Per Transit": {
                "value" : format_number(water_lost * 6),
                "tooltip" : "Total amount of water that exits the system and is not recycled throughout the entire canal transit."
            },

            "Cost Per Transit": {
                "value" : format_number(cost_per_lock * 6) + " dollars",
                "tooltip" : "Estimated total cost of the water used for a full transit, based on the water lost and the local price per gallon."
            }
        }

    return results

def format_number(n):
    n = round(n)
    if n > 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.0f} trillion"
    elif n > 1_000_000_000:
        return f"{n / 1_000_000_000:.0f} billion"
    elif n > 1_000_000:
        return f"{n / 1_000_000:.0f} million"
    elif n > 1_000:
        return f"{n / 1_000:.1f}k"
    else:
        return str(n)

if __name__ == '__main__':
    app.run(debug=True)