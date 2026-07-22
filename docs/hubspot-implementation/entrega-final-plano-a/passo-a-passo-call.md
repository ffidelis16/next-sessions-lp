# Plano A · roteiro da call

Objetivo: Fernando conduz a sequência; a pessoa responsável pelo portal opera o HubSpot. Nenhuma página existente será editada.

## 1. Confirmar antes de mexer

- [ ] Design Tools está disponível?
- [ ] Podemos criar template e pastas novos e exclusivos?
- [ ] Qual será o domínio e slug final?
- [ ] A página herda GTM, GA4, Meta Pixel e banner de cookies?
- [ ] Qual é a URL pública da pasta de assets?
- [ ] Qual URL será usada no redirect após o evento?
- [ ] Qual contato está autorizado para o teste do formulário?

Se a única opção for editar template compartilhado, parar e solicitar acesso para criar um template exclusivo.

## 2. Subir os assets

1. Abrir Files.
2. Criar `evento-modelos-negocio-2608`.
3. Subir todos os arquivos de `assets-upload/`.
4. Abrir um asset e copiar a URL pública, removendo o nome do arquivo.

## 3. Preparar o template

```powershell
cd .\entrega-final-plano-a
.\preparar-com-url.ps1 -AssetBaseUrl "https://cdn2.hubspot.net/hubfs/.../evento-modelos-negocio-2608"
```

Adicionar `-AdobeFontCssUrl "https://use.typekit.net/SEU-KIT.css"` somente se o kit estiver ativo e autorizado para o domínio final.

## 4. Criar o template exclusivo

1. Criar pasta nova no Design Manager.
2. Criar `evento-modelos-negocio.html`, `.css` e `.js`.
3. Copiar os arquivos correspondentes de `developer-files/`.
4. No HTML, usar `evento-modelos-negocio-pronto.html`.
5. Confirmar que o template aparece como `Evento presencial Nuvemshop Next · 26/08`.
6. Se houver erro de HubL, não improvisar no portal: copiar o erro e corrigir localmente.

## 5. Criar a página em rascunho

1. Criar nova landing page.
2. Selecionar o template exclusivo.
3. Preencher os campos de `METADADOS-DA-PAGINA.md`.
4. Manter a página sem publicação.

## 6. QA mínimo

- [ ] Desktop: 1440, 1280 e 1024 px.
- [ ] Mobile: 390, 375 e 360 px.
- [ ] Sem overflow horizontal.
- [ ] Imagens e logos carregam.
- [ ] Foto do Galileu está nítida na máscara circular.
- [ ] Contador corresponde à tabela D-45 a D-1, com troca às 00h BRT.
- [ ] Modal abre, fecha por botão, backdrop e `Esc`, e devolve o foco.
- [ ] Formulário carrega uma vez e não duplica.
- [ ] Banner de cookies e consentimento nativo aparecem.
- [ ] Eventos não são duplicados.
- [ ] Preview público corresponde ao rascunho aprovado.

Problemas devem ser corrigidos na fonte local e repassados ao package; não editar às pressas dentro do template durante a call.
