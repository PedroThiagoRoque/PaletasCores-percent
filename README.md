# Gerador de Paleta de Cores
Este é um aplicativo desktop criado com CustomTkinter, que permite ao usuário selecionar uma imagem, ajustar o número de cores desejadas para a paleta e gerar uma nova imagem contendo a paleta de cores extraída da imagem original.

## Funcionalidades
Seleção de Imagem: O usuário pode carregar uma imagem do computador para extração das cores.<br>
Ajuste de Parâmetros: O usuário pode definir o número de cores que deseja na paleta.<br>
Geração da Paleta de Cores: O aplicativo processa a imagem, agrupa cores semelhantes e gera uma nova imagem com a paleta correspondente.<br>
Feedback Visual de Processamento: Durante o processamento, um popup de carregamento com bloqueio da interface principal é exibido, garantindo uma experiência fluida.<br>
Suporte a imagens nos formatos JPG e PNG.<br>

## Tecnologias Utilizadas
Python 3.x <br>
CustomTkinter: Para criar a interface gráfica moderna.<br>
Pillow (PIL): Para manipulação de imagens.<br>
Scikit-learn (KMeans): Para quantização e agrupamento de cores semelhantes.<br>
Threading: Para evitar bloqueio da interface gráfica durante o processamento da imagem.<br>

## Instalação
Clone este repositório para o seu computador:<br>

git clone https://github.com/PedroThiagoRoque/PaletasCores-percent.git<br>
Instale as dependências necessárias. Você pode fazer isso com pip:<br>

customtkinter<br>
Pillow<br>
scikit-learn<br>

## Execute o script principal:
python AppCores.py <br>
OU Executável (.exe) na Pasta Dist/ <br>
Caso queira gerar um executável para Windows, use o PyInstaller: <br>

Instale o PyInstaller (se ainda não tiver instalado): <br>

pip install pyinstaller<br>
Gere o arquivo .exe:<br>

pyinstaller --onefile --windowed AppCores.py<br>
O executável será gerado na pasta dist.<br>

## Como Utilizar
Ao abrir o aplicativo, clique no botão "Selecionar Imagem" para escolher uma imagem do seu computador.
Defina o número de cores que deseja para a paleta usando o campo "Número de Cores".
Clique no botão "Gerar Imagem" para gerar e salvar a imagem contendo a paleta de cores.
Um popup de carregamento será exibido durante o processamento e, ao final, uma mensagem será mostrada informando o local onde a imagem foi salva.

## Exemplo de Uso

<sub>Exemplo de interface gráfica.</sub>

Ao carregar uma imagem, você verá uma versão reduzida dela na interface, e ao gerar a paleta de cores, uma nova imagem será salva no diretório de execução.
