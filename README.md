# Challenge - News Content Collect and Store



O Factory Method/Pattern permite que cada fonte de dados tenha o seu processamento de forma específica e o Single Responsibility Principle (SRP) também permite que a lógica de tratamento e armazenamento também estajam com suas reponsabilidades independentes. Isso é bom para o projeto, pois isolando as camadas, podemos observar e tratar melhor os erros e criar processos que podem ser utilizados por diversas origens, porque não foram construídas para um serviço específico, mas isoladas como uma ferramenta a ser utilizada.

No caso, poderíamos reutilizar processos e mudar mais rapidamente de um origem de extração, como para o scrap do jornal bbc.com, as modificações ficariam apenas na lógica de extração do novo jogal que possui suas características individuais e não precisaríamos reescrever outros processos, como o de ingestão para o BigQuery.
