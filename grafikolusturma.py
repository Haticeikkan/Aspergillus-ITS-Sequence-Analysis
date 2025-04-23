import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Yol ayarları
barcode_folder_name = input("Grafiği oluşturmak istediğin barcode klasör adı (örn: barcode01): ")
root_folder = r"C:\Kodlarim\Aspergillus_ITS_Sequence_Analysis\Sonuclar"
excel_file = os.path.join(root_folder, f"{barcode_folder_name}_blast_results.xlsx")
output_plot_path = os.path.join(root_folder, f"{barcode_folder_name}_species_plot.png")

# Excel'den veriyi oku
df = pd.read_excel(excel_file)

# Tür ismi sütunu kontrolü
species_column = 'ssciname'  # Tür adı bu sütunda yer alıyor
species_counts = df[species_column].value_counts()

# Grafik çizimi
plt.figure(figsize=(12, 6))
sns.barplot(x=species_counts.index, y=species_counts.values, palette="viridis")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Sekans Sayısı")
plt.xlabel("Tür")
plt.title(f"{barcode_folder_name} klasöründeki tür dağılımı")
plt.tight_layout()

# Kaydet
plt.savefig(output_plot_path)
plt.close()

print(f"Görsel başarıyla kaydedildi: {output_plot_path}")
