Este é um projeto de estudo. Quero deixar aqui definido quais são minhas inteções com esse desenvolvimento.

Uma das minhas inteções nesse projeto é adiquirir boas práticas de desenvolvimento, uma delas é chamada de "Separação de Preocupações"(Separation of Concerns(SoC)[Referência](https://medium.com/@okay.tonka/what-is-separation-of-concern-b6715b2e0f75)), que consiste em definir um arquivo para cada "Preocupação" do projeto.

Para o backend estou usando o FastAPI para para construir as APIs com python juntamente com Uvicorn para implementação do servidor web.

O banco de dados utilizado será o SQLite juntamente com a bilbioteca SQLAlchemy para fazer a interação entre o código python e o banco de dados.

models.py - Responsável por descrever a "forma" dos nossos dados.
database.py - Responsável por gerenciar a conexão com o banco de dados.