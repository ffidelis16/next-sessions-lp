# Entrega final · implementação HubSpot

Fonte canônica: `index.html` da versão publicada no GitHub Pages.

## Decisão executiva

Esta entrega contém somente o **Plano A**: template HTML + HubL novo, exclusivo e isolado, sem editar templates compartilhados do portal. É o caminho registrado como recomendado no package do FECBR 2026 e selecionado para esta implementação.

## Arquivos prontos

- `ENTREGA-FINAL-plano-a.zip`
- `entrega-final-plano-a/LEIA-ME.md`
- `entrega-final-plano-a/plano-final.md`
- `entrega-final-plano-a/passo-a-passo-call.md`
- `entrega-final-plano-a/METADADOS-DA-PAGINA.md`
- `entrega-final-plano-a/developer-files/`
- `entrega-final-plano-a/assets-upload/`
- `entrega-final-plano-a/CHECKSUMS-SHA256.txt`

## Regras de segurança

1. Criar página, template e pasta de assets novos e exclusivos.
2. Não editar `Blank`, `Blank Platform`, `Blank_empty.html` ou outra LP existente.
3. Montar tudo em rascunho e publicar somente após aprovação nominal.
4. Preservar `standard_header_includes` e `standard_footer_includes` para cookies e recursos nativos.
5. Não ativar GTM próprio antes de confirmar o tracking herdado no domínio final.
6. Não criar, remover ou alterar campos do formulário oficial.
7. Não fazer submissão de teste sem contato autorizado pelo cliente.
8. Confirmar domínio, slug, redirect e kit Adobe antes da publicação.

## Gate de execução

- Design Tools disponível e template novo autorizado: executar esta entrega.
- Design Tools indisponível ou única opção envolve editar arquivo compartilhado: interromper e solicitar acesso adequado.

## Reconstrução do package

Depois de qualquer alteração no `index.html` ou nos assets, executar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-hubspot-package.ps1
```

O script extrai CSS, corpo e JavaScript da fonte canônica, atualiza a pasta final, gera checksums e recria o ZIP único.
