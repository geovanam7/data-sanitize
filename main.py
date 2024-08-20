import pandas as pd
import matplotlib.pyplot as plt


def generate_comparison_graphs(file_path):
    try:
        # Carregar o arquivo Excel, especificando a linha de cabeçalho correta
        data = pd.read_excel(file_path, header=4)  # A partir da linha 5 (índice 4)
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return

    # Renomear as colunas para facilitar o entendimento
    data.columns = ['Brasil e Município', 'Total', 'Fossa ligada à rede', 'Fossa não ligada à rede',
                    'Fossa rudimentar', 'Vala', 'Rio, lago, córrego ou mar',
                    'Outra forma', 'Não tinham banheiro nem sanitário']

    # Substituir valores "-" por NaN para tratamento de dados ausentes
    data.replace("-", pd.NA, inplace=True)

    # Remover linhas onde o nome do município é NaN
    data_cleaned = data.dropna(subset=['Brasil e Município'])

    # Converter colunas numéricas para tipo float inicialmente
    for col in ['Total', 'Fossa ligada à rede', 'Fossa não ligada à rede',
                'Fossa rudimentar', 'Vala', 'Rio, lago, córrego ou mar',
                'Outra forma', 'Não tinham banheiro nem sanitário']:
        data_cleaned[col] = pd.to_numeric(data_cleaned[col], errors='coerce')

    # Converter colunas numéricas para tipo inteiro, substituindo NaN por 0
    for col in ['Total', 'Fossa ligada à rede', 'Fossa não ligada à rede',
                'Fossa rudimentar', 'Vala', 'Rio, lago, córrego ou mar',
                'Outra forma', 'Não tinham banheiro nem sanitário']:
        data_cleaned[col] = data_cleaned[col].fillna(0).astype(int)

    # Criar as colunas 'Estado' e 'Município'
    data_cleaned['Estado'] = data_cleaned['Brasil e Município'].apply(
        lambda x: x.split(' ')[-1] if '(' in x else ''
    ).str.replace("(", "").str.replace(")", "").str.strip()
    data_cleaned['Município'] = data_cleaned['Brasil e Município'].apply(
        lambda x: x.split(' (')[0] if '(' in x else x
    ).str.strip()
    data_cleaned.sort_values(['Estado', 'Município'], inplace=True)

    # Exibir todos os registros filtrados com formatação melhorada
    print("\nDados Filtrados e Organizados por Estado e Município:")
    print(data_cleaned[['Estado', 'Município', 'Total', 'Fossa ligada à rede', 'Fossa não ligada à rede',
                        'Fossa rudimentar', 'Vala', 'Rio, lago, córrego ou mar',
                        'Outra forma', 'Não tinham banheiro nem sanitário']].to_string(index=False,
                                                                                       float_format='{:.2f}'.format))

    # Filtrar dados para o Brasil
    brasil_data = data_cleaned[data_cleaned['Município'] == 'Brasil']

    # Filtrar dados para São Mateus - ES
    sao_mateus_data = data_cleaned[(data_cleaned['Município'] == 'São Mateus') & (data_cleaned['Estado'] == 'ES')]

    # Criar gráficos separados em uma única figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    if not brasil_data.empty:
        columns_to_plot = [
            'Total', 'Fossa ligada à rede', 'Fossa não ligada à rede',
            'Fossa rudimentar', 'Vala', 'Rio, lago, córrego ou mar',
            'Outra forma', 'Não tinham banheiro nem sanitário'
        ]
        bars = ax1.bar(columns_to_plot, brasil_data[columns_to_plot].values.flatten(), color='skyblue')

        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:,.0f}',  # Formatando o número com separador de milhar
                ha='center',
                va='bottom'
            )

        ax1.set_title('Distribuição dos Dados Totais do Brasil')
        ax1.set_xlabel('Categorias')
        ax1.set_ylabel('Quantidade')
        ax1.tick_params(axis='x', rotation=45)

    if not sao_mateus_data.empty:
        columns_to_plot_sao_mateus = [
            'Total', 'Fossa ligada à rede', 'Fossa não ligada à rede',
            'Fossa rudimentar', 'Vala', 'Rio, lago, córrego ou mar',
            'Outra forma', 'Não tinham banheiro nem sanitário'
        ]
        bars_sao_mateus = ax2.bar(columns_to_plot_sao_mateus,
                                  sao_mateus_data[columns_to_plot_sao_mateus].values.flatten(), color='lightcoral')

        for bar in bars_sao_mateus:
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:,.0f}',  # Formatando o número com separador de milhar
                ha='center',
                va='bottom'
            )

        ax2.set_title('Distribuição dos Dados de São Mateus - ES')
        ax2.set_xlabel('Categorias')
        ax2.set_ylabel('Quantidade')
        ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Caminho do arquivo Excel
    file_path = 'tabela6805.xlsx'

    # Gerar gráficos comparativos
    generate_comparison_graphs(file_path)
