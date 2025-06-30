Este é um bot para gerenciamento de servidores de FiveM
## 🚀 Funcionalidades Principais

✅ **Registro de Membros**  
- Usuários podem se registrar com nome, ID e telefone.  
- Sistema de aprovação por administradores.  
- Visualização da lista de membros registrados e aprovados.  
- Comando de demissão de membros.

✅ **Tickets de Farm**  
- Cria canais privados para cada membro registrar suas atividades de farm/venda.

✅ **Painel de Farm/Venda/Dinheiro Sujo**  
- Registre quantidades de itens farmados.
- Registre vendas com cálculo automático de comissão.
- Registre valores de dinheiro sujo.

✅ **Painel Financeiro**  
- Registre entradas, saídas e gastos.
- Visualize o saldo total da facção.

✅ **Painel de Parceiros**  
- Cadastre parceiros por setor (Armas, Munição, Lavagem, Drogas, Desmanche, Legal).
- Consulte parceiros por setor.

✅ **Comissão**  
- Gere relatório de comissão individual com base nas vendas dos membros.

✅ **Logs**  
- Todas as ações importantes são logadas em um canal de logs específico.

---

## 📌 Principais Comandos

| Comando | Descrição |
| ------- | --------- |
| `!listarcomandos` | Lista todos os comandos do bot. |
| `!registro` | Abre formulário para registro de membro. |
| `!listar_registros` | Lista todos os registros aprovados (Admins). |
| `!demitir` | Inicia processo de demissão de membro (Admins). |
| `!ticket` | Cria ticket/aba de farm individual para o membro. |
| `!farm` | Painel para registrar farm, vendas e dinheiro sujo. |
| `!financeiro` | Painel para registrar entradas, saídas e gastos. |
| `!saldo` | Exibe saldo atual da facção. |
| `!addparceiro` | Cadastro de parceiros por setor (Admins). |
| `!parcerias` | Consulta parceiros por setor. |
| `!comissao` | Lista comissão que cada membro tem a receber. |

---

## ⚙️ Requisitos

- Python 3.8+
- Bibliotecas:
  - `discord.py` (Ext)
  - `json` (padrão)
  - `os` (padrão)
  - `re` (padrão)

Instale o `discord.py` com:
```bash
pip install -U discord.py
