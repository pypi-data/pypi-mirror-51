# pullrequester
Este é um script [python](https://www.python.org/) para criação de pull requests em um repositório [Git](https://git-scm.com/) de acordo com os padrões da smiles

## Utilização
### Instalação
```
sudo yum install python pip
pip --trusted-host nexus-agile.smiles.local.br install --extra-index-url=http://nexus-agile.smiles.local.br/repository/smiles-pypi/simple --upgrade pullrequester
```

### Execução
Para executar o script, rodar com os seguintes parâmetros:
```
python -m pullrequester <github_token> <repo_path> <branch_name>
```

## Desenvolvimento
### Dependências
#### Runtime
- [PyGithub](http://pygithub.readthedocs.io/en/latest/introduction.html)
- [gitator](https://github.com/smiles-sa/gitator)

#### Testes
- [pytest](http://docs.pytest.org/en/latest/)

### Estratégia de Testes
Este script utiliza o framework [pytest](http://docs.pytest.org/en/latest/) para facilitar os testes unitários.

#### Setup para testes
Para rodar os testes, primeiro clonar o repositório e criar um `virtualenv`:
```
git clone git@github.com:smiles-sa/pullrequester.git
virtualenv -p python3 pullrequester
cd pullrequester
source bin/activate
```
Na sequência instalar as dependências. Segue exemplo (baseado em Enterprise Linux):
```
sudo yum install python pip
cd pullrequester
pip install -r requirements.txt
```

#### Execução dos testes
Para executar os testes, rodar o pytest:
```
pytest
```
