import re
import ace_tools as tools

# Caminhos de arquivo
path_in = "/mnt/data/clientes.csv"
path_invalid = "/mnt/data/clientes_invalidos.csv"

# Regex para e‑mail válido
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def contem_espaco(valor):
    """Retorna True se o valor contiver espaços."""
    return " " in str(valor)

def email_valido(email):
    """Valida e‑mail usando regex."""
    return re.match(EMAIL_REGEX, str(email)) is not None

# Ler CSV de entrada
df = pd.read_csv(path_in)

# --- Regras de validação --------------------------------------------------

# 1) Algum campo contém espaço?
mask_espaco = df.applymap(contem_espaco).any(axis=1)

# 2) E‑mail inválido
if "email" in df.columns:
    mask_email_invalido = ~df["email"].apply(email_valido)
else:
    mask_email_invalido = pd.Series(True, index=df.index)  # Se não existir coluna, marca todas

# 3) Altura não numérica
if "altura" in df.columns:
    df["altura_numerica"] = pd.to_numeric(df["altura"], errors="coerce")
    mask_altura_invalida = df["altura_numerica"].isna()
else:
    df["altura_numerica"] = pd.NA
    mask_altura_invalida = pd.Series(True, index=df.index)

# Combina todas as regras
mask_invalido = mask_espaco | mask_email_invalido | mask_altura_invalida

# Separa válidos e inválidos
df_invalidos = df[mask_invalido].copy()
df_validos = df[~mask_invalido].copy()

# Calcula média de altura dos válidos
media_altura = df_validos["altura_numerica"].mean()

# Salva CSV com inválidos
df_invalidos.to_csv(path_invalid, index=False)

# Mostra resultados
tools.display_dataframe_to_user(name="Linhas com problemas", dataframe=df_invalidos)

(media_altura, len(df_validos), len(df_invalidos))
