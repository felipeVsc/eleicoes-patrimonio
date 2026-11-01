# Superset 6.1 on Python 3.12: duckdb 2.x has no wheel for the default image's Python 3.10
FROM apache/superset:6.1.0-py312

USER root
# keep duckdb on the same version as the project (uv.lock): older versions can't read files written by newer ones
RUN uv pip install --python /app/.venv/bin/python --no-cache \
        duckdb==2.0.0 \
        duckdb-engine==0.17.0
COPY --chmod=755 superset-init.sh /app/superset-init.sh
USER superset

CMD ["/app/superset-init.sh"]
