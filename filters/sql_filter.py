#!/usr/bin/env python3
import panflute as pf
import sqlite3
import pandas as pd

def format_value(x):
    """Formate les valeurs pour affichage sans casser les types."""
    if pd.isna(x):
        return "None"
    # Évite 1.0 pour les entiers float
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)

def execute_sql(db_path, query):
    """Exécute une requête SQL SQLite et renvoie un tableau HTML."""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()

        # 🔹 Conversion contrôlée : uniquement pour affichage
        display_df = df.map(format_value)

        # 🔹 Rendu HTML sans index
        return display_df.to_html(index=False, escape=False)

    except Exception as e:
        return f"<pre>Erreur SQL : {e}</pre>"


def action(elem, doc):
    """Transforme les blocs SQL en code + résultat HTML."""
    if not (isinstance(elem, pf.CodeBlock) and 'sql' in elem.classes):
        return elem

    query = elem.text.strip()
    db_name = elem.attributes.get("db_name")

    if not db_name:
        return pf.CodeBlock(query, classes=["sql"])

    result_html = execute_sql(db_name, query)

    return [
        pf.CodeBlock(query, classes=["sql"]),
        pf.RawBlock(result_html, format="html")
    ]


def main(doc=None):
    pf.run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
