"""Top export per country (CEPII BACI 2018, via Visual Capitalist 'Mapped: The Top Export in Every Country') -> category."""
TOP = {
 "Canada": "Petroleum", "Greenland": "Fish", "Mexico": "Cars", "United States of America": "Petroleum",
 "Algeria": "Petroleum", "Angola": "Petroleum", "Benin": "Cotton", "Burkina Faso": "Gold", "Burundi": "Gold",
 "Cameroon": "Petroleum", "Central African Rep.": "Wood", "Chad": "Petroleum", "Congo": "Petroleum",
 "Côte d'Ivoire": "Cocoa", "Djibouti": "Sheep and goats", "Dem. Rep. Congo": "Copper", "Egypt": "Petroleum",
 "Eritrea": "Zinc", "Ethiopia": "Coffee", "Gambia": "Nuts", "Ghana": "Gold", "Guinea": "Gold", "Guinea-Bissau": "Nuts",
 "Kenya": "Tea", "Liberia": "Gold", "Libya": "Petroleum", "Madagascar": "Vanilla", "Malawi": "Tobacco", "Mali": "Gold",
 "Mauritania": "Iron", "Morocco": "Cars", "Mozambique": "Cloves", "Niger": "Gold", "Nigeria": "Petroleum",
 "Rwanda": "Gold", "Senegal": "Gold", "Sierra Leone": "Titanium", "Somalia": "Sheep and goats", "Somaliland": "Sheep and goats",
 "South Africa": "Gold", "Botswana": "Gold", "Lesotho": "Gold", "Namibia": "Gold", "eSwatini": "Gold",
 "S. Sudan": "Petroleum", "Sudan": "Petroleum", "Tanzania": "Gold", "Togo": "Petroleum", "Tunisia": "Wires",
 "Uganda": "Gold", "Zambia": "Copper", "Zimbabwe": "Gold",
 "Afghanistan": "Grapes", "Armenia": "Copper", "Azerbaijan": "Petroleum", "Bangladesh": "Suits", "Bhutan": "Ferro-alloys",
 "Brunei": "Petroleum", "Cambodia": "Jerseys", "China": "Transmission apparatus", "North Korea": "Watches",
 "Georgia": "Copper", "Indonesia": "Coal", "Iran": "Petroleum", "Iraq": "Petroleum", "Israel": "Diamonds",
 "Japan": "Cars", "Jordan": "Fertilizers", "Kazakhstan": "Petroleum", "Kuwait": "Petroleum", "Kyrgyzstan": "Gold",
 "Laos": "Electricity", "Lebanon": "Gold", "Malaysia": "Electronic circuits", "Mongolia": "Coal", "Myanmar": "Petroleum",
 "Nepal": "Yarn", "Oman": "Petroleum", "Pakistan": "Bed linen", "Philippines": "Electronic circuits", "Qatar": "Petroleum",
 "Saudi Arabia": "Petroleum", "South Korea": "Electronic circuits", "Sri Lanka": "Tea", "Palestine": "Stones",
 "Syria": "Olive oil", "Tajikistan": "Gold", "Thailand": "Machinery", "Turkmenistan": "Petroleum", "Turkey": "Cars",
 "United Arab Emirates": "Petroleum", "Uzbekistan": "Gold", "Vietnam": "Transmission apparatus", "Yemen": "Petroleum",
 "Taiwan": "Electronic circuits",
 "Albania": "Footwear", "Austria": "Cars", "Belarus": "Petroleum", "Belgium": "Cars", "Bosnia and Herz.": "Electricity",
 "Bulgaria": "Petroleum", "Croatia": "Petroleum", "Cyprus": "Petroleum", "N. Cyprus": "Petroleum", "Czechia": "Cars", "Denmark": "Medicine",
 "Estonia": "Transmission apparatus", "Finland": "Petroleum", "France": "Airplanes", "Germany": "Cars", "Greece": "Petroleum",
 "Hungary": "Cars", "Iceland": "Aluminium", "Ireland": "Medicine", "Italy": "Medicine", "Latvia": "Wood", "Lithuania": "Petroleum",
 "Luxembourg": "Cars", "Moldova": "Wires", "Montenegro": "Aluminium", "Netherlands": "Petroleum", "Norway": "Petroleum",
 "Poland": "Cars", "Portugal": "Cars", "Romania": "Cars", "Russia": "Petroleum", "Serbia": "Wires", "Slovakia": "Cars",
 "Slovenia": "Cars", "Spain": "Cars", "Sweden": "Cars", "Switzerland": "Gold", "North Macedonia": "Chemicals",
 "United Kingdom": "Cars", "Ukraine": "Sunflower seeds", "Kosovo": "Wires",
 "Argentina": "Petroleum", "Bahamas": "Cruise ships", "Belize": "Sugar", "Bolivia": "Petroleum", "Brazil": "Soybeans",
 "Chile": "Copper", "Colombia": "Petroleum", "Costa Rica": "Medical instruments", "Cuba": "Cigars", "Dominican Rep.": "Gold",
 "Ecuador": "Petroleum", "El Salvador": "T-shirts", "Falkland Is.": "Fish", "Guatemala": "Bananas", "Guyana": "Gold",
 "Haiti": "T-shirts", "Honduras": "T-shirts", "Jamaica": "Aluminium", "Nicaragua": "T-shirts", "Panama": "Petroleum",
 "Paraguay": "Soybeans", "Peru": "Copper", "Suriname": "Gold", "Trinidad and Tobago": "Petroleum", "Uruguay": "Wood pulp",
 "Venezuela": "Petroleum", "Puerto Rico": "Medicine",
 "Australia": "Coal", "New Zealand": "Milk",
 # not in the VC list; top export 2018 per OEC/BACI (crude or refined petroleum):
 "India": "Petroleum", "Gabon": "Petroleum", "Eq. Guinea": "Petroleum", "Timor-Leste": "Petroleum",
}
CAT = {
 "OIL": {"Petroleum", "Coal"},
 "METALS": {"Gold", "Copper", "Iron", "Zinc", "Titanium", "Aluminium", "Diamonds", "Ferro-alloys", "Stones"},
 "FOOD": {"Fish", "Cotton", "Wood", "Cocoa", "Sheep and goats", "Coffee", "Nuts", "Tea", "Vanilla", "Tobacco", "Cloves",
          "Grapes", "Olive oil", "Sunflower seeds", "Sugar", "Soybeans", "Cigars", "Bananas", "Wood pulp", "Milk"},
 "MADE": {"Cars", "Airplanes", "Machinery", "Wires", "Cruise ships", "Transmission apparatus", "Electronic circuits",
          "Watches", "Medicine", "Medical instruments", "Suits", "Jerseys", "Yarn", "Bed linen", "Footwear", "T-shirts",
          "Chemicals", "Fertilizers", "Electricity"},
}
def cat(name):
    p = TOP.get(name)
    for k, v in CAT.items():
        if p in v: return k
    return None
