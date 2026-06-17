import json

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + '\n' for line in source.split('\n')[:-1]] + [source.split('\n')[-1]] if source else []
    }

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + '\n' for line in source.split('\n')[:-1]] + [source.split('\n')[-1]] if source else []
    }

with open('Roentgenstrahlung.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_add = [
    create_code_cell("""# Plot: Absorption nach Material (log-Skala)
plt.figure(figsize=(10, 6))
# Verwende log-Skala für die y-Achse
plt.bar(materialien, I_korr_5_3, color='#58D68D', zorder=3)
plt.yscale('log')
plt.ylabel('Intensität I_korr [1/s] (log-Skala)')
plt.title('Absorption nach Material (d = 0,5 mm, korrigierte Daten)')
plt.grid(True, axis='y', linestyle='--', alpha=0.7, zorder=0)

# Werte über den Balken anzeigen
for i, v in enumerate(I_korr_5_3):
    plt.text(i, v * 1.1, f"{v:.2f}", ha='center', va='bottom', fontsize=9)

plt.show()"""),

    create_markdown_cell("""### Physikalische Interpretation der Ergebnisse

Die Messdaten zeigen eine starke Abhängigkeit der Absorption von der Ordnungszahl $Z$ des jeweiligen Materials. Dieses Verhalten lässt sich durch zwei wesentliche physikalische Effekte erklären.

#### Einfluss der Ordnungszahl Z
Bei der verwendeten Energie von 21 kV ist der Photoeffekt der dominierende Wechselwirkungsprozess zwischen Röntgenstrahlung und Materie.
Die Wahrscheinlichkeit $\\tau$, dass ein Röntgenphoton absorbiert wird, steigt näherungsweise proportional zu $Z^4$ an. Dadurch besitzen Materialien mit hoher Ordnungszahl ein deutlich größeres Absorptionsvermögen.

**Leichte Elemente**
Materialien wie Luft oder Kohlenstoff besitzen nur kleine Ordnungszahlen ($Z \\approx 6-7$). Ihre Atome enthalten vergleichsweise wenige Elektronen, wodurch die Wahrscheinlichkeit für eine Wechselwirkung mit der Strahlung gering bleibt. Die Röntgenstrahlung kann diese Materialien daher weitgehend ungehindert durchdringen.

**Schwere Metalle**
Schwere Metalle wie Eisen, Kupfer oder Silber besitzen eine deutlich höhere Elektronendichte und stärkere Kernladung. Dadurch steigt die Wahrscheinlichkeit für den Photoeffekt stark an.
Besonders Silber mit $Z = 47$ zeigt eine sehr starke Abschwächung der Strahlung. Die gemessene Intensität sinkt nahezu auf Null, was die hohe Wirksamkeit schwererer Elemente im Strahlenschutz verdeutlicht.

#### Die Zirkonium-Anomalie und die K-Absorptionskante
Ein auffälliges Ergebnis der Messreihe ist das Verhalten von Zirkonium. Trotz seiner hohen Ordnungszahl zeigt es eine größere Restintensität als theoretisch erwartet. Dieses Verhalten lässt sich durch die sogenannte K-Absorptionskante erklären.

Damit ein Röntgenphoton ein Elektron aus der innersten K-Schale eines Atoms herausschlagen kann, muss seine Energie größer sein als die Bindungsenergie dieses Elektrons.
Die K-Schalen-Bindungsenergie von Zirkonium liegt bei etwa:
$E_K \\approx 18\\text{ keV}$

Das verwendete Röntgenspektrum bei 21 kV enthält jedoch viele Photonen mit Energien unterhalb dieses Wertes. Diese Photonen besitzen nicht genügend Energie, um Elektronen aus der K-Schale des Zirkoniums herauszulösen. Für diesen Spektralbereich wird Zirkonium daher teilweise „transparent“.

Bei Eisen und Kupfer liegen die K-Absorptionskanten dagegen deutlich niedriger:
- Eisen: etwa 7,1 keV
- Kupfer: etwa 9,0 keV

Da nahezu das gesamte erzeugte Röntgenspektrum oberhalb dieser Energien liegt, können diese Materialien die Strahlung wesentlich effizienter absorbieren.

#### Zusammenfassung
Die Ergebnisse zeigen, dass die Absorption von Röntgenstrahlung im niedrigen Energiebereich stark von der Ordnungszahl des Materials abhängt. Materialien mit hoher Ordnungszahl absorbieren die Strahlung deutlich stärker als leichte Elemente.

Zusätzlich treten energieabhängige Transparenzeffekte auf, wenn die Photonenenergie unterhalb der Bindungsenergie innerer Elektronenschalen liegt. Diese sogenannten Absorptionskanten beeinflussen das Absorptionsverhalten erheblich und müssen bei der Auswahl geeigneter Abschirmmaterialien berücksichtigt werden."""),

    create_markdown_cell("""## 5.4 Beugung von Röntgenstrahlung am NaCl-Einkristall
In diesem Versuchsabschnitt wird die Wellennatur der Röntgenstrahlung mithilfe der Beugung an einem NaCl-Einkristall untersucht. Ziel des Experiments ist die Aufnahme des Röntgenspektrums sowie die experimentelle Bestimmung charakteristischer Wellenlängen der erzeugten Strahlung.

### Versuchsprinzip und Bragg-Bedingung
Die Beugung der Röntgenstrahlung erfolgt nach dem Prinzip der Bragg-Reflexion. Treffen die Röntgenstrahlen unter dem Glanzwinkel $\\theta$ auf die Netzebenen des Kristalls, so entsteht konstruktive Interferenz, wenn der Gangunterschied einem ganzzahligen Vielfachen der Wellenlänge $\\lambda$ entspricht.

Die Bedingung hierfür wird durch die Bragg-Gleichung beschrieben:
$n \\cdot \\lambda = 2 \\cdot d \\cdot \\sin(\\theta)$

Dabei gilt:
- $d = 282,01\\text{ pm}$ als Netzebenenabstand des NaCl-Kristalls,
- $n$ als Beugungsordnung,
- $\\lambda$ als Wellenlänge der Röntgenstrahlung,
- $\\theta$ als Glanzwinkel.

Nur wenn diese Bedingung erfüllt ist, entstehen Intensitätsmaxima im gemessenen Spektrum.

### Physikalische Analyse des Beugungsspektrums
Die grafische Darstellung der Zählrate in Abhängigkeit vom Glanzwinkel $\\theta$ zeigt eine klare Trennung zwischen kontinuierlichem Untergrund und charakteristischen Peaks der Molybdän-Anode.

**Kontinuierliches Bremsstrahlungsspektrum (Bremsberg)**
Das kontinuierliche Spektrum entsteht durch die Abbremsung der Elektronen im Coulombfeld der Anode. Dabei wird kinetische Energie in Röntgenstrahlung umgewandelt.
Der steile Anstieg der Intensität bei kleinen Winkeln (ca. 4,5° bis 5,0°) entspricht der Grenzwellenlänge $\\lambda_{min}$. Unterhalb dieser Wellenlänge ist keine Emission mehr möglich, da die Elektronenenergie vollständig ausgeschöpft wäre.

**Charakteristische Linien ($K_\\alpha$ und $K_\\beta$)**
Die scharfen Intensitätsmaxima im Spektrum sind die charakteristischen Linien der Molybdän-Anode.

Dabei gilt:
- $K_\\alpha$-Linie: höhere Intensität
- $K_\\beta$-Linie: geringere Intensität

Die höhere Intensität der $K_\\alpha$-Linie ergibt sich aus der größeren Übergangswahrscheinlichkeit innerhalb der Elektronenhülle.

### Charakteristische Kennlinien (Messdatentabelle und Peak-Identifikation)
Die folgende Tabelle zeigt die gemessenen Glanzwinkel der wichtigsten Intensitätsmaxima sowie deren Zuordnung zu den charakteristischen Spektrallinien."""),

    create_code_cell("""# Charakteristische Kennlinien
data_5_4 = {
    'Beugungsordnung (n)': [1, 1, 2, 2],
    'Linie': ['K_beta', 'K_alpha', 'K_beta', 'K_alpha'],
    'Glanzwinkel theta [°]': [6.3, 7.2, 12.8, 14.4],
    'Zählrate R [1/s]': [361.3, 420.0, 140.0, 160.0]
}

df_5_4 = pd.DataFrame(data_5_4)
display(df_5_4)"""),

    create_markdown_cell("""### Interpretation der Ergebnisse
Die Messdaten weisen insgesamt eine hohe Qualität und gute Übereinstimmung mit der Theorie auf.

**Wellenlängenbestimmung**
Über die gemessenen Glanzwinkel kann mithilfe der Bragg-Gleichung die Wellenlänge der Molybdän-Strahlung experimentell bestimmt werden.
Ein Vergleich der $K_\\alpha$-Linie mit dem Literaturwert von etwa
$\\lambda \\approx 71\\text{ pm}$
dient dabei zur Validierung der Messgenauigkeit und zeigt eine gute Übereinstimmung zwischen Theorie und Experiment.

**Apparative Auflösung**
Die deutliche und scharfe Auflösung der Beugung in zweiter Ordnung belegt die hohe Qualität der Messapparatur.
Insbesondere zeigt dies die sehr gute Justage des Röntgengoniometers sowie die hohe Güte des verwendeten NaCl-Einkristalls.

**Konsistenz der Messdaten**
Die Lage der Peaks in erster und zweiter Beugungsordnung steht in direktem Einklang mit der theoretischen Erwartung der Bragg-Bedingung.
Insbesondere folgt das Verhältnis der Winkel für $n = 1$ und $n = 2$ der sinusabhängigen Struktur der Bragg-Gleichung exakt, was die Gültigkeit des zugrunde liegenden Modells für diesen Versuchsaufbau bestätigt.""")
]

nb['cells'].extend(cells_to_add)

with open('Roentgenstrahlung.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Part 2 cells successfully added to Roentgenstrahlung.ipynb")
