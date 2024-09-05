import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog, messagebox

# Função para carregar dados
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
    if file_path:
        try:
            if file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                data = pd.read_csv(file_path)
            return data
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")
            return None

# Função para gerar gráficos e exibir o produto mais vendido por loja
def generate_plots(data):
    if data is None:
        return

    try:
        # Verificar se as colunas necessárias existem
        if 'ID Loja' not in data.columns or 'Produto' not in data.columns or 'Valor Final' not in data.columns:
            messagebox.showerror("Erro", "Os dados não contêm as colunas necessárias: 'ID Loja', 'Produto', e 'Valor Final'")
            return

        # Identificar o produto mais vendido por loja
        store_product_sales = data.groupby(['ID Loja', 'Produto'])['Valor Final'].sum().reset_index()
        top_products = store_product_sales.loc[store_product_sales.groupby('ID Loja')['Valor Final'].idxmax()]

        # Exibir o produto mais vendido por loja
        result_text = "\n".join([f"ID Loja: {row['ID Loja']}\nProduto: {row['Produto']}\nValor Final: {row['Valor Final']}" for _, row in top_products.iterrows()])
        messagebox.showinfo("Produto Mais Vendido por Loja", result_text)

        # Gráfico de barras do total gasto por produto para cada loja
        plt.figure(figsize=(12, 8))
        sns.barplot(x='ID Loja', y='Valor Final', hue='Produto', data=store_product_sales)
        plt.title("Total Gasto por Produto em Cada Loja")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("bar_plot.png")
        plt.show()

        # Gráficos de pizza para cada loja
        for loja in data['ID Loja'].unique():
            loja_data = store_product_sales[store_product_sales['ID Loja'] == loja]
            plt.figure(figsize=(10, 6))
            loja_data.set_index('Produto')['Valor Final'].plot.pie(autopct='%1.1f%%', startangle=140)
            plt.title(f"Distribuição do Gasto por Produto na Loja {loja}")
            plt.tight_layout()
            plt.savefig(f"pie_chart_{loja}.png")
            plt.show()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar os gráficos: {e}")

# Configuração da interface
def main():
    root = ctk.CTk()
    root.title("Programa de Ciência de Dados")

    load_button = ctk.CTkButton(root, text="Carregar Dados", command=lambda: generate_plots(load_data()))
    load_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
