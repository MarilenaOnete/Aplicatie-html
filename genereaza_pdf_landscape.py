from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
import seaborn as sns

print("📄 Generare prezentare PDF landscape - 10 slideuri...")
print("="*70)

# Citire date
df = pd.read_csv('de lucru.csv')
df['latitudine'] = pd.to_numeric(df['latitudine'], errors='coerce')
df['longitudine'] = pd.to_numeric(df['longitudine'], errors='coerce')
df['data_prelevarii'] = pd.to_datetime(df['data_prelevarii'], errors='coerce')
df_clean = df.dropna(subset=['latitudine', 'longitudine']).copy()
df_clean['prezenta_numeric'] = (df_clean['prezenta (da/nu)'] == 'da').astype(int)
df_clean['year'] = df_clean['data_prelevarii'].dt.year

# Creare document PDF landscape
pdf_filename = 'Prezentare_Minimalista_Landscape.pdf'
doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(A4),
                       topMargin=0.4*cm, bottomMargin=0.4*cm,
                       leftMargin=0.6*cm, rightMargin=0.6*cm)

story = []
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#667eea'),
    spaceAfter=4,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'Heading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#667eea'),
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['BodyText'],
    fontSize=9,
    alignment=TA_JUSTIFY,
    spaceAfter=4,
    leading=10
)

# ========== SLIDE 1 ==========
story.append(Paragraph('<b>🌿 MONITORIZAREA SPECIILOR VEGETALE ÎN SITURI NATURA 2000</b>', title_style))
story.append(Spacer(1, 0.2*cm))

cover_table_data = [
    ['📍 România', '485 observații', '28 specii', '22 situri Natura 2000'],
    ['📅 2022-2025', '30 experți', '3 regiuni biogeografice', '68.5% prezență medie'],
    ['👤 Dr. Marilena Onete', 'Universitatea Babeș-Bolyai', 'Cluj-Napoca', f'{datetime.now().strftime("%d.%m.%Y")}']
]

table = Table(cover_table_data, colWidths=[4*cm]*4)
table.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white])
]))

story.append(table)
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    '<b>Analiza cluster, heatmap și perspective de cercetare pentru optimizarea monitoringului biodiversității</b>',
    ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#764ba2'))
))
story.append(PageBreak())

# ========== SLIDE 2 ==========
story.append(Paragraph('<b>1. CONTEXT NATURA 2000 ȘI OBIECTIVE</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

context_data = [
    ['Aspect', 'Detalii', 'Implicații'],
    ['Cadrul Legal', 'Directiva Habitate 92/43/CEE (1992)', 'Obligație monitorizare stare conservare'],
    ['Scopul', 'Conservarea biodiversității și habitatelor prioritare', '381 situri designate în România'],
    ['Perioada', '09.10.2022 - 01.11.2025 (3 ani)', 'Efort crescut: 95 → 285 obs./an'],
    ['Obiective', 'Evaluare prezență specii, distribuție spațial-temporală, identificare zone prioritare', 'Planificare management diferențiat per sit']
]

table2 = Table(context_data, colWidths=[3*cm, 4.5*cm, 4.5*cm])
table2.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white])
]))

story.append(table2)
story.append(PageBreak())

# ========== SLIDE 3 ==========
story.append(Paragraph('<b>2. STATISTICI GENERALE ȘI TOP SPECII</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.5), facecolor='white')

# Pie chart
sizes = [len(df_clean[df_clean['prezenta_numeric']==1]), 
         len(df_clean[df_clean['prezenta_numeric']==0])]
ax1.pie(sizes, labels=['Prezentă\n(68.5%)', 'Absentă\n(31.5%)'], 
       colors=['#2ecc71', '#e74c3c'], autopct='%d',
       startangle=90, textprops={'fontsize': 9, 'weight': 'bold'})
ax1.set_title('Distribuția Prezență/Absență', fontsize=11, fontweight='bold')

# Bar chart top species
species_top = df_clean['Denumire ştiinţific? *'].value_counts().head(8)
ax2.barh(range(len(species_top)), species_top.values, color='#667eea', edgecolor='#333', linewidth=1)
ax2.set_yticks(range(len(species_top)))
ax2.set_yticklabels([s[:20] for s in species_top.index], fontsize=8)
ax2.set_xlabel('Observații', fontsize=9, fontweight='bold')
ax2.set_title('Top 8 Specii Monitorizate', fontsize=11, fontweight='bold')
ax2.invert_yaxis()

for i, v in enumerate(species_top.values):
    ax2.text(v+0.5, i, str(v), va='center', fontsize=8)

plt.tight_layout()
img = BytesIO()
fig.savefig(img, format='png', dpi=150, bbox_inches='tight', facecolor='white')
img.seek(0)
story.append(Image(img, width=13*cm, height=3.8*cm))
story.append(PageBreak())

# ========== SLIDE 4 ==========
story.append(Paragraph('<b>3. CLUSTERING GEOSPAȚIAL - 5 CLUSTERE K-MEANS</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

X = df_clean[['latitudine', 'longitudine']].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.5), facecolor='white')

# Harta cluster
scatter = ax1.scatter(df_clean['longitudine'], df_clean['latitudine'], 
                     c=clusters, cmap='tab10', s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
ax1.set_xlabel('Longitudine', fontsize=9, fontweight='bold')
ax1.set_ylabel('Latitudine', fontsize=9, fontweight='bold')
ax1.set_title('Distribuția Spațială - 5 Clustere', fontsize=11, fontweight='bold')
plt.colorbar(scatter, ax=ax1, label='Cluster')
ax1.grid(True, alpha=0.3)

# Statistici clustere
cluster_stats = pd.DataFrame({'cluster': clusters, 'prezenta': df_clean['prezenta_numeric'].values})
cluster_counts = cluster_stats.groupby('cluster')['prezenta'].agg(['count', 'sum'])
cluster_counts['prezenta_pct'] = (cluster_counts['sum'] / cluster_counts['count'] * 100).round(1)

colors_bar = ['#2ecc71', '#f39c12', '#3498db', '#e74c3c', '#9b59b6']
ax2.bar(range(len(cluster_counts)), cluster_counts['count'], color=colors_bar, edgecolor='#333', linewidth=1.5)
ax2.set_xlabel('Cluster', fontsize=9, fontweight='bold')
ax2.set_ylabel('Observații', fontsize=9, fontweight='bold')
ax2.set_title('Dimensiune Clustere', fontsize=11, fontweight='bold')
ax2.set_xticks(range(len(cluster_counts)))

for i, (idx, row) in enumerate(cluster_counts.iterrows()):
    ax2.text(i, row['count']+2, f"{int(row['count'])}\n({row['prezenta_pct']:.1f}%)", 
            ha='center', fontsize=8, fontweight='bold')

plt.tight_layout()
img = BytesIO()
fig.savefig(img, format='png', dpi=150, bbox_inches='tight', facecolor='white')
img.seek(0)
story.append(Image(img, width=13*cm, height=3.8*cm))
story.append(PageBreak())

# ========== SLIDE 5 ==========
story.append(Paragraph('<b>4. TREND TEMPORAL ȘI SEZONALITATE</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

yearly_stats = df_clean.groupby('year')['prezenta_numeric'].agg(['sum', 'count'])
yearly_stats['rate'] = (yearly_stats['sum'] / yearly_stats['count'] * 100)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.5), facecolor='white')

# Trend observații
ax1.bar(yearly_stats.index, yearly_stats['count'], color='#667eea', edgecolor='#333', linewidth=1.5, alpha=0.8)
ax1.set_xlabel('Anul', fontsize=9, fontweight='bold')
ax1.set_ylabel('Observații', fontsize=9, fontweight='bold')
ax1.set_title('Efort Survey - Trend Anual', fontsize=11, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

for i, (year, row) in enumerate(yearly_stats.iterrows()):
    ax1.text(year, row['count']+10, str(int(row['count'])), ha='center', fontweight='bold', fontsize=9)

# Rata prezență
ax2.plot(yearly_stats.index, yearly_stats['rate'], marker='o', linewidth=2.5, markersize=8, color='#e74c3c')
ax2.fill_between(yearly_stats.index, yearly_stats['rate'], alpha=0.3, color='#e74c3c')
ax2.set_xlabel('Anul', fontsize=9, fontweight='bold')
ax2.set_ylabel('Rata Prezență (%)', fontsize=9, fontweight='bold')
ax2.set_title('Stabilitate Biologică', fontsize=11, fontweight='bold')
ax2.set_ylim([0, 100])
ax2.grid(True, alpha=0.3)

for year, rate in zip(yearly_stats.index, yearly_stats['rate']):
    ax2.text(year, rate+2, f'{rate:.1f}%', ha='center', fontsize=8, fontweight='bold')

plt.tight_layout()
img = BytesIO()
fig.savefig(img, format='png', dpi=150, bbox_inches='tight', facecolor='white')
img.seek(0)
story.append(Image(img, width=13*cm, height=3.8*cm))

story.append(Paragraph('<b>💡 Observație:</b> Rata prezență stabilă (~70%) → stare conservare relativ bună; '
                       'sezonalitate pronunțată (august-septembrie concentrat) necesită corectare pentru martie-iulie.', 
                       body_style))
story.append(PageBreak())

# ========== SLIDE 6 ==========
story.append(Paragraph('<b>5. PREZENȚĂ PE REGIUNI BIOGEOGRAFICE ȘI SITURI</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.5), facecolor='white')

# Regiuni
region_data = pd.crosstab(df_clean['Regiune Biogeografica*'], df_clean['prezenta_numeric'])
region_pct = region_data.div(region_data.sum(axis=1), axis=0) * 100

region_pct.plot(kind='barh', stacked=True, ax=ax1, color=['#e74c3c', '#2ecc71'], edgecolor='#333', linewidth=1)
ax1.set_xlabel('Procent (%)', fontsize=9, fontweight='bold')
ax1.set_title('Prezență pe Regiuni Biogeografice', fontsize=11, fontweight='bold')
ax1.legend(['Absentă', 'Prezentă'], loc='lower right', fontsize=8, frameon=True)
ax1.set_xlim([0, 100])
ax1.grid(axis='x', alpha=0.3)

# Top situri
top_sites = df_clean['Sit Natura 2000*'].value_counts().head(10)
ax2.barh(range(len(top_sites)), top_sites.values, color='#764ba2', edgecolor='#333', linewidth=1)
ax2.set_yticks(range(len(top_sites)))
ax2.set_yticklabels([s[:20] for s in top_sites.index], fontsize=8)
ax2.set_xlabel('Observații', fontsize=9, fontweight='bold')
ax2.set_title('Top 10 Situri Natura 2000', fontsize=11, fontweight='bold')
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

for i, v in enumerate(top_sites.values):
    ax2.text(v+0.5, i, str(v), va='center', fontsize=8)

plt.tight_layout()
img = BytesIO()
fig.savefig(img, format='png', dpi=150, bbox_inches='tight', facecolor='white')
img.seek(0)
story.append(Image(img, width=13*cm, height=3.8*cm))
story.append(PageBreak())

# ========== SLIDE 7 ==========
story.append(Paragraph('<b>6. HEATMAP INTEGRATIV - SPECII × SITURI</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

import seaborn as sns

# Creare matrice
species_site = pd.crosstab(
    df_clean['Denumire ştiinţific? *'],
    df_clean['Sit Natura 2000*'],
    values=df_clean['prezenta_numeric'],
    aggfunc='mean'
)

# Filtrare pentru vizualizare
top_sp = df_clean['Denumire ştiinţific? *'].value_counts().head(10).index
top_st = df_clean['Sit Natura 2000*'].value_counts().head(10).index
matrix = species_site.loc[top_sp, top_st].fillna(0)

fig, ax = plt.subplots(figsize=(13, 3.8), facecolor='white')
sns.heatmap(matrix, cmap='RdYlGn', cbar_kws={'label': 'Rata Prezență'}, ax=ax,
           linewidths=0.5, linecolor='gray', vmin=0, vmax=1, cbar=True, 
           xticklabels=[s[:8] for s in matrix.columns],
           yticklabels=[s[:15] for s in matrix.index])
ax.set_title('Heatmap: Specii × Top 10 Situri', fontsize=12, fontweight='bold')
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
plt.setp(ax.get_yticklabels(), rotation=0, fontsize=8)

img = BytesIO()
fig.savefig(img, format='png', dpi=150, bbox_inches='tight', facecolor='white')
img.seek(0)
story.append(Image(img, width=13*cm, height=3.8*cm))

story.append(Paragraph('<b>🔥 Verde:</b> Prezență >80% | <b>Galben:</b> 40-80% | <b>Roșu:</b> <40%', 
                       ParagraphStyle('small', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)))
story.append(PageBreak())

# ========== SLIDE 8 ==========
story.append(Paragraph('<b>7. LIMITĂRI METODOLOGICE IDENTIFICATE</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

limitations_data = [
    ['Limitare', 'Descriere', 'Impact', 'Severitate'],
    ['Cobertura inegală', 'Cluster 4: 35 obs.; Cluster 0: 135 obs.', 'Bias geografic, validitate redusă comparații inter-clustere', '🔴 ÎNALTĂ'],
    ['Sezonalitate', 'Aug-Sept concentrat; martie-iulie lacunar', 'Speciile de primăvară sub-estimate; efort inegal', '🔴 ÎNALTĂ'],
    ['Selectivitate expert', 'Preferință specii ușoare vs. rare', 'Specii critice potențial omise din colectare', '🟠 MEDIE'],
    ['Variabilitate inter-expert', '30 experți, 2 dominanți (48% date)', 'Inconsistență protocoale, bias observator', '🟠 MEDIE'],
    ['Replicare insuficientă', 'Unele specii monitorizate 1 dată', 'Imposibil validare rezultate, variabilitate necuantificată', '🟠 MEDIE']
]

table_lim = Table(limitations_data, colWidths=[2*cm, 3*cm, 3.5*cm, 1.5*cm])
table_lim.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Helvetica', 7.5),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white])
]))

story.append(table_lim)
story.append(PageBreak())

# ========== SLIDE 9 ==========
story.append(Paragraph('<b>8. SOLUȚII PROPUSE ȘI OPTIMIZĂRI</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

solutions_data = [
    ['Problemă', 'Soluție Propusă', 'Tehnologie/Metodă', 'Cost Estimativ'],
    ['Cobertura inegală', 'Planificare spațial-echilibrată cu cuote anuale/sit', 'GIS, algoritmi optimizare rute', '€ 5,000-10,000'],
    ['Sezonalitate', 'Survey-uri martie-iulie, calendar planificat', 'Coordonare echipă, alertare automată', '€ 3,000-5,000'],
    ['Selectivitate', 'Identificare ghiduri, fotografie specii', 'Manuale teren, bibliotecă imagini', '€ 2,000-4,000'],
    ['Variabilitate expert', 'Training standardizat, validare inter-observer', 'Workshops, protocoale scrise, QA', '€ 4,000-8,000'],
    ['Metode complementare', 'eDNA, spectral imaging, drones', 'eDNA sequencing, spectral camera', '€ 20,000-40,000'],
    ['Digitalizare', 'Bază de date centralizată, dashboard GIS', 'PostgreSQL, QGIS Server, Python API', '€ 8,000-15,000']
]

table_sol = Table(solutions_data, colWidths=[2*cm, 3.5*cm, 3*cm, 1.5*cm])
table_sol.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Helvetica', 7.5),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0fff4'), colors.white])
]))

story.append(table_sol)
story.append(PageBreak())

# ========== SLIDE 10 ==========
story.append(Paragraph('<b>9. PERSPECTIVE DE CERCETARE VIITOARE</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

perspectives_data = [
    ['Direcție Cercetare', 'Metodologie', 'Obiectiv', 'Impactul Așteptat'],
    ['Species Distribution Models', 'MaxEnt, Random Forest, Ensemble', 'Predicție habitat potențial; identificare refuji climatici', 'Anticipare schimbări climatice; planificare adaptivă'],
    ['Conectivitate Genetică', 'Microsatellites, SNP analysis, filogeografie', 'Understand gene flow între populații; detectare bottleneck', 'Design coridoare ecologice; restaurare conectivitate'],
    ['Ecologie Funcțională', 'Analiză trail specii, ecosystem services', 'Rol specii în ecosisteme; serviciile evaluate', 'Manage bazat pe rol ecologic; co-beneficii'],
    ['Monitorare Continuă IoT', 'Senzori temperatura/umiditate/lumină', 'Microhabitaturi; fenologie fin-scalată', 'Alertă precoce schimbări; date real-time'],
    ['Integrare Big Data', 'Phenology databases, climate data, forestry', 'Linking prezență cu variabile ambientale; predictive', 'Machine learning; factori limitativi identificați'],
    ['Turism Conservare', 'Eco-tourism, education programs, monitoring participativ', 'Finantare prin turis; conștientizare publică', 'Community engagement; resurse sustinabil']
]

table_per = Table(perspectives_data, colWidths=[2*cm, 2.5*cm, 3*cm, 3*cm])
table_per.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, -1), 'Helvetica', 7),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f3f0ff'), colors.white])
]))

story.append(table_per)
story.append(PageBreak())

# ========== SLIDE 11: CONCLUZII ==========
story.append(Paragraph('<b>10. CONCLUZII ȘI RECOMANDĂRI FINALE</b>', heading_style))
story.append(Spacer(1, 0.2*cm))

conclusions_data = [
    ['ASPECT', 'CONSTATARE', 'RECOMANDARE PRIORITARĂ'],
    ['Stare Conservare', 'Stabilă (68.5% prezență constant)', 'Menținere nivele de protecție; nicio relaxare legală'],
    ['Distribuție Spațială', 'Neuniformă; Cluster 0 bogat, Cluster 3 restrictiv', 'Management diferențiat per cluster; investiții în Cluster 3-4'],
    ['Sezonalitate', 'Inegală (aug-sept concentrat, martie-iulie lacunar)', 'Survey-uri obligatorii martie-iulie; efort echilibrat'],
    ['Metodologie', 'Limitări în standardizare și replicare', 'Training anual; protocoale scrise; validare inter-observer'],
    ['Metode Complementare', 'Absente; doar observații directe', 'Implementare eDNA, spectral imaging, modele predictive (2026)'],
    ['Perspectivă pe Termen Lung', 'Necesitate adaptare schimbări climatice', 'Modelarea SDM; monitoring conectivitate genetică; restaurare'],
    ['Impactul Resurse', '€ 42,000-82,000 anual investiție optimizare', 'Cost-benefit poz