from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session to work

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Check if 'ship_size' is in the form (user submitted the main form)
    if 'ship_size' in request.form:
        ship_size = int(request.form['ship_size'])
        session['ship_size'] = ship_size  # Store it in session
    else:
        # If no ship_size is submitted, use the last saved value
        ship_size = session.get('ship_size', 50000)  # Default to 50,000 if missing

    amount_type = (request.form.get('amount', 'per_lock')) # Transit amount to be displayed

    # Print the values to verify they are received correctly
    print(f"Received ship_size: {ship_size}")
    #print(f"Recieved transit amount: {transit_amount}")

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

    # Calculate locks
    result = {
        "Panamax" : lock_calculation(panamax_lock_data, ship_size, amount_type),
        "Neopanamax" : lock_calculation(neopanamax_lock_data, ship_size, amount_type),

    }

    # If JavaScript updates amount_type, return only the results section
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template('results.html', result=result)

    return render_template('index.html', result=result, amount_type=amount_type)

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
            "Ship Size": ship_size,
            "Water Displaced Per Lock": format_number(water_displaced),
            "Water Needed Per Lock": format_number(water_needed),
            "Water Lost Per Lock": format_number(water_lost),
            "Cost Per Lock": format_number(cost_per_lock),
        }
    elif amount_type == 'per_transit':
        # Full transit calculations (6 locks)
        results = {
            "Ship Size": ship_size,
            "Water Displaced Per Transit ": format_number(water_displaced * 6),
            "Water Needed Per Transit": format_number(water_needed * 6),
            "Water Lost Per Transit": format_number(water_lost * 6),
            "Cost Per Transit": format_number(cost_per_lock * 6)
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
        return f"{n / 1_000:.1f} thousand"
    else:
        return str(n)

if __name__ == '__main__':
    app.run(debug=True)