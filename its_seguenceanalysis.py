import os
import subprocess
import pandas as pd
from pathlib import Path
from io import StringIO

# Ayarlar
reference_db = r"C:\Kodlarim\Aspergillus_ITS_Sequence_Analysis\ITS_RefSeq\ITS_DB"
root_folder = r"C:\Kodlarim\Aspergillus_ITS_Sequence_Analysis\Fastalar"
results_folder = r"C:\Kodlarim\Aspergillus_ITS_Sequence_Analysis\Sonuclar"

barcode_folder_name = input("İşlenecek klasör adını girin (örn: barcode01): ")
output_excel = os.path.join(results_folder, f"{barcode_folder_name}_blast_results.xlsx")

all_results = []

def run_blast(query_path):
    blast_cmd = [
        "blastn",
        "-query", str(query_path),
        "-db", reference_db,
        "-outfmt", "6 qseqid sseqid stitle pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen nident",
        "-max_target_seqs", "100",
    ]
    result = subprocess.run(blast_cmd, capture_output=True, text=True, check=True)
    return result.stdout

def parse_blast_results(blast_output, barcode, fasta_name):
    columns = [
        "qseqid", "sseqid", "stitle", "pident", "length", "mismatch", "gaps", "qstart", "qend",
        "sstart", "send", "evalue", "bitscore", "qlen", "slen", "nident"
    ]
    df = pd.read_csv(StringIO(blast_output), sep="\t", names=columns)

    df["qcov"] = (df["length"] / df["qlen"] * 100).clip(upper=100).round(2)

    df = df[(df["qcov"] >= 95) & (df["pident"] >= 95) & (df["evalue"] == 0.0)]

    df.insert(0, "Barcode", barcode)
    df.insert(1, "Fasta Filename", fasta_name)
    
    # stitle'dan tür ismi çek
    df.insert(2, "ssciname", df["stitle"].apply(lambda x: " ".join(x.split()[1:3]) if len(x.split()) >= 3 else "Unknown"))

    return df

barcode_folder = Path(root_folder) / barcode_folder_name
for fasta_file in barcode_folder.glob("*.fasta"):
    print(f"İşleniyor: {fasta_file}")
    try:
        blast_output = run_blast(fasta_file)
        result_df = parse_blast_results(blast_output, barcode_folder.name, fasta_file.name)
        if not result_df.empty:
            print(result_df.to_string(index=False))
            all_results.append(result_df)
        else:
            print("\tEşleşme bulunamadı veya filtreyi geçemedi.")
    except Exception as e:
        print(f"\tHata oluştu: {e}")

if all_results:
    final_df = pd.concat(all_results, ignore_index=True)
    final_df.to_excel(output_excel, index=False)
    print(f"\nTüm sonuçlar Excel'e yazıldı: {output_excel}")
else:
    print("\nHiçbir sonuç yazılmadı. Eşleşme yok veya tüm sonuçlar filtre dışında kaldı.")
