# Projeto dbt `eleicoes`

Transformações silver e gold do pipeline. Visão geral, resultados e instruções no
[README da raiz](../README.md); modelo dimensional em [starschema.md](../starschema.md).

```bash
uv run dbt build                          # modelos + testes, na ordem do DAG
uv run dbt docs generate && uv run dbt docs serve   # documentação e grafo de linhagem
```
