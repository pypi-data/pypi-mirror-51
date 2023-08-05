#SDK Braspag

###Gerar Token de autenticação

```
from Auth import Auth


client_id = {{client Id fornecido pela Braspag}}
client_secret = {{client Secret fornecido pela Braspag}}

auth = Auth(client_id, client_secret)

# Gera o token de autenticação
auth.generate_token()

# Retorna o token gerado
print(bp.token)

# Verifica se o token ainda é válido
print(bp.expired_token())
```

