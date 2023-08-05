# History

---
## 0.5.0
- HTML API:
  - Added `auto-select`, `multi-select` and `numbered` flags on `<section>` 
  tag. They take effect only if the `<section>` tag contains options
  - Boolean attributes are evaluated according to HTML5 (if present, a boolean
  attribute is true; if absent, it's false)

- NodeJS API:
  - Added `MenuMeta` and `FormItemMenuMeta` objects to describe `Menu` objects 
  and `FormItemMenu` objects respectively.
    - `MenuMeta` can contain `auto_select`
    - `FormItemMenuMeta` can contain `auto_select`, `multi_select` and `numbered`
    - these attributes have origin in `<section>` tag
---
