# Qt for Windows (pt-BR)

## Dicas ([Grupo Qt Brasil](https://t.me/qtbrasil))

**_Qual a diferença do Instalador Oficial entre o online/offline?_**

**R =** Obviamente o on necessita de internet durante a instalação do início ao fim. E o
off necessita de um teste de conexão durante a tela de login do instalador, mas a
instalação em si é offline.

---

**_Qual a diferença entre o compilador do VS2015(v140) e VS2017(v141)/VS2019(v142)? E porquê
tem os dois?_**

**R =** Além do **v141** ser mais atualizado como, por exemplo, o uso do C++17.
O que difere na prática é que o **v141** lhe permite usar a API WinRT, ou seja, você
pode desenvolver aplicações no _Qt_ ao estilo _UWP_ (x86/x64) usado no Windows
8/8.1/10 e também o clássico estilo _Win32_ (x64 only) {não me refiro a plataforma x86
nesse caso, mas sim a outra API do Windows _NT_ }, porém o **v140** somente no estilo
WinNT (x86/x64). Se você estiver usando esta opção não esqueça de instalar o
_WinSDK,_ no caso do _Windows 10_ instale duplamente a versão build inicial v10.240 e
a versão atual do mesmo. Pois o inicial tem o depurador “cdb.exe” quanto os mais
recentes não o acrescentam e consequentemente o _Qt Creator_ não detecta.

---

**_E o MinGW [Minimal GNU for Windows]?_**

**R =** O instalador oficial lhe permite baixar usando uma versão obsoleta e no qual não
lhe impede de aprender, mas também não te ajuda em relação as libraries (*.dll, *.a).
Já que a Microsoft foca qualquer desenvolvimento de aplicação no _Windows_ seja
usado o **_M$VC_** , no caso posso citar aqui o package manager (vcpkg) que baixa o
código fonte e compila usando **_M$VC_**. Mas para **_MinGW_** temos como alternativa
mais moderna o **_Msys2_** , no qual você na maioria das vezes não precisa compilar nada,
pois já vem compilado e ele lembra muito a distro ArchLinux usando o pacman. Então se
no caso mais comum de projeto, _ex.:_

- Criar uma aplicação de Banco de Dados usando Mysql, Sqlite, Postgresql e
    Firebird.

Você pode baixar o _Qt_(x86/x64) usando o terminal do **_Msys2_** e poderá também baixar de forma
opcional as libraries adicionais no caso do plugin pgsql e fbsql.
```
Depend. opcionais    : mingw-w64-(i686 ou x86_64)-libmariadbclient
                       mingw-w64-(i686 ou x86_64)-firebird2
                       mingw-w64-(i686 ou x86_64)-postgresql

PS: compile seu projeto no modo release para funcionar com estas dependências!!!
```

**PS:** Existem duas builds para baixar que são **_static_** e tradicionalmente **_dynamic._**
Porém se quiser fazer uma aplicação como do exemplo acima na build **static** , terá
problemas para compilar, ou terá de fazê-lo manualmente recompilando a build com
a source do plugin necessário.

Para mais informações sobre [MSYS2 for Qt WinDev](https://wiki.qt.io/MSYS2)

---

**_Como fazer deploy no Windows?_**

**R =** Simples, quando você instala o _Qt_ pelo instalador oficial **MinGW/MSVC** ele mostra junto aos ícones {_QtCreator, Designer, Assistant_} um console tendo como parametro o diretório do _Qt_ no qual pode procurar a pasta do seu projeto usando o cmd. Já no **_Msys2_** você terá que abrir o terminal dele usando como parâmetro o tipo plataforma que deseja utilizar (**MinGW32/64**), ou simplesmente acrescentar no próprio projeto desta forma, _Ex.:_

**Método 1:** 
- Abra o arquivo.pro e coloque:

```
isEmpty(TARGET_EXT) {
    win32 {
        TARGET_CUSTOM_EXT = .exe
        }
} else {
    TARGET_CUSTOM_EXT = $${TARGET_EXT}
}

win32 {
    DEPLOY_COMMAND = windeployqt
}

CONFIG( debug, debug|release ) {
    # debug
    DEPLOY_TARGET = $$shell_quote($$shell_path($${OUT_PWD}/debug/$${TARGET}$${TARGET_CUSTOM_EXT}))
} else {
    # release
    DEPLOY_TARGET = $$shell_quote($$shell_path($${OUT_PWD}/release/$${TARGET}$${TARGET_CUSTOM_EXT}))
}

# Use += ao invés do = se for usar multiplos QMAKE_POST_LINKs
QMAKE_POST_LINK = $${DEPLOY_COMMAND} $${DEPLOY_TARGET}
```

**Método 2:**
- Abra o seu projeto no _QtCreator_ e aperte Ctrl+5 -> Run -> Add Step Deploy e escolha a opção Custom.
![cap1](https://user-images.githubusercontent.com/6756180/44786137-8d93f580-ab69-11e8-9a53-e3427d8f045b.PNG)
E por fim clique com o botão direito do mouse sobre o projeto e escolha deploy ou simplesmente vai no Menu -> Build -> Deploy

**PS:** Quando se trata de library externo como libSql, entre outros. Você colocará manualmente na pasta do seu **_Executável_**(_Modo: **Release**_) e não do _Projeto source_. Se você for usar **_MSVC_** não esqueçam de acrescentar na pasta do **_Executável_** o _vcredist_(da mesma plataforma  da build), então se for usar um instalador (_InnoSetup, NSIS, Advanced Installer, Qt Installer Framework_) terá todas as dependencias necessárias da **M$** inclusas.
