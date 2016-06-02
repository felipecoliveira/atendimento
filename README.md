# atendimento
Sistema de Atendimento a Usuários Externos


* **Ubuntu**:

    sudo apt-get -y install libz-dev libxft-dev libjpeg62 libjpeg-dev libfreetype6-dev python-dev

  
* **Configurar Postgresql**:

  * Acessar Postrgresql para criar o banco ``atendimento`` com a role ``atendimento``::

      sudo su - postgres
      psql

      CREATE USER atendimento LOGIN
      ENCRYPTED PASSWORD 'atendimento'
      NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;

      ALTER ROLE atendimento VALID UNTIL 'infinity';

      CREATE DATABASE atendimento
         WITH OWNER = atendimento
         ENCODING = 'UTF8'
         TABLESPACE = pg_default
         LC_COLLATE = 'pt_BR.UTF-8'
         LC_CTYPE = 'pt_BR.UTF-8'
         CONNECTION LIMIT = -1;

      \q
      exit
