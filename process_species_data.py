import pandas as pd
import folium
from folium import plugins
import json

# Citire CSV
df = pd.read_csv('de lucru.csv')

# Curățare date
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')

# Eliminare rânduri cu coordonate invalide
df = df.dropna(subset=['latitudine', 'longitudine'])

# Creare hartă de bază
map_center = [df['latitudine'].mean(), df['longitudine'].mean()]
m = folium.Map(
    location=map_center,
    zoom_start=7,
    tiles='OpenStreetMap'
)

# Colorare după status prezență
colors_map = {
    'da': '#2ecc71',  # Verde
    'nu': '#e74c3c'   # Roșu
}

status_names = {
    'da': 'Prezentă',
    'nu': 'Absentă'
}

# Adăugare markeri
for idx, row in df.iterrows():
    if pd.notna(row['latitudine']) and pd.notna(row['longitudine']):
        status = row['prezenta (da/nu)']
        color = colors_map.get(status, '#95a5a6')
        
        popup_text = f"""
        <b>{row['COD specie*']}</b><br>
        <i>{row['Denumire ştiinţific? *']}</i><br>
        <b>Status:</b> {status_names.get(status, 'Nespecificat')}<br>
        <b>Data:</b> {row['data_prelevarii']}<br>
        <b>Sit:</b> {row['Sit Natura 2000*']}<br>
        <b>Localitate:</b> {row['Localitate*']}<br>
        <b>Expert:</b> {row['nume expert *']}
        """
        
        folium.CircleMarker(
            location=[row['latitudine'], row['longitudine']],
            radius=8,
            popup=folium.Popup(popup_text, max_width=300),
            color='rgba(0,0,0,0.2)',
            fill=True,
            fillColor=color,
            fillOpacity=0.8,
            weight=2
        ).add_to(m)

# Adăugare legendă
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; right: 50px; width: 250px; height: 180px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:14px; padding: 10px;
     border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2)">
     
<p style="margin: 0 0 10px 0; font-weight: bold; color: #333;">
    🌿 Legenda</p>
     
<p style="margin: 5px 0;">
    <i class="fa fa-circle" style="color:#2ecc71"></i> 
    <span style="color: #2ecc71; font-weight: bold;">Prezentă</span> - Specie detectată</p>
    
<p style="margin: 5px 0;">
    <i class="fa fa-circle" style="color:#e74c3c"></i> 
    <span style="color: #e74c3c; font-weight: bold;">Absentă</span> - Specie nedetectată</p>

<hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">

<p style="margin: 5px 0; font-size: 12px;">
    <b>Total observații:</b> {}</p>
<p style="margin: 5px 0; font-size: 12px;">
    <b>Specii prezente:</b> {}</p>
<p style="margin: 5px 0; font-size: 12px;">
    <b>Specii absente:</b> {}</p>
</div>
'''.format(
    len(df),
    len(df[df['prezenta (da/nu)'] == 'da']),
    len(df[df['prezenta (da/nu)'] == 'nu'])
)

m.get_root().html.add_child(folium.Element(legend_html))

# Salvare hartă
m.save('harta_specii_natura2000.html')
print("✓ Hartă creată: harta_specii_natura2000.html")

# Statistici
print("\n📊 STATISTICI:")
print(f"Total observații: {len(df)}")
print(f"Specii prezente: {len(df[df['prezenta (da/nu)'] == 'da'])}")
print(f"Specii absente: {len(df[df['prezenta (da/nu)'] == 'nu'])}")
print(f"Specii unice: {df['Denumire ştiinţific? *'].nunique()}")
print(f"\nSituri Natura 2000: {df['Sit Natura 2000*'].nunique()}")