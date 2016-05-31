# atendimento
Sistema de Atendimento a Usuários Externos

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
