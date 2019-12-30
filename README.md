# Tesouro Direto Spider

## Setting Database:
- Create the database:
```sql
create database tesouro_direto;
```
- Create the tables:
```sql
create table public_titles
(
    id         serial primary key,
    name       varchar(50) not null unique,
    due_date   date        not null,
    created_at timestamp default now()
);

comment on table public_titles is 'Nomes e informações imutáveis dos títulos públicos do tesouro direto.';

alter table public_titles
    owner to eliassoares;

create table public_title_values
(
	id SERIAL PRIMARY KEY,
	public_title_id smallint not null references public_titles(id),
	tax float4 not null,
	minimum_value float4 not null,
	unit_price float4 not null,
	created_at timestamp default now()
);

comment on table public_title_values is 'Valores de taxas, valores mínimos e preços unitários do http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos';

CREATE INDEX idx_investing_public_title_values_public_title_id
ON public_title_values(public_title_id);


SET TIMEZONE TO 'America/Sao_Paulo';
```

## Docker:
- Build the image:
```bash
docker build -t tesouro-direto-image .
```

- Run the container:
```bash
docker run --name=tesouro-direto-spider \
    -e POSTGRES_HOST="YOUR_HOST" \
    -e POSTGRES_PORT="YOUR_PORT" \
    -e POSTGRES_PASSWORD="YOUR_PASSWORD" \
    -e POSTGRES_USER="YOUR_USER" \
    tesouro-direto-image  python main.py
```

You can add on your `/etc/crontab`:
```bash
# De segunda à sexta, das 8:05 às 19:05 (para pegar o horário de verão)
5 8-19 * * 1-5   root docker restart tesouro-direto-spider
```
