# RedmineTaskCreator
Script que auxilia a criação de tasks no Redmine a partir de uma planilha XLS.

Exemplo:
[![asciicast](https://asciinema.org/a/bruC4ANbOQ2N86fg0Sn3HuRqT.png)](https://asciinema.org/a/bruC4ANbOQ2N86fg0Sn3HuRqT)

## Planilha
O formato da planilha deve ser o seguinte ([exemplo](xls/teste.xlsx)):

| Tarefa  | Descrição | Pontos | Requisitos Associados |
| ------------- | ------------- | ------------- | ------------- |
| [A] Manter usuários  | Tarefa agregadora  | | RFA0123 |
| [BACK-END] Cadastrar usuário  | Cadastra um usuário no BD | 8 | RFU0130, RFS0131
| [FRONT-END] Cadastrar usuário  | Cadastra um usuário na interface | 13 | RFU0130, RFS0131
| [A] Manter empresa  | Tarefa agregadora  | | RFA0140 |
| [BACK-END] Cadastrar empresa  | Cadastra uma empresa no BD | 8 | RFU0141

Taregas que iniciam com `[A]` serão marcadas como `WORKPACKAGE` e as tarefas a seguir terão ela marcada como tarefa pai. No exemplo as tarefas teriam a seguinte hierarquia no Redmine:

```
Manter usuários
|   [BACK-END] Cadastrar usuário
|   [FRONT-END] Cadastrar usuário
Manter empresa
|   [BACK-END] Cadastrar empresa
```

A tag `[A]` é removida na hora de cadastrar a tarefa.

## Modo de utilização
```sh
python createTasksFromXLSX.py [-h] [-u USER] [-p PARENT]
                              [-a ASSIGNEDTO] [-v]
                              filePath
                              
positional arguments:
  filePath              Caminho do arquivo xlsx com as atividades a serem cadastradas

optional arguments:
  -h, --help            Mostra essa ajuda e sai
  -u USER, --user USER  Usuário do redmine
  -p PARENT, --parent PARENT
                        Id da tarefa pai das tarefas a serem criadas (Id da sprint?)
  -v, --verbose         Aumenta a verbosidade da saída do programa
```

A tarefa pai deve estar atribuída para algum usuário pois as tarefas criadas serão atribuídas para este mesmo usuário.

## License

Distributed under the terms of the `MIT` license, "Redmine Task Creator" is free and open source software