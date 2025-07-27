# 🐾 SeuPet - Sistema de Adoção de Animais

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![GitHub last commit](https://img.shields.io/github/last-commit/SEU_USUARIO/SEU_REPOSITORIO)
![GitHub repo size](https://img.shields.io/github/repo-size/SEU_USUARIO/SEU_REPOSITORIO)
![GitHub issues](https://img.shields.io/github/issues/SEU_USUARIO/SEU_REPOSITORIO)
![GitHub license](https://img.shields.io/github/license/SEU_USUARIO/SEU_REPOSITORIO)

---

## 📚 Descrição

O **SeuPet** é um sistema web desenvolvido para facilitar o processo de **adoção de animais** em organizações de acolhimento. Ele automatiza tarefas como cadastro de animais, gerenciamento de tutores e controle das adoções, trazendo agilidade, organização e mais transparência para as instituições.

---

## 🛠️ Tecnologias Utilizadas

- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
- ![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white)
- ![Express.js](https://img.shields.io/badge/Express.js-000000?logo=express&logoColor=white)
- ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
- ![Draw.io](https://img.shields.io/badge/Draw.io-FF8800?logo=diagrams.net&logoColor=white)
- ![Visual Studio Code](https://img.shields.io/badge/VS%20Code-007ACC?logo=visual-studio-code&logoColor=white)

---

## 👤 Perfis de Usuário

- **Administrador:** gerencia o sistema (animais, tutores, adoções, usuários).
- **Tutor:** pessoa que deseja adotar um animal.
- **Visitante:** pode visualizar os animais e se cadastrar como tutor.

---

## 📦 Funcionalidades Principais

### 🐶 Animais
- Cadastro de animais
- Edição e remoção
- Listagem com filtros
- Registro de histórico médico e status de adoção

### 👤 Tutores
- Cadastro com CPF e CEP
- Edição e exclusão de perfil
- Visualização de adoções e animais adotados

### 📑 Adoções
- Solicitação de adoção por tutores
- Confirmação de adoção por administradores
- Acompanhamento do status

### 🔒 Usuários
- Login seguro com senha oculta
- Cadastro e gerenciamento de administradores
- Geração de tokens e autenticação

---

## 📁 Estrutura de Diretórios (sugestão)

```
SeuPet/
├── backend/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── app.js
├── frontend/
│   ├── index.html
│   ├── styles/
│   └── scripts/
├── docs/
│   ├── Documento de Requisitos.docx
│   └── Diagrama de Classes.pdf
├── .gitignore
├── README.md
└── package.json
```

---

## ⚙️ Requisitos do Sistema

- Node.js (v18+)
- MongoDB (local ou Atlas)
- Navegador moderno (Chrome, Firefox, Opera)

---

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   ```

2. Instale as dependências:
   ```bash
   cd backend
   npm install
   ```

3. Inicie o servidor:
   ```bash
   npm start
   ```

4. Abra o frontend:
   ```bash
   cd ../frontend
   open index.html  # ou simplesmente abra no navegador
   ```
