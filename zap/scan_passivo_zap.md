# Relatório ZAP (Passivo)

Não existem findings de severidade **Medium** ou **High**. A implementação proativa de Middlewares (HSTS, X-Frame-Options, X-Content-Type-Options e CSP), a configuração sem wildcards do CORS, uso estrito do Pydantic (`extra='forbid'`) e autenticação verificando ownership mitificaram os alertas passivos.
