from stars.stars import load_stars
from constellations.constellations import load_constellations

if __name__ == "__main__":
    stars = load_stars()
    print(f"Loaded {len(stars)} stars.")

    star_lookup = {s.hr: s for s in stars}

    constellations = load_constellations(star_lookup)
    print(f"Loaded {len(constellations)} constellations.")

    for c in constellations[:5]:
        print(c)                # repr: nombre y secuencia de HR
        print("  Stars:", [s.hr for s in c.stars][:10], "…")  # primeros HR convertidos
        # b) Asegúrate de que el número de estrellas enlazadas coincide con el count
        assert len(c.stars) == len(c.hr_sequence), f"{c.name} mismatch!"
    
    print("All checks passed.")