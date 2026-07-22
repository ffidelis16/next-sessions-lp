# Plano A · template codificado exclusivo

## Objetivo

Criar uma nova landing page usando um template HTML + HubL exclusivo para o evento presencial de 26/08, mantendo o comportamento da versão aprovada e sem alterar estruturas compartilhadas do portal.

## Estrutura

- `developer-files/evento-modelos-negocio.html`
- `developer-files/evento-modelos-negocio.css`
- `developer-files/evento-modelos-negocio.js`
- `assets-upload/` com todas as imagens e logos
- `preparar-com-url.ps1` para gerar o template pronto

O template usa `enableDomainStylesheets: false`, `standard_header_includes`, `standard_footer_includes` e uma URL-base única para os assets do Files.

## Sequência

1. Confirmar permissão para criar template novo no Design Manager.
2. Criar pasta exclusiva `evento-modelos-negocio-2608` no Files e no Developer File System.
3. Fazer upload de `assets-upload/` no Files.
4. Copiar a URL pública da pasta e executar `preparar-com-url.ps1`.
5. Criar os três arquivos de `developer-files/` no Design Manager.
6. Colar o conteúdo de `evento-modelos-negocio-pronto.html` no template.
7. Criar nova landing page em rascunho usando somente esse template.
8. Preencher metadados, domínio, slug, imagem social e redirect.
9. Validar página, formulário, cookies e tracking antes de publicar.

## Formulário

- Portal: `8180620`
- Formulário: `bdb0ccad-d2b3-471a-adf1-9187057e1ab3`
- O formulário é carregado apenas na primeira abertura do modal.
- Os CTAs seguintes apenas reabrem o mesmo formulário.
- Não manipular o conteúdo interno do iframe do HubSpot.

## Tracking

A página envia `cta_click`, `form_open`, `form_submit`, `generate_lead`, `scroll_depth` e `scarcity_state` ao `dataLayer`. O package não instala um container GTM. O time de dados deve confirmar se o domínio final já fornece GTM/GA/Pixel e mapear os eventos sem duplicação.

## Rollback

Antes da publicação, descartar o rascunho. Depois da publicação, despublicar ou redirecionar a URL. O template exclusivo pode permanecer arquivado sem afetar outras páginas.
